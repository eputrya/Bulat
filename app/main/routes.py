import logging
import os
import subprocess

import pytest
from flask import render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory
from flask_login import login_user, logout_user

from app.helpers.network_device import NetworkDevice
from app.helpers.unit import Unit
from app.helpers.utils import create_device, execute_operation_on_device
from app.main import bp
from app.models.Config import Config
from app.models.Tickets import Tickets
from app.models.User import User

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
ALLURE_REPORT_DIR = os.path.join(BASE_DIR, 'allure_report')
REPORT_DIRECTORY = os.path.join(BASE_DIR, 'report_directory')


@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.devices'))
    return render_template('index.html')


@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@bp.route('/devices')
def devices():
    return render_template('devices.html')


@bp.route('/start_test', methods=['GET', 'POST'])
def start_test():
    return render_template('run.html')


@bp.route('/check_connect', methods=['POST'])
def check_connect():
    data = request.values
    device = NetworkDevice(
        ip_address=data.get('ip'),
        device_type='cisco_ios',
        username=data.get('login'),
        password=data.get('password'),
        port=int(data.get('port'))
    )
    result = device.check_connect()

    if result['status'] == 'success':
        session['ip_address'] = data.get('ip')
        session['username'] = data.get('login')
        session['password'] = data.get('password')
        session['port'] = data.get('port')
        return jsonify(result), 200
    else:
        session.pop('ip_address', None)
        session.pop('username', None)
        session.pop('password', None)
        session.pop('port', None)
        return jsonify(result), 400


@bp.route('/show_running_config', methods=['POST'])
def show_running_config():
    def get_running_config(device):
        config = device.get_running_config()
        if config:
            return jsonify({'status': 'success', 'config': config}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Не удалось получить конфигурацию'}), 400

    return execute_operation_on_device(get_running_config)


@bp.route('/show_version', methods=['POST'])
def show_version():
    def get_software_version(device):
        version = device.get_software_version()
        if version:
            return jsonify({'status': 'success', 'version': version}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Не удалось получить версию ПО'}), 400

    return execute_operation_on_device(get_software_version)


@bp.route('/selection_of_the_test/<device_name>', methods=['GET', 'POST'])
def selection_of_the_test(device_name):
    session['device_name'] = device_name
    session['test_id'] = request.form.get('test')
    if request.method == "POST":
        test = Unit.get_unit(int(request.form.get('test')))
        return render_template('run.html', name=test.name, img=test.img, des=test.description, conf=test.configuration)
    return render_template('all-tests.html')


@bp.route('/upload_config', methods=['POST'])
def upload_config():
    test_name = session.get('test_id')
    device_name = session.get('device_name')

    if not test_name or not device_name:
        return jsonify({'status': 'error', 'message': 'Test name or device name not found in session.'}), 400

    test = Tickets.query.filter_by(id=test_name).first()
    if not test:
        return jsonify({'status': 'error', 'message': f"Test with ID '{test_name}' not found."}), 404

    config = Config.query.filter_by(test_id=test.id, device_name=device_name).first()
    if not config:
        return jsonify(
            {'status': 'error', 'message': f"Config for device '{device_name}' in test '{test_name}' not found."}), 404

    device = create_device(device_name, session['ip_address'], session['username'], session['password'],
                           int(session['port']))

    if device.connect():
        if device.load_configuration_to_device(config.config.split('\n')):
            print(config.config.split('\n'))
            return jsonify({'status': 'success', 'message': 'Configuration uploaded successfully.'}), 200
        else:
            device.disconnect()
            return jsonify({'status': 'error', 'message': 'Failed to upload configuration.'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Failed to connect to device.'}), 500


@bp.route('/start', methods=['POST'])
def start():
    try:
        result = pytest.main(
            [
                f"--alluredir={ALLURE_REPORT_DIR}",
                os.path.join(BASE_DIR, 'tests', 'ZebOS_1.5', 'GRE', 'test_check.py')

            ]
        )

        if result == 0:
            message = 'All tests completed successfully.'
            subprocess.run(['allure', 'generate', ALLURE_REPORT_DIR, '-o', REPORT_DIRECTORY, '--clean'], check=True)
        else:
            message = 'Some tests failed.'
            subprocess.run(['allure', 'generate', ALLURE_REPORT_DIR, '-o', REPORT_DIRECTORY, '--clean'], check=True)

        return jsonify({'status': 'success', 'message': message}), 200
    except subprocess.CalledProcessError as e:
        logging.error(f"Error generating Allure report: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while generating the Allure report.'}), 500
    except Exception as e:
        logging.error(f"Error running tests: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while running the tests.'}), 500


@bp.route('/copy_default_config', methods=['POST'])
def copy_default_config():
    device_name = session.get('device_name')

    if not device_name:
        return jsonify({'status': 'error', 'message': 'Device name not found in session.'}), 400

    device = create_device(device_name, session['ip_address'], session['username'], session['password'],
                           int(session['port']))

    if device.connect():
        try:
            success = device.copy_default_config()
            if success:
                return jsonify({'status': 'success',
                                'message': 'Default configuration copied and device rebooted successfully.'}), 200
            else:
                return jsonify(
                    {'status': 'error', 'message': 'Failed to copy default configuration and reboot device.'}), 500
        except Exception as e:
            logging.error(f"Error copying default configuration to device {device.ip_address}: {e}")
            return jsonify({'status': 'error', 'message': f"Error copying default configuration: {str(e)}"}), 500
        finally:
            device.disconnect()
    else:
        return jsonify({'status': 'error', 'message': 'Failed to connect to device.'}), 500


@bp.route('/report_directory/<path:path>')
def serve_report(path):
    return send_from_directory('report_directory', path)


@bp.route('/check_report')
def check_report():
    report_path = os.path.join(REPORT_DIRECTORY, 'index.html')
    if os.path.exists(report_path):
        return jsonify({'exists': True}), 200
    else:
        return jsonify({'exists': False}), 404
