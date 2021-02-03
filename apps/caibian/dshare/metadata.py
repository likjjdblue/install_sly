#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'dshare',
    'NFSAddr': None,
    'NFSBasePath': None,
    'DshareLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'DshareImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/dshare-deploy:xjzmy-devops-2.0.3',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'DshareDBHost': 'mariadb-svc',
    'DshareDBName': 'mty_dshare',
    'DshareDBUser': 'dshare',
    "DshareDBPassword": None,
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    ]
}