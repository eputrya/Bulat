import os
import sys

import allure
from tests import check_ver_platform

sys.path.insert(1, os.path.join(sys.path[0], '../../../main'))


@allure.feature('Поддержка GRE Tunnel')
@allure.story('Валидация платформы')
def test_check_ver_platform():
    assert check_ver_platform(), "Firmware version lower than 2.5!"


