# -*- encoding: utf-8 -*-
from pylxd import client
from pylxd import exceptions
from pylxd import operation
from ws4py.client import WebSocketBaseClient
from ws4py.manager import WebSocketManager
import json
import time

m = WebSocketManager()


class _WebsocketClient(WebSocketBaseClient):
    """A basic websocket client for the LXD API.

    This client is intentionally barebones, and serves
    as a simple default. It simply connects and saves
    all json messages to a messages attribute, which can
    then be read are parsed.
    """

    def handshake_ok(self):
        m.add(self)

    def received_message(self, message):
        json_message = json.loads(message.data.decode('utf-8'))

def use_client(func):
    """ Decorator to connect to and from ev/ws clients """
    def func_wrapper(self, server, *args, **kwargs):
        s = self.config[server]
        ws_client = client.Client(
            endpoint=s.get("endpoint"),
            cert=s.get("cert"),
            verify=s.get("verify")
        )
        ev_client = ws_client.events(_WebsocketClient)
        ssl_options = {
            "keyfile": s.get("keyfile"),
            "certfile": s.get("certfile"),
        }

        ev_client.ssl_options=ssl_options
        ev_client.connect()
        kwargs.update({
            "ev_client": ev_client,
            "ws_client": ws_client,
        })
        res = func(self, server, *args, **kwargs)
        ev_client.close_connection()
        return res
    return func_wrapper

class LxdApi(object):

    def __init__(self):
        return

    def set_config(self, config):
        self.config = config

    @use_client
    def get_container_info(self, server, **kwargs):
        ws_client = kwargs["ws_client"]
        ws_client.api.operations[0]

        cont_names = []
        for cont in ws_client.containers.all():
            cont.fetch()
            data_dict = {
                "architecture": cont.architecture,
                "config": cont.config,
                "created_at": cont.created_at,
                "devices": cont.devices,
                "ephemeral": cont.ephemeral,
                "expanded_config": cont.expanded_config,
                "expanded_devices": cont.expanded_devices,
                "name": cont.name,
                "profiles": cont.profiles,
                "status": cont.status,
                "status_code": cont.status_code,
                "stateful": cont.stateful,
                "snapshots": self.get_snapshot_list(cont, cont.name)
               }
            cont_names.append(data_dict)
        return cont_names

    @use_client
    def exec_container_cmd(self, server, name, cmd, **kwargs):
        ws_client = kwargs["ws_client"]
        container = ws_client.containers.get(name)

        if cmd == "start":
            container.start()
        elif cmd == "stop":
            container.stop()
        elif cmd == "freeze":
            container.freeze()
        elif cmd == "unfreeze":
            container.unfreeze()
        elif cmd == "create_snapshot":
            res = self.create_snapshot(container, name)
        elif cmd == "get_snapshots":
            res = self.get_snapshot_list(container, name)
        elif cmd == "delete_snapshot":
            res = self.delete_snapshot(container, name, "snapname")

        return 0

    @use_client
    def exec_snapshot_cmd(self, server, snap, name, cmd, **kwargs):
        ws_client = kwargs["ws_client"]
        container = ws_client.containers.get(name)

        if cmd == "delete":
            res = self.delete_snapshot(container, name, snap)
        elif cmd == "activate":
            res = self.activate_snapshot(container, name, snap)

    def create_snapshot(self, container, c_name):
        try:
            snap_name = "%s_%s" % (c_name, time.strftime("%Y%m%d%H%M%S"))
            container.snapshots.create(snap_name)
            return "Finished creating snapshot"
        except Exception as e:
            return "Error creating snapshot: %s" % e

    def get_snapshot_list(self, container, c_name):
        try:
            names = []
            for c in container.snapshots.all():
                names.append(c.name)
            return names
        except Exception as e:
            return "Error getting snapshot list: %s" % e

    def activate_snapshot(self, container, c_name, s_name):
        try:
            container.execute([
                "copy",
                "%s/%s" % (c_name, s_name),
                s_name,
                "test123"
            ])
            return "Finished activating snapshot"
        except Exception as e:
            return "Error activating snapshot: %s" % e

    def delete_snapshot(self, container, c_name, s_name):
        try:
            for s in container.snapshots.all():
                if s.name == s_name:
                    s.delete()
            return "Deleted %s" % s_name
        except Exception as e:
            return "Error deleting snapshot: %s" % e
