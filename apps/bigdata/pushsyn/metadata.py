#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'pushsyn',
    'NFSAddr': None,
    'NFSBasePath': None,
    'PushSynLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,

    'PushSynImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/push-syn-deploy:zmy-devops-v2.21.1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'PushSynPrimaryDBHost': 'mariadb-svc',
    'PushSynPrimaryDBName': 'propagation',
    'PushSynPrimaryDBUser': 'propagation',
    "PushSynPrimaryDBPassword": None,


    'RedisHost': 'redis-svc:6379',
    'RedisPassword': None,


    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.nacos/NacosTool',
                    'apps.common.zookeeper/ZookeeperTool', 'apps.common.kafka/KafkaTool',
                    'apps.bigdata.propagationserver/PropagationServerTool',
                    ]
}