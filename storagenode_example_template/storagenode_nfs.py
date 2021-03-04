#!/usr/bin/env python2
# -*- coding: utf-8 -*-


######         datastoragenode   配置项说明      ###
# NFS 数据存储节点，用于存放数据；提供的节点信息必须能够SSH 可达
# hostname: NFS 服务器 SSH IP 地址 (必填项，按实际情况修改)
# port:  NFS 服务器 SSH 端口 (必填项； SSH 端口默认是 22，如果非默认端口，按实际情况修改)
# username: NFS 服务器 SSH 用户名 (必填项； 工具运行过程中需要使用ROOT 权限，请使用ROOT 账号)
# password：  NFS 服务器 SSH root 账号密码 (必填项； 工具运行过程中需要使用ROOT 权限，请使用ROOT 账号密码)
#  baseurl:   NFS 服务挂载路径  （非必填项，不建议修改）
#   basepath:   非必填项，不建议修改
######      END      ###########


datastoragenode = {
    'type': 'nfs',
    'hostname':  '192.168.200.74',
    'port': 22,
    'username': 'root',
    'password': 'TempPass',
    'basepath': '/',
    'baseurl': '/TRS/DATA',
}



######         logstoragenode   配置项说明      ###
# NFS 数据存储节点，用于存放数据；提供的节点信息必须能够SSH 可达
# hostname: NFS 服务器 SSH IP 地址 (必填项，按实际情况修改)
# port:  NFS 服务器 SSH 端口 (必填项； SSH 端口默认是 22，如果非默认端口，按实际情况修改)
# username: NFS 服务器 SSH 用户名 (必填项； 工具运行过程中需要使用ROOT 权限，请使用ROOT 账号)
# password：  NFS 服务器 SSH root 账号密码 (必填项； 工具运行过程中需要使用ROOT 权限，请使用ROOT 账号密码)
#  baseurl:   NFS 服务挂载路径  （非必填项，不建议修改）
#   basepath:   非必填项，不建议修改
######      END      ###########

logstoragenode = {
    'type': 'nfs',
    'hostname':  '192.168.200.74',
    'port': 22,
    'username': 'root',
    'password': 'TempPass',
    'basepath': '/',
    'baseurl': '/TRS/LOG'
}




######         dynamicstoragenode   配置项说明      ###
#  NFS 数据存储节点，用于存放中间件数据（Redis,MongoDB,Elasticsearch,Kafka,Zookeeper,Nacos,Rabbitmq）；提供的节点信息必须能够SSH 可达
# hostname: NFS 服务器 SSH IP 地址 (必填项，按实际情况修改)
# port:  NFS 服务器 SSH 端口 (必填项； SSH 端口默认是 22，如果非默认端口，按实际情况修改)
# username: NFS 服务器 SSH 用户名 (必填项； 工具运行过程中需要使用ROOT 权限，请使用ROOT 账号)
# password：  NFS 服务器 SSH root 账号密码 (必填项； 工具运行过程中需要使用ROOT 权限，请使用ROOT 账号密码)
#  baseurl:   NFS 服务挂载路径  （非必填项，不建议修改）
#   basepath:   非必填项，不建议修改
######      END      ###########


dynamicstoragenode = {
    'type': 'nfs',
    'hostname':  '192.168.200.74',
    'port': 22,
    'username': 'root',
    'password': 'TempPass',
    'basepath': '/',
    'baseurl': '/TRS/DATA',
}



namespace = 'sly2'