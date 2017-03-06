# -*- coding: utf-8 -*-
#import eventlet
#eventlet.monkey_patch()
from flask_socketio import SocketIO
#from flask_socketio import emit
#from flask_socketio import join_room
#from flask_socketio import disconnect
from threading import Thread


class lxd_socketio(SocketIO):

    def __init__(self, app=None, **kwargs):
        super(lxd_socketio, self).__init__(app=None, **kwargs)
        #self.lxd_thread = None
        self.server_data = {"server_cpu_usage": {}}
        self.config = None
        self.label_ticker = 1

    def set_lxd_config(self, config):
        self.config = config

    def setup_thread(self):
        if not self.lxd_thread:
            self.lxd_thread = Thread(target=self.update_thread)
            self.lxd_thread.start()

    def update_thread():
        while True:
            time.sleep(5)
            self.server_data["server_cpu_usage"] = self._update_cpu_info()
            self.label_ticker += 1
            self.emit(
                "update_graph",
                {
                    "cpu_usage": self.server_data["server_cpu_usage"],
                },
                namespace="/update",
            )

    def _update_cpu_info(self):
        #TODO CLEAN UP!!
        for s in self.config:
            # get ip from endpoint
            server_ip = self.config[s]["endpoint"]
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
                self.server_cpu_usage[s] = {}

            data = cpu_api.get_cpu_load()
            total_cpu_usage = 0.0
            cpu_data = {}
            for d in data:
                cpu_data[d] = data[d]
                if 'data' in self.server_cpu_usage[s].keys():
                    if d in self.server_cpu_usage[s]["labels"].keys():
                        self.server_cpu_usage[s]["labels"][d].append(self.label_ticker)
                        self.server_cpu_usage[s]["data"][d].append(total_cpu_usage)
                    else:
                        self.server_cpu_usage[s]["labels"][d] = [self.label_ticker]
                        self.server_cpu_usage[s]["data"][d] = [total_cpu_usage]
                else:
                    self.server_cpu_usage[s]["labels"] = {}
                    self.server_cpu_usage[s]["data"] = {}
                    self.server_cpu_usage[s]["labels"][d] = [self.label_ticker]
                    self.server_cpu_usage[s]["data"][d] = [total_cpu_usage]

                # save max of 10 datapoints
                if len(self.server_cpu_usage[s]["data"][d]) > 10:
                    self.server_cpu_usage[s]["labels"][d].pop(0)
                    self.server_cpu_usage[s]["data"][d].pop(0)

            self.server_cpu_usage[s]["color"] = self.config[s]["rgba_color"]
        return server_cpu_usage
