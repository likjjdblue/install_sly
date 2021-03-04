#!/usr/bin/env python2
# -*- coding: utf-8 -*-

######         datastoragenode   配置项说明      ###
# NAS 数据存储节点，用于存放数据；提供的NAS 只能是以NFS 方式访问（块存储方式，目前不支持）
# hostname: NAS 访问IP 地址 (必填项，按实际情况修改)
# baseurl: NAS 访问URL （必填项，按实际情况修改）
# basepath:  程序内部地址   （非必填项，不建议修改）
######      END      ###########


datastoragenode = {
    'type': 'nas',
    'hostname':  '192.168.200.66',
    'basepath': '/TRS/DATA',
    'baseurl': '/volume1/NFS',
}



######         logstoragenode   配置项说明      ###
# NAS 日志存储节点，用于存放日志；提供的NAS 只能是以NFS 方式访问（块存储方式，目前不支持）
# hostname: NAS 访问IP 地址 (必填项，按实际情况修改)
# baseurl: NAS 访问URL （必填项，按实际情况修改）
# basepath:  程序内部地址   （非必填项，不建议修改）
######      END      ###########



logstoragenode = {
    'type': 'nas',
    'hostname':  '192.168.200.66',
    'basepath': '/TRS/LOG',
    'baseurl': '/volume1/NFS2'
}


######         dynamicstoragenode   配置项说明      ###
# NAS 数据存储节点，用于存放中间件数据（Redis,MongoDB,Elasticsearch,Kafka,Zookeeper,Nacos,Rabbitmq）；提供的NAS 只能是以NFS 方式访问（块存储方式，目前不支持）
# hostname: NAS 访问IP 地址 (必填项，按实际情况修改)
# baseurl: NAS 访问URL （必填项，按实际情况修改）
# basepath:  程序内部地址   （非必填项，不建议修改）
######      END      ###########

dynamicstoragenode = {
    'type': 'nas',
    'hostname':  '192.168.200.74',
    'basepath': '/TRS/DATA',
    'baseurl': '/home/tmp_nfs_storage'
}


namespace = 'sly2'
