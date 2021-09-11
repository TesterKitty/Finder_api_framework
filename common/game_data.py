import json

from common.json_util import analysis_json, read_json_data, get_json_data, write_json_data
from common.requests_util import RequestsUtil
from common.yaml_util import get_object_path


class GameData(RequestsUtil):



    def get_login_data(self):
        method="login"
        data = analysis_json(read_json_data(get_object_path() + "/data/data.json"), method)
        uid=self.get_uid()
        res=self.send_request(str(*uid),method,data)
        login_data=json.loads(json.dumps(res))
        write_json_data(login_data,get_object_path()+"/data/login_data.json")
        return login_data
    def game_init(self):
        self.get_uid()
        self.get_login_data()
        # print(self.get_login_data())


if __name__ == '__main__':
    gamedata=GameData()



