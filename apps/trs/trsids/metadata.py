#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'trsids',
    'NFSAddr': None,
    'NFSBasePath': None,
    'TRSIDSDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'TRSIDSImage': 'registry.cn-hangzhou.aliyuncs.com/trsrd/trsids:5.1-134463-20210104-new3',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    "TRSIDSPassword": None,
    'TRSIDSDBName': 'mty_ids',
    'TRSIDSDBUser': 'mtyids',
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool']
}