#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'transfervideo',
    'NFSAddr': None,
    'NFSBasePath': None,
    'TransferVideoLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'TransferVideoImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/transfer_video:v2',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'TransferVideoPrimaryDBHost': 'mariadb-svc',
    'TransferVideoPrimaryDBName': 'transfer',
    'TransferVideoPrimaryDBUser': 'transfer',
    "TransferVideoPrimaryDBPassword": None,

    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redisha/RedisHATool', 'apps.common.nacos/NacosTool',
                     'apps.common.zookeeper/ZookeeperTool','apps.common.kafka/KafkaTool',
                    'apps.bigdata.transferresourceai/TransferResourceAITool',
                    ]
}