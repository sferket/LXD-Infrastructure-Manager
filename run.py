from flask import Flask
from flask import render_template
from flask import jsonify
from flask import session
from flask import request
from flask import Response
from flask import make_response
from flask import Markup
from application.socket import lxd_socketio
from application.api import LxdApi
from application.api import SshApi
from application.api.servers import Servers
#from flask_socketio import SocketIO
from config import Config
 
import random
import pdb
import json

import time
print '444' 

from lxd_infrastructure_manager.hosts import Hosts
from lxd_infrastructure_manager.addons import Load

#hosts = Hosts()

#time.sleep(20)

print '-1.1'
app = Flask(__name__)
print '-1.2'
app.debug = True #TODO REMOVE FOR LIVE
print '-1.3'
app.config["SECRET_KEY"] = "UBeCeTW3TE5c24XecqLWGoRCBhdDKR" #TODO ACTUAL SECRET KEY
print '-1.3'
socketio = lxd_socketio()
print '-1.4'
lxd_api = LxdApi()
print '-1.5'
global config
print '-1.6'
thread = None
servers = None

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/flaskstatic/<path:path>')
def serve_partial(path):
    print '+++++++++++++++++Staitc'
    tst = '<div class="row bg_green">\
    <div class="col-md-12 center">\
        <h1 style="color:white;">LXD Control Panel [[controller]]</h1>\
    </div>\
    </div>'
    from flask import Markup

    #return render_template('/partial/{}'.format(path))
    tst = '<h1 style="color:white;">LXD Control Panel</h1>'
    #tst = 'test123'
    return render_template('directives/menu_servers_tmp.html', tst=Markup(tst))

@app.route('/renderedstatic/<type>/<file>')
def serve_static(type, file):
#     tst = '<div class="row bg_green">\
#     <div class="col-md-12 center">\
#         <h1 style="color:white;">LXD Control Panel [[controller]]</h1>\
#     </div>\
#     </div>'
    

    #return render_template('/partial/{}'.format(path))
    #tst = '<h1 style="color:white;">LXD Control Panel</h1>'
    #tst = 'test123'
    #return render_template('directives/%s' % file, tst=Markup(tst))
    return render_template('directives/%s' % file, sections=Markup(load.host_sections), buttons=Markup(load.host_buttons) )



@app.route("/get_info/")
def get_info_r():
    print 'CALLLLLL'
#     print '-request->%s' % request
#     print '-request->%s' % request.method
#     print request.args.get('host', '')
#     print request.args.get('container', '')
    
    containers = {}
#     containers['sandbox-16.lxd'] = {'test123' : {'name' : 't123', 'status' : 'Stopped'}
#                                     , 't456' : {'name' : 't456', 'status' : 'Stopped'} }
    #print 'ppppppppppp:%s' % containers 
#    for k,v in servers.get_display_info().iteritems():
#        print 'get_info(%s): %s' % (k,v) 

    #print '8888$>%s' % servers.get_display_info()['sandbox-16.lxd']['lxd_container_get']
    #print '9999$>%s' % servers.get_display_info()['sandbox-16.lxd']['lxd_snapshots_all']
    
    print request.args.get('checksumNodes', '')
    tree_checksum, tree_list = servers.get_tree_list(request.args.get('checksumNodes', ''))
    
    vals = {
        "servers": servers.get_display_info(),
        "containers": containers,
        "test": time.strftime("%H:%M:%S")
    }
    if tree_list:
        vals.update({"tree": tree_list})
        vals.update({"tree_checksum": tree_checksum})
        #vals.update({"tree_checksum": '123456'})
        print 'YYYYYYYYY:%s' % (tree_checksum)
    
    if request.args.get('host', ''):
        vals.update({"server_data" : servers.get_display_info()[request.args.get('host', '')]})

    if request.args.get('container', ''):
        for c in servers.get_display_info()[request.args.get('host', '')]['lxd.container_get']:
            if c.has_key(request.args.get('container', '')):
                vals.update({"container_data" : c.get(request.args.get('container', ''))})
    
    
    print 'ENDCALLLLL'
    return jsonify(vals)

@app.route("/container_cmd/", methods=["POST"])
def container_cmd_handler():
    print '-9->%s' % request
    if request.method == "POST":
        req_data = request.get_json()
        server = req_data.get("server")
        container = req_data.get("container")
        method = req_data.get("method")
        snap = req_data.get("snap")
        tar_name = '' or req_data.get("tar_name")
        if req_data.get("type") == "container":
            servers.exec_container_cmd(server, container, method, tar_name)
        elif req_data.get("type") == "snapshot":
            servers.exec_container_cmd(server, container, method, snap)

        #return xxx??
        
def get_container_info(server, container):
    print 'PPPPPPPPPPrint get_container_info'
    field_translations = {
        "name": "name",

    }
    for c in lxd_api.get_container_info(server):
        if c["name"] == container:
            return c

def update_thread():
#    global servers
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(5)
        count += 1
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
    print '1'
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    print '2'
    global config
    #config = _get_configuration()
    socketio.init_app(app)
    print '3'
    #socketio.set_lxd_config(config)
    #lxd_api.set_config(config)
# New
    global servers
    #servers = Servers(config)
    print '4'
    global load
    load = Load('/home/ferkets/git/LXD-Infrastructure-Manager/addons')
    load.inject_hosts_update_methods(Hosts)
    servers = Hosts()
    #servers.update_host_stats()
    
    servers.do_updates()
    print '5'
    #servers.execute_ssh_command()


if __name__ == "__main__":
    print '0.1'
    config_app()
    print '0.2'
    socketio.run(app, host='0.0.0.0')
    print '0.3'
