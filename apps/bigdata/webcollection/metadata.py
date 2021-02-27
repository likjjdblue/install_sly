#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'webcollection',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'WebCollectionLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'WebCollectionImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/webcollection:v4',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'WebCollectionPrimaryDBHost': 'mariadb-svc',
    'WebCollectionPrimaryDBName': 'websitecollection',
    'WebCollectionPrimaryDBUser': 'websitecollection',
    "WebCollectionPrimaryDBPassword": None,

    'WebCollectionSecondDBHost': 'mariadb-svc',
    'WebCollectionSecondDBName': 'mcb_dicttool',
    'WebCollectionSecondDBUser': 'mcbdicttool',
    "WebCollectionSecondDBPassword": None,

    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,

    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'WebCollectionMQHost': 'rabbitmq-svc',
    'WebCollectionMQPort': '5672',
    'WebCollectionMQUser': 'admin',
    'WebCollectionMQPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                     'apps.common.nacos/NacosTool','apps.common.redisha/RedisHATool',
                    'apps.common.zookeeper/ZookeeperTool','apps.common.kafka/KafkaTool',
                    'apps.bigdata.dicttool/DicttoolTool',
                    ]
}