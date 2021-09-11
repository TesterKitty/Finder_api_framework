from common.json_util import get_json_data, read_json_data
from common.tools import calculate_data
from common.yaml_util import get_object_path


class DebugTalk:

     def get_login_data(self,key):
         """
         获取登陆的数据
         :param data:
         :param key:
         :return:
         """
         data=read_json_data(get_object_path()+"/data/login_data.json")
         return get_json_data(data,key)
     def get_asset(self,symbol,*args):
         """

         :param symbol:运算符
         :param args: 参数
         :return:
         """
         return calculate_data(symbol,*args)