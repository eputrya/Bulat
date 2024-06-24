import logging
import time

from flask import session
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

from app.models.Config import Config
from app.models.Tickets import Tickets


class NetworkDevice:
    def \
            __init__(self, ip_address: str, device_type: str, username: str, password: str, port: int):
        self.ip_address = ip_address
        self.device_type = device_type
        self.username = username
        self.password = password
        self.port = port
        self.connection = None

    def connect(self) -> bool:
        device_params = {
            'device_type': f"{self.device_type}_telnet",
            'host': self.ip_address,
            'username': self.username,
            'password': self.password,
            'port': self.port
        }

        try:
            self.connection = ConnectHandler(**device_params)
            logging.info(f"Successfully connected to device with IP address {self.ip_address} on port {self.port}")
            return True
        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            logging.error(f"Connection error to {self.ip_address} on port {self.port}: {e}")
        except Exception as e:
            logging.error(f"Unknown error while connecting to {self.ip_address} on port {self.port}: {e}")

        self.connection = None
        return False

    def disconnect(self) -> None:
        if self.connection:
            self.connection.disconnect()
            logging.info(f"Disconnected from device with IP address {self.ip_address}")
        else:
            logging.info(f"No active connection to device with IP address {self.ip_address}")

    def send_command(self, command: str, expect_string=None) -> str:
        if not self.connection:
            logging.error("No active connection. Please connect first.")
            return ""

        try:
            output = self.connection.send_command(command, expect_string=expect_string)
            logging.info(f"Command '{command}' executed successfully:\n{output}")
            return output
        except Exception as e:
            logging.error(f"Error executing command '{command}': {e}")
            return ""

    def check_connect(self) -> dict:
        if self.connect():
            message = f'Successfully connected to {self.ip_address}'
            status = 'success'
        else:
            message = f'Failed to connect to {self.ip_address}'
            status = 'error'

        self.disconnect()
        return {'status': status, 'message': message}

    def load_configuration_to_device(self, config_lines: list) -> bool:
        if not self.connection:
            logging.error("No active connection. Please connect first.")
            return False

        try:
            for command in config_lines:
                self.connection.send_command(command)
                time.sleep(2)
            logging.info(f"Configuration successfully loaded to device with IP address {self.ip_address}")
            return True
        except Exception as e:
            logging.error(f"Error loading configuration to {self.ip_address}: {e}")
            return False

    def get_device_config(self) -> bool:
        test_name = session.get('test_name')
        device_name = session.get('device_name')

        if not test_name or not device_name:
            logging.error("Test name or device name not found in session.")
            return False

        test = Tickets.query.filter_by(id=test_name).first()
        if not test:
            logging.error(f"Test with name '{test_name}' not found.")
            return False

        config = Config.query.filter_by(test_id=test.id, device_name=device_name).first()
        if not config:
            logging.error(f"Config for device '{device_name}' in test '{test_name}' not found.")
            return False

        config_lines = config.config.split('\n')
        return self.load_configuration_to_device(config_lines)


class Trident(NetworkDevice):
    def __init__(self, ip_address, username, password, port: int):
        super().__init__(ip_address, "cisco_ios", username, password, port)

    def reboot(self):
        pass

    def get_software_version(self):
        if self.connection:
            version = self.send_command("show version")
            logging.info(f"Software version of the switch with IP address {self.ip_address}:\n{version}")
            return version
        logging.error("No active connection. Please connect first.")
        return ""

    def get_running_config(self):
        if self.connection:
            config = self.send_command("show run")
            logging.info(f"Running configuration of the switch with IP address {self.ip_address}:\n{config}")
            return config
        logging.error("No active connection. Please connect first.")
        return ""

    def load_configuration_to_device(self, config_lines: list) -> bool:
        if not self.connection:
            logging.error("No active connection. Please connect first.")
            return False

        try:
            for command in config_lines:
                output = self.send_command(command, expect_string="DUT")
                logging.info(f"Command '{command}' executed successfully:\n{output}")
                time.sleep(2)
            logging.info(f"Configuration successfully loaded to device with IP address {self.ip_address}")
            return True
        except Exception as e:
            logging.error(f"Error loading configuration to {self.ip_address}: {e}")
            return False

    def copy_default_config(self):
        if not self.connection:
            logging.error("No active connection. Please connect first.")
            return False
        try:
            self.connection.send_command("enable", expect_string="DUT")
            output = self.connection.send_command('copy empty-config startup-config')
            logging.info(f"Command 'copy empty-config startup-config' executed successfully:\n{output}")
            self.connection.send_command("reload", expect_string="reboot system", read_timeout=.5)
            self.connection.send_command("y", expect_string="")
            logging.info("Reboot command sent. Please wait, the device is rebooting...")
            time.sleep(110)
            retries = 3
            for _ in range(retries):
                if self.connection.is_alive():
                    logging.info("Device successfully rebooted.")
                    return True
                logging.info("Waiting completed, but device is not accessible. Trying again...")
                time.sleep(10)
            return True
        except Exception as e:
            logging.error(f"Error copying configuration and rebooting device with IP address {self.ip_address}: {e}")
            return False
