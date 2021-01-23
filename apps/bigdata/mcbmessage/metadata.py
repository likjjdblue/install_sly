#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'mcbmessage',
    'NFSAddr': None,
    'NFSBasePath': None,
    'MCBMessageLogPath': None,
    'MCBMessageDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MCBMessageImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/message:v2',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'MCBMessagePrimaryDBHost': 'mariadb-svc',
    'MCBMessagePrimaryDBName': 'message',
    'MCBMessagePrimaryDBUser': 'message',
    "MCBMessagePrimaryDBPassword": None,

    'MCBMessageSecondDBHost': 'mariadb-svc',
    'MCBMessageSecondDBName': 'mty_wcm',
    'MCBMessageSecondDBUser': 'mtywcm',
    "MCBMessageSecondDBPassword": None,

    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,

    'MCBMessageMQHost': 'rabbitmq-svc',
    'MCBMessageMQPort': '5672',
    'MCBMessageMQUser': 'admin',
    'MCBMessageMQPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.nacos/NacosTool',
                    'apps.common.rabbitmqha/RabbitmqHATool', 'apps.common.zookeeper/ZookeeperTool',
                    'apps.common.kafka/KafkaTool', 'apps.caibian.trswcm/TRSWCMTool',
                    ]
}