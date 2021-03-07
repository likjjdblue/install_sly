#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'nginx',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'NginxDataPath': None,
    'NginxLogDataPath': None,
    'NginxConfigDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'NginxImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/nginx',
    "NFSProvisionerImage": 'registry.cn-hangzhou.aliyuncs.com/trssly/nfs-client-provisioner:latest',
    'NginxWCMDataPath': None,
    'NginxWCMPublishDataPath': None,
    'NginxMCNDataPath': None,
}