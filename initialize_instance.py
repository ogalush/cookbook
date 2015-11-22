from fabric.api import *
import getpass

#-- Execute CommandLine.
## fab -P -z 5 -f update_pkg.py update_pkg

#--Def
##env.hosts = ['www.teamlush.biz']
#-- need password for parallel execute.
#-- http://blog.masu-mi.me/2015/04/11/fabric_tips.html
env.password = getpass.getpass('Enter the sudo password: ')

#env.use_ssh_config = true
#env.key_filename = "~/.ssh/id_rsa"
#--Def(END)


##==================================
# install chefdk(local)
##==================================
def install_chefdk():
  #-- create ssh-key(No Passphrase)
  run('ssh-keygen -t rsa -b 4096 -N '' -f /home/ogalush/.ssh/id_rsa_chef')
  #-- install chefdk
  sudo('dpkg -l |grep chefdk || dpkg -i /usr/local/src/chefdk_0.10.0-1_amd64.deb', pty=False)
  run('chef --help')
  sudo('chef gem install knife-zero', pty=False)

##==================================
# initialize nova instance (ubuntu)
##==================================
@parallel(pool_size=5)
def init_ubuntu():
  env.user='ubuntu'
  env.key_filename = '~/.ssh/id_rsa_chef'
  local('rm -f ~/.ssh/known_hosts')
  sudo('sudo dpkg-reconfigure openssh-server', pty=False)
  sudo('cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime', pty=False)
  run('date')
  sudo('apt-get -y install ruby', pty=False)
  sudo('sed -i".bak" -e \'s/\/\/nova.clouds.archive.ubuntu.com/\/\/ftp.jaist.ac.jp/g\'  /etc/apt/sources.list', pty=False)
  put('/usr/local/src/chefdk_0.10.0-1_amd64.deb','/tmp/')
  sudo('dpkg -l |grep chefdk || dpkg -i /tmp/chefdk_0.10.0-1_amd64.deb', pty=False)
  run('chef --help')
  sudo('chef gem install knife-zero', pty=False)
  update_pkg()

@parallel(pool_size=5)
def update_pkg():
  sudo('cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime', pty=False)
  sudo('apt-get -y update', pty=False)
  sudo('apt-get -y upgrade', pty=False)
  sudo('apt-get -y dist-upgrade', pty=False)
  sudo('apt-get -y autoremove', pty=False)

def reboot():
  run('hostname')
  sudo('shutdown -r now', pty=False)
