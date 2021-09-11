import allure
import  pytest

from common.requests_util import RequestsUtil
from common.yaml_util import read_testcase_file

@allure.epic("findler,apiauto")
@allure.feature("僚机&任务")
class TestRequests:
       @allure.story("出售僚机")
       @pytest.mark.parametrize('caseinfo',read_testcase_file(r"\testcases\drone_sell.yml"))
       def test_drone_sell(self,caseinfo):
           RequestsUtil().analysis_yaml(caseinfo)
       @allure.story("任务领取")
       @pytest.mark.parametrize('caseinfo',read_testcase_file(r'\testcases\task_gainTaskReward.yml'))
       def test_task_gainTaskReward(self,caseinfo):
           RequestsUtil().analysis_yaml(caseinfo)

