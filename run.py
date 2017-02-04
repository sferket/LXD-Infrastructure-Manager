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
from application.api.servers import Servers
#from flask_socketio import SocketIO

from config import Config
import time
import random
import pdb
import json


app = Flask(__name__)
app.debug = True #TODO REMOVE FOR LIVE
app.config["SECRET_KEY"] = "secret!" #TODO ACTUAL SECRET KEY
socketio = lxd_socketio()
lxd_api = LxdApi()
global config
thread = None
servers = None

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get_info/")
def get_info_r():
    containers = {}

    containers = servers.get_containers()
    
    vals = {
        "servers": servers.get_display_info(),
        "containers": containers,
    }
    return jsonify(vals)

@app.route("/default_name/")
def get_default_name_r():
    containers = {}

    containers = servers.get_containers()
    
    vals = {
        "servers": servers.get_display_info(),
        "containers": containers,
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
        tar_name = '' or req_data.get("tar_name")
        if req_data.get("type") == "container":
            if method == 'refresh':
                servers.get(server).refresh_container_info() #.refresh_container_info()
            lxd_api.exec_container_cmd(server, container, method, tar_name)
        elif req_data.get("type") == "snapshot":
            lxd_api.exec_snapshot_cmd(server, snap, container, method)


def update_thread():
#    global servers
    """Example of how to send server generated events to clients."""
    while True:
        if servers.get_client_update().wait(60):
            servers.get_client_update().clear()

        mes = {}
        if servers:
            for s in servers.get():
                mes.update({s : servers.get(s).get_info()})
            mes = json.dumps(mes)
             
            socketio.emit('my_response',
                           mes,
                          namespace='/update')
        
@socketio.on("connected", namespace="/update")
def got_event(msg):
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=update_thread)
    socketio.emit('my_response', {'data': 'Connected', 'count': 0})

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
# New
    global servers
    servers = Servers(config)

if __name__ == "__main__":
    config_app()
    #socketio.run(app, use_reloader=False)
    socketio.run(app)
