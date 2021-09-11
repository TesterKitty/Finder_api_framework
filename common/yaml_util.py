import json
import os.path

import yaml




def get_object_path():
    """
    获取项目根路径
    :return:
    """
    return os.path.abspath(os.getcwd().split('common')[0])

def read_config_file(one_node,two_node):
    """
    读取yml
    :param one_node: 根节点
    :param two_node: 一节点
    :return: value[one_node][two_node]
    """
    with open(get_object_path()+"/config.yml",encoding="utf-8") as f:
         value=yaml.load(stream=f,Loader=yaml.FullLoader)
         return value[one_node][two_node]

#读取yaml测试用例
def read_testcase_file(yaml_path):
    """
    读取测试用例配置
    :param yaml_path:文件路径，当前路径，非全路径
    :return:  caseinfo
    """
    with open(get_object_path()+yaml_path,encoding="utf-8") as f:
        caseinfo=yaml.load(stream=f,Loader=yaml.FullLoader)
        return caseinfo
#清空extract.yml文件
def clear_extract_file():
    # with open(get_object_path()+"/extract.yml",encoding='utf-8',mode='w') as f:
    #       f.truncate() #清空
    ...

if __name__ == '__main__':
    # read_cofig_file("base_url","dev_url")
    res= read_testcase_file("/testcases/drone_sell.yml")
    print(res)


