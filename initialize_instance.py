from fabric.api import *
import getpass

#-- Execute CommandLine.
## fab -P -z 5 -f update_pkg.py update_pkg

#--Def
##env.hosts = ['www.teamlush.biz']
#-- need password for parallel execute.
#-- http://blog.masu-mi.me/2015/04/11/fabric_tips.html
#env.use_ssh_config = true
#env.key_filename = "~/.ssh/id_rsa"
##env.password = getpass.getpass('Enter the sudo password: ')
env.connection_attempts=3
env.timeout=30
#--Def(END)


##==================================
# install chefdk(local)
##==================================
@parallel(pool_size=5)
def install_chefdk():
  #-- create ssh-key(No Passphrase)
  run('ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa_chef')
  #-- install chefdk
  sudo('dpkg -l |grep chefdk || dpkg -i /usr/local/src/chefdk_1.0.3-1_amd64.deb', pty=False)
  run('chef --help')
  sudo('chef gem install knife-zero', pty=False)

##==================================
# initialize nova instance (ubuntu)
##==================================
##@parallel(pool_size=5)
def init_ubuntu():
  #-- initialize
  env.user='ubuntu'
  env.key_filename = '~/.ssh/id_rsa_chef'
  local('ssh-keygen -f ~/.ssh/known_hosts -R '+ env.host)

  #-- Repair dpkg
  sudo('sudo dpkg --configure -a')
  sudo('sudo dpkg-reconfigure openssh-server', pty=False)
  #-- for ubuntu16.04
  sudo('sudo timedatectl set-timezone Asia/Tokyo', pty=False)
  run('date')
  #-- for ubuntu16.04(END)
## for ubuntu14.04
##  sudo('echo Asia/Tokyo | tee /etc/timezone', pty=False)
##  sudo('dpkg-reconfigure --frontend noninteractive tzdata', pty=False)
##  run('date')
## for ubuntu14.04(END)
  sudo('sed -i "s/UTC=yes/UTC=no/g" /etc/default/rcS')
  sudo('apt-get -y install ruby', pty=False)
  put('/usr/local/src/chefdk_1.0.3-1_amd64.deb','/tmp/')
  sudo('dpkg -l |grep chefdk || dpkg -i /tmp/chefdk_1.0.3-1_amd64.deb', pty=False)
  run('chef --help')
  sudo('chef gem install knife-zero', pty=False)
  local('chef exec knife zero bootstrap '+ env.host +' --ssh-user ubuntu -i ~/.ssh/id_rsa_chef --sudo --run-list "recipe[base]"')
  update_pkg()

@parallel(pool_size=5)
def update_pkg():
  sudo('apt-get -y update', pty=False)
  sudo('apt-get -y upgrade', pty=False)
  sudo('apt-get -y dist-upgrade', pty=False)
  sudo('apt-get -y autoremove', pty=False)

def reboot():
  sudo('shutdown -r now', pty=False)

##==================================
# apply /etc/hosts for cdh
##==================================
##@parallel(pool_size=5)
def apply_hosts():
  env.user='ubuntu'
  env.key_filename = '~/.ssh/id_rsa_chef'
  put('hosts_cdh.txt', '/tmp/hosts')
  sudo('cp /tmp/hosts /etc/hosts')
  run('cat /etc/hosts')
