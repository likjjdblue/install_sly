#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'sqltool',
    'NFSAddr': None,
    'NFSBasePath': None,

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'SQLFilePath': None,
    'SQLAccountPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'SQLToolImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sql_tool:latest',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
}