#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import operator
import flask
from flask import Flask, jsonify, request, url_for, abort, Response

app = Flask(__name__)


@app.route('/')
def show_commands():
    commands = get_command()
    categories = get_categories_with_commands(commands)
    return flask.render_template('index.html', categories=categories)


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
    #retjs = json.dumps({'returncd': return_code, 'command': cmd_str, 'stdout': stdout_data, 'stderr': stderr_data})
    response = jsonify({'results': {'returncd': return_code, 'command': cmd_str, 'stdout': stdout_data, 'stderr': stderr_data}})
    response.status_code = 200
    return response


# process実行
def run_command(cmd_str):
    p = subprocess.Popen(cmd_str.split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    return p.returncode, str(stdout_data, encoding='utf-8'), str(stderr_data, encoding='utf-8')


# モデル操作
def get_command(key=None):
    data = read_file()
    if key is None:
        return data
    if key in data:
        return data[key]
    else:
        return {}


def get_categories_with_commands(commands):
    category_names = []
    for command in commands.values():
        if command['category'] not in category_names:
            category_names.append(command['category'])

    categories = []
    for category_name in category_names:
        commands_tmp = {}
        for key, command in commands.items():
            if command['category'] == category_name:
                commands_tmp[key] = command
        categories.append({'name': category_name, 'commands': commands_tmp})

    return categories


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
