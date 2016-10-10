#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import subprocess
from flask import Flask, jsonify, request, url_for, abort, Response

app = Flask(__name__)


@app.route('/api/commands', methods=['GET'])
def get_commands():
    response = jsonify({'results': get_command()})
    response.status_code = 200
    return response


@app.route('/api/commands/<key>', methods=['GET'])
def read_command(key):
    response = jsonify({'results': get_command(key)})
    response.status_code = 200
    return response


@app.route('/api/commands/<key>/run', methods=['GET'])
def run_command(key):
    cmd = get_command(key)
    cmd_str = cmd['command']
    return_code, stdout_data, stderr_data = run_command(cmd_str)
    retjs = [{'returncd': return_code, 'command': cmd_str, 'stdout': stdout_data, 'stderr': stderr_data}]
    response = {'results': retjs}
    response.status_code = 200
    return response


# process実行
def run_command(cmd_str):
    p = subprocess.Popen(cmd_str.split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    print(p.returncode)
    return p.returncode, stdout_data, stderr_data


# モデル操作
def get_command(key=None):
    data = read_file()
    if key is None:
        return data;
    if key in data:
        return data[key]
    else:
        return {}


# JSONアクセス
def read_file():
    BASE_DIR = os.path.dirname(__file__)
    file_name = 'static/commands/commands.json'
    try:
        with open(os.path.join(BASE_DIR, file_name), 'r') as f:
            return json.load(f)
    except IOError as e:
        print(e)
        return None


if __name__ == '__main__':
    app.run(host='0.0.0.0')
