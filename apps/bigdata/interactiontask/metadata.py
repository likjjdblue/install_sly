#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'interactiontask',
    'NFSAddr': None,
    'NFSBasePath': None,
    'InteractionTaskLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'InteractionTaskImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/interaction-task-deploy:zmy-devops-v1.6.1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'InteractionTaskDBHost': 'mariadb-svc',
    'InteractionTaskDBName': 'interaction',
    'InteractionTaskDBUser': 'interaction',
    "InteractionTaskDBPassword": None,
    'TRSRedisHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redisha/RedisHATool', 'apps.common.nacos/NacosTool',
                    'apps.common.zookeeper/ZookeeperTool', 'apps.common.kafka/KafkaTool'
                    ]
}