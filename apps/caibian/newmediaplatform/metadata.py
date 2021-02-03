#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'newmediaplatform',
    'NFSAddr': None,
    'NFSBasePath': None,
    'NewMediaPlatformLogPath': None,
    'NewMediaPlatformDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'NewMediaPlatformImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/newmediaplatform-deploy:xjzmy-devops-v5.20.1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'NewMediaPlatformDBHost': 'mariadb-svc',
    'NewMediaPlatformDBName': 'new_media_platform',
    'NewMediaPlatformDBUser': 'newmedia',
    "NewMediaPlatformDBPassword": None,

    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,

    'RedisPassword': None,
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool',
                    ]
}