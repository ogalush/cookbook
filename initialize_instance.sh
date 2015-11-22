#!/bin/bash

set -x
TARGET='192.168.0.107'

fab -f ./initialize_instance.py -H $TARGET init_ubuntu && \
chef exec knife zero bootstrap $TARGET --ssh-user ubuntu -i /home/ogalush/.ssh/id_rsa_chef --sudo --run-list 'recipe[base]' && \
fab -f ./initialize_instance.py -H $TARGET reboot
set +x
