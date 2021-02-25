#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'ddc',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'DDCLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'DDCImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/ddc-deploy:xjzmy-devops-2.2.3',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'DDCDBHost': 'mariadb-svc',
    'DDCDBName': 'mty_ddc',
    'DDCDBUser': 'mtyddc',
    "DDCDBPassword": None,
    'DDCRedisHost': 'redis-svc',
    'DDCRedisPort': '6379',
    'DDCRedisPassword': None,
    'DDCMQUser': 'admin',
    'DDCMQPassword': None,
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.redis/RedisTool',
                    'apps.common.rabbitmqha/RabbitmqHATool', 'apps.caibian.trswcm/TRSWCMTool',
                    ]
}