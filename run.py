# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2016 - Open2bizz
#    Author: Open2bizz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of the GNU General Public License is available at:
#    <http://www.gnu.org/licenses/gpl.html>.
#
##############################################################################
#from gevent import monkey
#monkey.patch_all()
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, jsonify, session, request
from threading import Thread
from flask_socketio import SocketIO, emit, join_room ,disconnect
from app import LxdApi, SshApi, GetCpuLoad
import sys
from config import Config
import time
import random

import pdb

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
thread = None
config = {}

def update_thread():
    server_cpu_usage = {}
    label_ticker = 1
    while True:
        time.sleep(5)
        for s in config:
            # get ip from endpoint
            server_ip = config[s]["endpoint"]
            server_ip = server_ip.split(":")
            server_ip = server_ip[1]
            server_ip = server_ip.replace("//","")

            # get cpu usage
            cpu_api = GetCpuLoad(
                server_ip=server_ip,
                username=config[s]["username"],
                password=config[s]["password"],
            )

            if not s in server_cpu_usage.keys():
                # if new server
                server_cpu_usage[s] = {}

            data = cpu_api.get_cpu_load()
            print "data: %s" % data
            total_cpu_usage = 0.0
            cpu_data = {}
            for d in data:
                cpu_data[d] = data[d]
                if 'data' in server_cpu_usage[s].keys():
                    if d in server_cpu_usage[s]["labels"].keys():
                        server_cpu_usage[s]["labels"][d].append(label_ticker)
                        server_cpu_usage[s]["data"][d].append(total_cpu_usage)
                    else:
                        server_cpu_usage[s]["labels"][d] = [label_ticker]
                        server_cpu_usage[s]["data"][d] = [total_cpu_usage]
                else:
                    server_cpu_usage[s]["labels"] = {}
                    server_cpu_usage[s]["data"] = {}
                    server_cpu_usage[s]["labels"][d] = [label_ticker]
                    server_cpu_usage[s]["data"][d] = [total_cpu_usage]

                # save max of 10 datapoints
                if len(server_cpu_usage[s]["data"][d]) > 10:
                    server_cpu_usage[s]["labels"][d].pop(0)
                    server_cpu_usage[s]["data"][d].pop(0)

            server_cpu_usage[s]["color"] = config[s]["rgba_color"]

        label_ticker += 1
        print "server_cpu_usage: %s" % server_cpu_usage
        socketio.emit(
            "message",
            {"data": "This is data",
             "cpu_usage": server_cpu_usage},
            namespace="/update"
        )

@app.route("/")
def main():
    lxd = LxdApi(config)
    containers = {}
    for s in config:
        containers[s] = lxd.get_container_info(s)

    ssh = SshApi(config)
    server_info = {}
    for s in config:
        server_info[s] = ssh.get_server_info(s)

    global thread
    if thread is None:
        thread = Thread(target=update_thread)
        thread.start()

    return render_template(
        "home.html",
        servers=config,
        containers=containers,
        server_info=server_info
    )

@socketio.on("got event", namespace="/update")
def got_event(msg):
    print "msg['data']: %s" % msg['data']

@socketio.on("connect", namespace="/update")
def test_connect():
    emit("my response", {"data": "Connected", "count": 0})

@socketio.on("disconnect", namespace="/update")
def test_disconnect():
    print "Client disconnected"


@app.route("/cmd/<server>/<container>/<method>")
def cmd(server, container, method):
    lxd = LxdApi(config)
    lxd.exec_container_cmd(server, container, method)
    return ("",204)

@app.route("/update/container/info/")
def update_container_info():
    lxd = LxdApi(config)
    containers = {}
    for s in config:
        containers[s] = lxd.get_container_info(s)
    return jsonify(containers)

def get_configuration():
    f = file("server_cfg.cfg")
    cfg = Config(f)
    config = {}

    for server in cfg.servers:
        config[server.name] = {
            "username": server.username,
            "password": server.password,
            "endpoint": server.endpoint,
            "cert": (server.certfile,server.keyfile),
            "verify": server.verify,
            "keyfile": server.keyfile,
            "certfile": server.certfile,
            "rgba_color": "rgba(%s,%s,%s,1)" % (
                    random.randrange(255),
                    random.randrange(255),
                    random.randrange(255)
            )
        }
    return config

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "public, max-age=0"
    return response

if __name__ == "__main__":
    config = get_configuration()
    #app.run(debug=True)
    socketio.run(app)

