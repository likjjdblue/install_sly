#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'downimg',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'DownImgDataPath': None,
    'DownImgLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'DownImgImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/tmyimgcenter:v1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'DownImgDBHost': 'mariadb-svc',
    'DownImgDBName': 'devdc',
    'DownImgDBUser': 'tmyimgcenter',
    "DownImgDBPassword": None,
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    ]
}