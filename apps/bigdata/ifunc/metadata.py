#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'ifunc',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'iFuncLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'iFuncImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/transfer-ifuncun-deploy:zmy-devops-v1.0.0.7',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'iFuncPrimaryDBHost': 'mariadb-svc',
    'iFuncPrimaryDBName': 'mcb_metasearch',
    'iFuncPrimaryDBUser': 'mcbmetasearch',
    "iFuncPrimaryDBPassword": None,


    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redisha/RedisHATool', 'apps.common.nacos/NacosTool',
                     'apps.common.zookeeper/ZookeeperTool','apps.common.kafka/KafkaTool',
                    ]
}