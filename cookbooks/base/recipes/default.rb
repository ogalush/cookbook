#
# Cookbook Name:: base
# Recipe:: default
#
# Copyright 2015, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

#-- OSUser
#-- https://docs.chef.io/resource_group.html
#-- https://docs.chef.io/resource_user.html
group 'ogalush' do
  action :create
  gid      '1010'
  append true
end

group 'tendo' do
  action :create
  gid      '1011'
  append true
end

user 'ogalush' do
  home     '/home/ogalush'
  shell    '/bin/bash'
  uid      1010
  gid      1010
  password '$6$testtest$5txpZMim8XzgmQ8V0DPQvomReE6CJRHfSQ1gSkhAlsWTqRGY.MqHAVNkW8dc6LbPAZLsiXxl4Ju59YUvCrBen1'
  supports :manage_home => true
end

user 'tendo' do
  home     '/home/tendo'
  shell    '/bin/bash'
  uid      1011
  gid      1011
  password '$6$testtest$ZhkCNjAyGvDSaqAuzScAS5EWblP.MikFo1hoGHPbRmMujFTu6o1LT3MezAnb.BP4TXl11qUaKKkYeWT671lQq0'
  supports :manage_home => true
end

#-- authorized_keys
keys = {}
keys['ogalush'] = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7TBVieOcYJC3KQZLwzWQuvBvECqSCqPBjPauB09qRBDQiRYFJ3V1AfhoPAfM2yiXpWtugzF5rppFyNtL5BgnDNqRds1ETTxh5GyNxdpNZZ/SU9Taj6k1HemRBz4dTFCMrAA9Y2uktVx1YErV44jgi9KFdOwFpMxu4pyalFKQ4+qzbTYu9q7ucxa0zVbqKozSW/orww6ej6tYMgsybHhliEzO7ucecB0hhKjeSxjgVEAsRDjqN8zesKpgnTVLnmoBLAL3RWAOLJoOL4Svz1q8akXLuSgSqRniynN/I9nA12R8LYdQVo8RJzsQCIVuIdmm3nZgOoLL+bcfC3Uwaezf9 ogalush@kinder'
keys['tendo']  = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQChznMEbcIbUY5soThwWLhpTVZdUCNf6AFrbWuoh7dbLxwHvS+OAkm8FmZpHuvNQhPViVKT+jvr5ytfi2iGF9vfmIZGDuM847UYvmMdTh6pP3PeNnMDkO/FpzB6OcFGU9VdF+2qkjOxyqdxLYaJ0ckeqQkEbSfAOjmrXCNUcBb5g3kgWh4JFpTHF7Ao1c12eRnomy9XjgBVMqyl3qjXLk/2GLtI59jztIhRxPeGSPVYiuiNmmITe5rOq6kHJQzFkTIIdvjOdSf6rZt/0Ab2LK6BeDtJUNH7YfILL6frCQMeM0yC4jLjmyeLFOM3E3I0SMJTKy46dzn2x6lMMxL8TO+v endo.tadshi3@gmail.com'

%w{ogalush tendo}.each do |user|
    directory "/home/#{user}/.ssh" do
      owner user
      group user
      mode 0700
      action :create
    end

    file "/home/#{user}/.ssh/authorized_keys" do
      content keys[user]
      owner user
      group user
    end

    file "/home/#{user}/.vimrc" do
      content ':set number'
      owner user
      group user
    end
end


#-- OSGroup(初期ユーザの権限を開発ユーザ全てに付与
%w{adm sudo}.each do |gname|
  group gname do 
    members ['ogalush', 'tendo']
    action :create
    append true
  end
end

#-- Development tools
%w{ntp zsh traceroute automake make whois git cpufreqd cpufrequtils sysstat}.each do |pkg|
  package pkg do 
    action :install
  end
end
