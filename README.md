# Motivation
The main motivation was that we could not find a GUI to manage multiple LXD servers. 
We wanted to be able to:
- Manage containers on multiple LXD servers
- View statistict of the physical LXD server
- View statistics of the containers

# Preview
![Alt text](/screenshots/screenshot1.png?raw=true "Overview")

# Installation
## Prepare LXD server(s)
We tested on Ubuntu 16.04
Do these steps to install a basic LXD server:
- sudo apt-get update
- sudo apt-get install lxd
- sudo lxd init
- Storage backend: dir			<== For easy testing, use ZFS for production
- LXD over network: yes
- Configure bridge automatically


Startup your first container on the host:
lxc launch ubuntu:16.04 sandbox-16
Get shell: lxc exec sandbox-16 -- /bin/bash

## Install LXD-Infrastructure-Manager
This can be a stand-alone server or even a container on one the the LXD hosts
We advise to create a new virtualenv: 
- virtualenv lxd
- cd lxd
- source bin/activate
- git clone https://github.com/sferket/LXD-Infrastructure-Manager.git
- cd LXD-Infrastructure-Manager
- pip install -r requirements.txt

## Prepare LXD server for remote connections
On LXD server:
Optionally,if not done during init:  Enable:
- lxc config 
- set core.https_address "[::]:8443"

For now we still need local account to ssh to:
- sudo adduser lxd_panel
- sudo adduser lxd_panel lxd

Add certificatee to trust:
- sudo lxc config trust list
- sudo lxc config trust add /root/.config/lxc/client.crt
- sudo lxc config trust list

The required client certificates are stored in /root/.config/lxc


# License
licensed under LGPL version 3 (also known as LGPLv3). See also the GPL FAQ and the compatibility matrix.
