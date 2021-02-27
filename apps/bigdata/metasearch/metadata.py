#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'metasearch',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'MetaSearchLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MetaSearchImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/metasearch:v2',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'MetaSearchPrimaryDBHost': 'mariadb-svc',
    'MetaSearchPrimaryDBName': 'mcb_metasearch',
    'MetaSearchPrimaryDBUser': 'mcbmetasearch',
    "MetaSearchPrimaryDBPassword": None,

    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,

    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redisha/RedisHATool', 'apps.common.nacos/NacosTool',
                     'apps.common.zookeeper/ZookeeperTool','apps.common.kafka/KafkaTool',
                    ]
}