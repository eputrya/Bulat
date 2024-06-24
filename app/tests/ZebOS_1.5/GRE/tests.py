import os
import re
import sys

import allure
from flask import session

from app.helpers.utils import create_device

sys.path.insert(1, os.path.join(sys.path[0], '../../../main'))


def check_ver_platform():
    pattern = r"Platform\s+:\s+(\S+)"
    device_name = session.get('device_name')

    dut = create_device(device_name, session['ip_address'], session['username'], session['password'],
                        int(session['port']))
    print("Test №1", "Валидация платформы", sep='\n')

    try:
        dut.connect()

        with allure.step('Запрос версии'):
            text = dut.send_command('show version')

        match = re.search(pattern, text)

        if match:
            platform_version = match.group(1)
            print(f"Platform version: {platform_version}")
        else:
            print("No match found.")
            return False

        with allure.step('Ожидаемый результат: BS7510-48.'):
            if "BS7510-48" in platform_version:
                print(f'Platform is {platform_version}, it\'s ok!')
                print("")
                return True
            else:
                print(f"Version platform wrong - {platform_version}!")
                return False

    except ValueError as err:
        print(f"ValueError: {err}")
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        dut.disconnect()
