#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'callback',
    'NFSAddr': None,
    'NFSBasePath': None,
    'CallbackLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'CallbackImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/callback-deploy:devops-1.1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'CallbackPrimaryDBHost': 'mariadb-svc',
    'CallbackPrimaryDBName': 'mcb_metasearch',
    'CallbackPrimaryDBUser': 'mcbmetasearch',
    "CallbackPrimaryDBPassword": None,


    'RedisHost': 'redis-svc:6379',
    'RedisMasterName': 'mymaster',
    'RedisPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool',
                    ]
}