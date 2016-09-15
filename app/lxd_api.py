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
from pylxd import client, exceptions
from pylxd import operation
from ws4py.client import WebSocketBaseClient
from ws4py.manager import WebSocketManager
import json

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


class LxdApi(object):
    def __init__(self, config):
        self.config = config

    def get_container_info(self, server):
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
               } 
            cont_names.append(data_dict)

        ev_client.close_connection()
        return cont_names

    def exec_container_cmd(self, server, name, cmd):
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
        container = ws_client.containers.get(name)

        if cmd == "start":
            container.start()
        elif cmd == "stop":
            container.stop()
        elif cmd == "freeze":
            container.freeze()
        elif cmd == "unfreeze":
            container.unfreeze()

        ev_client.close_connection()
        return 0 
