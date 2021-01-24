#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'mediaresource',
    'NFSAddr': None,
    'NFSBasePath': None,
    'MediaResourceLogPath': None,
    'MediaResourceDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MediaResourceImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/media-resource:v2',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'MediaResourcePrimaryDBHost': 'mariadb-svc',
    'MediaResourcePrimaryDBName': 'media_resource',
    'MediaResourcePrimaryDBUser': 'media_resource',
    "MediaResourcePrimaryDBPassword": None,

    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,

    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.nacos/NacosTool',
                     'apps.common.zookeeper/ZookeeperTool','apps.common.kafka/KafkaTool',
                    'apps.common.redisha/RedisHATool',
                    ]
}