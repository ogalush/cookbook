#!/bin/bash

set -x
#TARGETHOST='192.168.0.200,192.168.0.210'
TARGETHOST='192.168.0.103'
#TARGETHOST='192.168.0.210'

fab -f ./initialize_instance.py -I -H $TARGETHOST init_ubuntu && \
fab -f ./initialize_instance.py -I -H $TARGETHOST update_pkg && \
fab -f ./initialize_instance.py -I --warn-only -H $TARGETHOST reboot && \
##chef exec knife zero bootstrap $TARGETHOST --ssh-user ubuntu -i /home/ogalush/.ssh/id_rsa_chef --sudo --run-list 'recipe[base]' && \

#-- Modify /etc/hosts
##fab -P -z 5 -f ./initialize_instance.py -H $TARGETHOST apply_hosts && \
set +x
