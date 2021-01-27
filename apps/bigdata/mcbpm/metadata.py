#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'mcbpm',
    'NFSAddr': None,
    'NFSBasePath': None,
    'MCBPMLogPath': None,
    'MCBPMDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MCBPMImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/pm:v4',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'MCBPMPrimaryDBHost': 'mariadb-svc',
    'MCBPMPrimaryDBName': 'pm',
    'MCBPMPrimaryDBUser': 'pm',
    "MCBPMPrimaryDBPassword": None,

    'MCBPMSecondDBHost': 'mariadb-svc',
    'MCBPMSecondDBName': 'mty_wcm',
    'MCBPMSecondDBUser': 'mtywcm',
    "MCBPMSecondDBPassword": None,

    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,

    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'MCBPMMQHost': 'rabbitmq-svc',
    'MCBPMMQPort': '5672',
    'MCBPMMQUser': 'admin',
    'MCBPMMQPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.nacos/NacosTool',
                    'apps.common.rabbitmqha/RabbitmqHATool', 'apps.common.zookeeper/ZookeeperTool',
                    'apps.common.kafka/KafkaTool', 'apps.caibian.trswcm/TRSWCMTool',
                    'apps.common.redisha/RedisHATool',
                    ]
}