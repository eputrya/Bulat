from flask import jsonify
from flask import session

from app.helpers.network_device import Trident


def create_device(device_name, ip_address, username, password, port):
    if device_name == 'ZebOS_1.5':
        return Trident(ip_address=ip_address, username=username, password=password, port=port)
    elif device_name == 'AnotherDevice':
        return None
    else:
        raise ValueError(f"Unknown device_name: {device_name}")


def execute_operation_on_device(operation_func):
    ip_address = session.get('ip_address')
    username = session.get('username')
    password = session.get('password')
    port = session.get('port')
    device_name = session.get('device_name')

    if not all([ip_address, username, password, port]):
        return jsonify({'status': 'error', 'message': 'Нет данных для подключения в сессии'}), 400

    try:
        device = create_device(device_name, ip_address, username, password, int(port))
        if not device:
            return jsonify({'status': 'error', 'message': 'Не удалось создать устройство'}), 400

        if not device.connect():
            return jsonify({'status': 'error', 'message': 'Не удалось подключиться к устройству'}), 400

        result = operation_func(device)
        device.disconnect()

        return result

    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
