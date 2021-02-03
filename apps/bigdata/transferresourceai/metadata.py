#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'transferresourceai',
    'NFSAddr': None,
    'NFSBasePath': None,
    'TransferResourceAILogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'TransferResourceAIImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/transfer-resource-ai-deploy:zmy-devops-v1.0.0.4',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'TransferResourceAIPrimaryDBHost': 'mariadb-svc',
    'TransferResourceAIPrimaryDBName': 'transfer',
    'TransferResourceAIPrimaryDBUser': 'transfer',
    "TransferResourceAIPrimaryDBPassword": None,

    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redisha/RedisHATool', 'apps.common.nacos/NacosTool',
                     'apps.common.zookeeper/ZookeeperTool','apps.common.kafka/KafkaTool',
                    ]
}