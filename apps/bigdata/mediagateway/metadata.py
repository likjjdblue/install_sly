#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'mediagateway',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'MediaGatewayLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MediaGatewayImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/media-gateway:v1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'MediaGatewayDBHost': 'mariadb-svc',
    'MediaGatewayDBName': 'media_gateway',
    'MediaGatewayDBUser': 'media_gateway',
    "MediaGatewayDBPassword": None,
    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,
    'dependences': ['apps.common.nginx/NginxTool','apps.common.redis/RedisTool',
                    'apps.common.nacos/NacosTool', 'apps.common.mariadb/MariaDBTool',
                    ]
}