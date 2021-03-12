#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'imserver',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'IMServerLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'IMServerImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/im-server-deploy:xjzmy-devops-v0.2.1.6',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'IMServerDBHost': 'mariadb-svc',
    'IMServerDBName': 'im_server',
    'IMServerDBUser': 'im_server',
    "IMServerDBPassword": None,
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    ]
}