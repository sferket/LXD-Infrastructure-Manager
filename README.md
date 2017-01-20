# LXD-Infrastructure-Manager
Manager multiple physical LXD servers and the containers deployed on them

# Prepare LXD server
We tested on Ubuntu 16.04

apt-get update
apt-get install lxd
lxd init

Storage backend: dir			<== For easy testing, use ZFS for production
LXD over network: yes
Configure bridge automatically


Startup your first container on the host:
lxc launch ubuntu:16.04 sandbox-16
Get shell: lxc exec sandbox-16 -- /bin/bash

# Install LXD-Infrastructure-Manager
We advise to create a new virtualenv: virtualenv lxd
cd lxd
source bin/activate

git clone https://github.com/sferket/LXD-Infrastructure-Manager.git

cd LXD-Infrastructure-Manager
pip install -r requirements.txt


On LXD server:
Optionally,if not done during init:  Enable:
lxc config set core.https_address "[::]:8443"

For now we still need local accoutn to ssh to:
adduser lxd_panel
adduser lxd_panel lxd

Add certificatee to trust:
lxc config trust list
lxc config trust add /root/.config/lxc/client.crt
lxc config trust list

The required client certificates are stored in /root/.config/lxc
