import json
import os

import jsonpath

from common.logger_util import write_log
from common.yaml_util import get_object_path, read_config_file


def analysis_json(data,method,params=None):
    """
    将data 改成测试需要的请求数据
    :param data: 原始数据
    :param version: 修改的 version
    :param method:  请求方法
    :param params: 参数
    :return:  修改后的data
    """
    for i in data:
        # print(i)
        if isinstance(i, dict):
            for head_key in i:
                if "v" in head_key:
                    i[head_key] = read_config_file("base_version","version")
        if isinstance(i, list):
            for j in i:
                for data_key in j:
                    if "method" in data_key:
                        j[data_key] = method
                    if "params" in data_key:
                        if params!=None:
                            j[data_key] = params
            return data

def read_json_data(path):
    """
    读取json文件
    :param path: 路径
    :return: json数据
    """
    with open(path,"r",encoding="utf-8") as f:
         data=json.loads(f.read())
         return data
def write_json_data(data,path):
    """
    写入python
    :param data: 要写入的数据
    :param path: 存放路径
    :return:
    """
    with open(path,"w") as f:
        json.dump(data,f)
        write_log("正在存入数据")

def get_json_data(data,key):
    """
    获取指定的值
    :param data:数据源
    :param key: 查询的key
    :return: value
    """
    value=jsonpath.jsonpath(data,"$.."+key+"")
    return value


if __name__ == '__main__':
   path=get_object_path()+"/data/data.json"
   print(analysis_json(read_json_data(path),"1.7.3","hello",params={}))