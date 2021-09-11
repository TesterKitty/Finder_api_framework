import pytest

from common.game_data import GameData
from common.yaml_util import clear_extract_file


@pytest.fixture(scope='function',autouse=True)
def game_login():
    GameData().game_init()

@pytest.fixture(scope="session",autouse=True)
def log():
    print("test log")



