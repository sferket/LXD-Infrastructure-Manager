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
