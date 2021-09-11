import json
import traceback

import requests

from common.json_util import analysis_json, read_json_data, get_json_data
from common.logger_util import write_log, error_log
from common.tools import replace_data
from common.yaml_util import read_config_file, get_object_path, read_testcase_file
from debug_talk import DebugTalk


class RequestsUtil():
    """
      统一请求封装
      """
    session = requests.session()

    def __init__(self):
        self.url = ""
        self.data = ""

    def replace_value(self, data):
        def replace_data(data):
            for i in range(1, data.count("${") + 1):
                if "${" in data and "}" in data:
                    start_index = data.index("${")  # 获取下标
                    end_index = data.index("}", start_index)  # 从start坐标开始，向后找的第一个坐标
                    old_value = data[start_index:end_index + 1]  # +1找到后边两个字符
                    func_name = old_value[2:old_value.index("(")]  # 获取函数名称
                    args_name = old_value[old_value.index("(") + 1:old_value.index(")")]  # 获取参数
                    new_value = getattr(DebugTalk(), func_name)(*args_name.split(','))
                    if isinstance(new_value, list):
                        data = data.replace(old_value, str(*new_value))
                    else:
                        data = data.replace(old_value, str(new_value))
                    return data
            # 不管什么类型，统一转换成字符串格式

        if data and isinstance(data, dict):  # 如果data不为空，并且data的类型是一个字典
            str_data = json.dumps(data)
        else:
            str_data = data

        for i in range(str_data.count("${")):
            old_data = str_data[str_data.rfind("${"):]
            new_data = replace_data(old_data)
            str_data = str_data.replace(old_data, new_data)
        if not data or not isinstance(data, dict):
            data = str_data
            # 还原数据类型
        else:  # 如果data不为空，并且data的类型是一个字典
            data = json.loads(str_data)  # 反序列化，还原数据类型
        return data

    def get_url(self, method, uid):
        """
          获取url
          :param method:
          :param uid:
          :return:
          """
        url = read_config_file("base_url", "dev_url")
        url = replace_data(url, method, uid)
        return url

    def get_uid(self):
        """
        获取uid
        :return:
        """
        method = "login_getUid"
        data = analysis_json(read_json_data(get_object_path() + "/data/data.json"), method)
        res = self.send_request("123456789", method, data)
        res = json.loads(json.dumps(res))
        uid = get_json_data(res, "uid")
        return uid

    def analysis_yaml(self, caseinfo):
        """

        :param caseinfo: 分析传进来的用例数据，然后请求接口
        :return:
        """
        self.method = caseinfo['method']

        self.params = caseinfo['params']
        self.params = analysis_json(read_json_data(get_object_path() + "/data/data.json"), self.method, self.params)
        self.name = caseinfo['name']
        self.uid = self.get_uid()
        # 请求接口
        res = self.send_request(*self.uid, self.method, self.params)
        # 断言，把返回值拿去加工一下，然后做断言
        expected_results = caseinfo['validate']
        actual_results = res
        write_log("接口的实际返回值:{0}".format(res))
        write_log("---------断言下边的预期结果和实际结果--expected_results={0}---actual_results={1}------".format(expected_results, actual_results) )
        self.validate_result(expected_results, actual_results)

        return res

    def send_request(self, uid, method, data):
        """
          发送请求
          :param uid:
          :param method:
          :param data:
          :return:
          """
        # print(uid, data, method, "-------发送的各种数据------")
        self.url = self.get_url(method, str(uid))
        self.data = data
        res = RequestsUtil.session.request("post", url=self.url, json=data)
        res_data = json.loads(json.dumps(res.json()))
        return res_data
    def validate_result(self, expected_results, actual_results):
        """
          断言
          :param expected_results:预期结果集 list，
          :param actual_results: 实际结果集，执行接口返回数据 json or list
          :return:
          """
        try:
            # 解析数据
            # 断言是否成功标记，0成功，其他失败
            flag = 0
            if expected_results and isinstance(expected_results, list):
                for expected in expected_results:
                    for key, value in dict(expected).items():
                        # 断言方式
                        if key == "equals":
                            for assert_key, assert_value in dict(value).items():
                                if assert_key == 'retCode':
                                    if get_json_data(actual_results, 'retCode')[0] != assert_value:
                                        flag = flag + 1
                                        write_log("断言失败：{0}不等于{1}".format(assert_key, assert_value))
                                elif assert_key == 'asset':
                                    write_log( "获取asset的值:{0}".format(get_json_data(actual_results, 'asset')))
                                    for i in get_json_data(actual_results, 'asset'):
                                        asset_flg = 0
                                        for value  in i:
                                            if str(i[value]) not in str(self.replace_value(assert_value)):
                                                asset_flg=asset_flg+1
                                            else:
                                                asset_flg=0
                                                break
                                        if asset_flg!=0:
                                            write_log("断言失败：{0}中不存在{1}".format(
                                                get_json_data(actual_results, 'asset'),
                                                self.replace_value(assert_value)))
                                else:
                                    # write_log("--------第二次进行断言时-------------", actual_results, assert_key)
                                    key_list = get_json_data(actual_results, assert_key)
                                    #print(key_list, "-------key_list的值--------")
                                    if key_list:
                                        if assert_value not in key_list:
                                            flag = flag + 1
                                            write_log("断言失败：{0}不等于{1}".format(assert_key, assert_value))
                                    else:
                                        flag = flag + 1
                                        write_log("断言失败：返回结果中不存在{0}".format(assert_key))
            assert flag == 0
            write_log("-------------------接口请求成功------------------")
        except Exception as f:
            write_log("--------接口请求失败-------------")
            write_log("----------接口请求结束-----------")
            error_log("断言异常：异常信息%s" % str(traceback.format_exc()))
if __name__ == "__main__":
    data = read_testcase_file(r"\testcases\drone_sell.yml")
    data1 = get_json_data(data, "asset")
    # print(data1)
    value = RequestsUtil.replace_value(*data1)
    print(value)
