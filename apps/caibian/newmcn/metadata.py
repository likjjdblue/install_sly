#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'newmcn',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'MCNDataPath': None,
    'MCNLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MCNImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/mcn-deploy:xjzmy-devops-2.5.5',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'UPCDBHost': 'mariadb-svc',
    'UPCDBName': 'mcn_upc',
    'UPCDBUser': 'mcnupc',
    "UPCDBPassword": None,

    'UPC_MtyDBHost': 'mariadb-svc',
    'UPC_MtyDBName': 'mcn_upc_mty',
    'UPC_MtyDBUser': 'mcnupc',
    "UPC_MtyDBPassword": None,

    'UPC_QuartzDBHost': 'mariadb-svc',
    'UPC_QuartzDBName': 'mcn_upc_quartz',
    'UPC_QuartzDBUser': 'mcnupc',
    "UPC_QuartzDBPassword": None,

    'UPC_MrsDBHost': 'mariadb-svc',
    'UPC_MrsDBName': 'mty_mrs',
    'UPC_MrsDBUser': 'mcnupc',
    "UPC_MrsDBPassword": None,

    'UPCRedisHost': 'redis-svc',
    'UPCRedisPort': '6379',
    'UPCRedisPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool'
                    ]
}