#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'newmcnadmin',
    'NFSAddr': None,
    'NFSBasePath': None,
    'MCNAdminDataPath': None,
    'MCNAdminLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MCNAdminImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/mcnadmin:v1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'UPCAdminDBHost': 'mariadb-svc',
    'UPCAdminDBName': 'mcn_upc',
    'UPCAdminDBUser': 'mcnadmin',
    "UPCAdminDBPassword": None,

    'UPCAdmin_MtyDBHost': 'mariadb-svc',
    'UPCAdmin_MtyDBName': 'mcn_upc_mty',
    'UPCAdmin_MtyDBUser': 'mcnadmin',
    "UPCAdmin_MtyDBPassword": None,

    'UPCAdmin_QuartzDBHost': 'mariadb-svc',
    'UPCAdmin_QuartzDBName': 'mcn_upc_quartz',
    'UPCAdmin_QuartzDBUser': 'mcnadmin',
    "UPCAdmin_QuartzDBPassword": None,

    'UPCAdmin_MrsDBHost': 'mariadb-svc',
    'UPCAdmin_MrsDBName': 'mty_mrs',
    'UPCAdmin_MrsDBUser': 'mcnadmin',
    "UPCAdmin_MrsDBPassword": None,

    'UPCAdminRedisHost': 'redis-svc',
    'UPCAdminRedisPort': '6379',
    'UPCAdminRedisPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.caibian.newmcn/MCNTool'
                    ]
}