import json

from common.yaml_util import read_testcase_file



def replace_data(data,*args):
    new_data=data
    def replace_lod(data, new_str):
        """
        替换数据
        :param data:数据源
        :param new_str: 要替换的值
        :return: new_data
        """
        if data and isinstance(data, dict):
            str_data = json.dumps(data)
        else:
            str_data = data
        for value in range(1, str_data.count("${") + 1):
            if "${" in str_data and "}" in data:
                start_indext = str_data.index("${")  # 获取下标
                end_index = str_data.index("}", start_indext)
                old_value = str_data[start_indext:end_index + 1]
            return str_data.replace(old_value, new_str)
    for i in args:
        new_data=replace_lod(new_data,i)
    return new_data



def calculate_data(symbol,*args):
    try:
        if len(args)<2:
            print("传入参数少于2无法进行运算")
            return
        elif symbol!="+" and symbol!="-" and symbol==None:
             print("不支持的运算符：%s"%symbol)
             return
        if symbol=="+":
           num=0
           for i in args:
               num=num+int(i)
           return num
        if symbol=="-":
            num = 0
            argslist=list(args)
            argslist.sort(reverse=True)
            for i in range(len(argslist)):
               if i==0:
                   num=int(argslist[i])
                   continue
               print(num,argslist[i])
               num=num-int(argslist[i])
            return num
    except:
        print("运算符不存在或，参数不是整数")
if __name__ == '__main__':
  ...
