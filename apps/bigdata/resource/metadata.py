#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'resource',
    'NFSAddr': None,
    'NFSBasePath': None,
    'ResourceLogPath': None,
    'ResourceDataPath': None,
    'ResourceMediaDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'ResourceImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/resource:v6',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'ResourcePrimaryDBHost': 'mariadb-svc',
    'ResourcePrimaryDBName': 'mcb_dicttool',
    'ResourcePrimaryDBUser': 'mcbdicttool',
    "ResourcePrimaryDBPassword": None,

    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,

    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'ResourceMQHost': 'rabbitmq-svc',
    'ResourceMQPort': '5672',
    'ResourceMQUser': 'admin',
    'ResourceMQPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.nacos/NacosTool',
                    'apps.common.zookeeper/ZookeeperTool', 'apps.common.kafka/KafkaTool',
                     'apps.caibian.dicttool/DicttoolTool', 'apps.common.redisha/RedisHATool',
                    ]
}