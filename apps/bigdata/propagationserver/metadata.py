#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'propagationserver',
    'NFSAddr': None,
    'NFSBasePath': None,
    'PropagationServerLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,

    'PropagationServerImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/propagation-server:v2',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'PropagationServerPrimaryDBHost': 'mariadb-svc',
    'PropagationServerPrimaryDBName': 'propagation',
    'PropagationServerPrimaryDBUser': 'propagation_server',
    "PropagationServerPrimaryDBPassword": None,


    'RedisHost': 'redis-svc:6379',
    'RedisPassword': None,


    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.nacos/NacosTool',
                    'apps.common.zookeeper/ZookeeperTool', 'apps.common.kafka/KafkaTool',
                    ]
}