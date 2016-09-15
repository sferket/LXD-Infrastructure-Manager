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
from flask import Flask, render_template, jsonify
from app import LxdApi, SshApi
import sys
from config import Config

app = Flask(__name__)
config = {}

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

    return render_template(
        "home.html", 
        servers=config, 
        containers=containers, 
        server_info=server_info
    )


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
        }

    return config

if __name__ == "__main__":
    config = get_configuration()
    app.run(debug=True)

#@app.after_request
#def add_header(response):
#    response.headers["Cache-Control"] = "public, max-age=0"
#    return response
