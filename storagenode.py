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


######         externalMariadbnode   配置项说明      ###
# 外部MYSQL 访问地址;如果项目组希望使用第三方提供的mysql (或mariadb),可以在这个地方进行配置。
# 提供的ROOT 账号，必须具有创建DB，table ,user,为用户复权等权限；配置前最好手动验证账号权限

# mysqlhost：外部数据库 IP 地址 (必填项，按实际情况修改)
# mysqlport： 外部数据库端口 默认3306  (必填项，按实际情况修改)
#  mysqluser：  外部数据库账号 (用户名只能是root )
# mysqlpassword:  外部数据库root 账号密码  (必填项，按实际情况修改)

#如果需要配置请将下面的"#"注释去掉

#externalMariadbnode ={
#    'mysqlhost': '192.168.200.168',
#    'mysqlport': 3306,
#    'mysqluser': 'root',
#    'mysqlpassword': 'abc123',
#}

######      END      ###########



###    harborAddr  配置项说明      ###
### 内部Docker  镜像仓库地址 ###

#如果需要配置请将下面的"#"注释去掉

#harborAddr='registry.cn-hangzhou.aliyuncs.com'

####    END    ###