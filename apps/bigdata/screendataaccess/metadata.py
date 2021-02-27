#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'screendataaccess',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'ScreenDataAccessDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'ScreenDataAccessImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/screen-data-access:v5',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'ScreenDataAccessPrimaryDBHost': 'mariadb-svc',
    'ScreenDataAccessPrimaryDBName': 'tmy_decision_center',
    'ScreenDataAccessPrimaryDBUser': 'decisioncenter',
    "ScreenDataAccessPrimaryDBPassword": None,

    'ScreenDataAccessSecondDBHost': 'mariadb-svc',
    'ScreenDataAccessSecondDBName': 'bigscreen',
    'ScreenDataAccessSecondDBUser': 'bigscreen',
    "ScreenDataAccessSecondDBPassword": None,

    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,

    'ScreenDataAccessMQHost': 'rabbitmq-svc',
    'ScreenDataAccessMQPort': '5672',
    'ScreenDataAccessMQUser': 'admin',
    'ScreenDataAccessMQPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.nacos/NacosTool',
                    'apps.common.rabbitmqha/RabbitmqHATool', 'apps.common.zookeeper/ZookeeperTool',
                    'apps.common.kafka/KafkaTool', 'apps.bigdata.tmydecisioncenter/TmyDecisionCenterTool',
                    ]
}