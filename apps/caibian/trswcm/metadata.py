#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'trswcm',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'TRSWCMDataPath': None,
    'TRSWCMLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'TRSWCMImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/wcm-deploy:xjzmy-devops-2.22.53',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'TRSWCMDBHost': 'mariadb-svc',
    'TRSWCMDBName': 'mty_wcm',
    'TRSWCMDBUser': 'mtywcm',
    "TRSWCMDBPassword": None,
    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,
    'TRSMQUser': 'admin',
    'TRSMQPassword': None,
    'PrivateURLHost': None,
    'PublishURLHost': None,
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.rabbitmqha/RabbitmqHATool',
                    ]
}