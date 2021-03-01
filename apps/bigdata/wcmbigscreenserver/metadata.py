#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'wcmbigscreenserver',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'WCMBigScreenServerDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'WCMBigScreenServerImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/wcm-bigscreen-server-deploy:zmy-devops-v2.2.0.2',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'WCMBigScreenServerPrimaryDBHost': 'mariadb-svc',
    'WCMBigScreenServerPrimaryDBName': 'mty_wcm',
    'WCMBigScreenServerPrimaryDBUser': 'mtywcm',
    "WCMBigScreenServerPrimaryDBPassword": None,

    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,

    'WCMBigScreenServerMQHost': 'rabbitmq-svc',
    'WCMBigScreenServerMQPort': '5672',
    'WCMBigScreenServerMQUser': 'admin',
    'WCMBigScreenServerMQPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.nacos/NacosTool',
                    'apps.common.rabbitmqha/RabbitmqHATool', 'apps.common.zookeeper/ZookeeperTool',
                    'apps.common.kafka/KafkaTool', 'apps.caibian.trswcm/TRSWCMTool',
                    ]
}