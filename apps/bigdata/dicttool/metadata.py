#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'dicttool',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'DicttoolLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'DicttoolImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/dicttool:v2',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'DicttoolDBHost': 'mariadb-svc',
    'DicttoolDBName': 'mcb_dicttool',
    'DicttoolDBUser': 'mcbdicttool',
    "DicttoolDBPassword": None,
    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redisha/RedisHATool', 'apps.common.nacos/NacosTool',
                    'apps.common.zookeeper/ZookeeperTool', 'apps.common.kafka/KafkaTool'
                    ]
}