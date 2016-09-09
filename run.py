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
import app as api
import sys
from config import Config

app = Flask(__name__)
f = file("server_cfg.cfg")
cfg = Config(f)
servers = [server.name for server in cfg.servers]
uname = cfg.server_auth.username
s_pwd = cfg.server_auth.password


@app.route("/")
def main():
    containers = {}
    for s in servers:
        containers[s] = api.get_containers(s)

    server_info = {}
    for s in servers:
        server_info[s] = api.get_server_info(s, uname, s_pwd)

    return render_template(
        "home.html", 
        servers=servers, 
        containers=containers, 
        server_info=server_info
    )


@app.route("/cmd/<server>/<container>/<method>")
def cmd(server, container, method):
    api.container_cmd(server, container, method)
    return ("",204) 


@app.route("/update/container/info/")
def update_container_info():
    containers = {} 
    for s in servers:
        containers[s] = api.get_containers(s)
    return jsonify(containers)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


if __name__ == "__main__":
    app.run(debug=True)
