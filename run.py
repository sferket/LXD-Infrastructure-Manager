from flask import Flask
from flask import render_template
from flask import jsonify
from flask import session
from flask import request
from flask import Response
from flask import make_response
from application.socket import lxd_socketio
from application.api import LxdApi
from application.api import SshApi
from config import Config
import time
import random
import pdb


app = Flask(__name__)
app.debug = True #TODO REMOVE FOR LIVE
app.config["SECRET_KEY"] = "secret!" #TODO ACTUAL SECRET KEY
socketio = lxd_socketio()
lxd_api = LxdApi()
global config

@app.route("/")
def main():
    containers = {}
    for s in config:
        containers[s] = lxd_api.get_container_info(s)

    ssh = SshApi(config)
    server_info = {}
    for s in config:
        server_info[s] = ssh.get_server_info(s)

    vals = {
        "servers": config,
        "containers": containers,
        "server_info": server_info,
    }
    return render_template("index.html", **vals)

@app.route("/get_info/")
def get_info_r():
    containers = {}
    for s in config:
        containers[s] = lxd_api.get_container_info(s)

    ssh = SshApi(config)
    server_info = {}
    for s in config:
        server_info[s] = ssh.get_server_info(s)
    vals = {
        "servers": config,
        "containers": containers,
        "server_info": server_info,
    }
    return jsonify(vals)

@app.route("/container_cmd/", methods=["POST"])
def container_cmd_handler():
    if request.method == "POST":
        req_data = request.get_json()
        server = req_data.get("server")
        container = req_data.get("container")
        method = req_data.get("method")
        snap = req_data.get("snap")
        tar_snap = req_data.get("tar_snap")
        tar_cont = req_data.get("tar_cont")
        tar_prof = req_data.get("tar_prof")
        print "tar_prof: %s" % tar_prof
        if req_data.get("type") == "container":
            lxd_api.exec_container_cmd(server, container, method, tar_snap)
            # get update container info after method
            c_info = get_container_info(server, container)
            return make_response(jsonify(c_info))
        elif req_data.get("type") == "snapshot":
            lxd_api.exec_snapshot_cmd(server, snap, container, method, tar_cont, tar_prof)
            c_info = get_container_info(server, container)
            return make_response(jsonify(c_info))

def get_container_info(server, container):
    field_translations = {
        "name": "name",

    }
    for c in lxd_api.get_container_info(server):
        if c["name"] == container:
            return c

@socketio.on("connected", namespace="/update")
def got_event(msg):
    print "SocketIO connected!"

@app.after_request
def add_header(response):
    #TODO REMOVE FOR LIVE
    response.headers["Cache-Control"] = "public, max-age=0"
    return response

""" setup / run app """
def _get_configuration():
    f = file("server_cfg.cfg")
    cfg = Config(f)
    config = {}

    for server in cfg.servers:
        config[server.name] = {
            "servername": server.name,
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
            ),
            "excluded_containers": tuple(server.excluded_containers),
            "available_profiles": tuple(server.available_profiles)
        }
    return config

def config_app():
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    global config
    config = _get_configuration()
    socketio.init_app(app)
    socketio.set_lxd_config(config)
    lxd_api.set_config(config)

if __name__ == "__main__":
    config_app()
    socketio.run(app, host="0.0.0.0")
