#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'datagather',
    'NFSAddr': None,
    'NFSBasePath': None,
    'DataGatherLogPath': None,
    'DataGatherDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'DataGatherImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/gather-consumer:v1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'DataGatherDBHost': 'mariadb-svc',
    'DataGatherDBName': 'picture_center',
    'DataGatherDBUser': 'data_access',
    "DataGatherDBPassword": None,
    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,
    'dependences': ['apps.common.nginx/NginxTool','apps.common.redis/RedisTool',
                    'apps.common.nacos/NacosTool','apps.common.zookeeper/ZookeeperTool',
                    'apps.common.kafka/KafkaTool',
                    ]
}