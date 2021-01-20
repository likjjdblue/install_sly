#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'mlfsearch',
    'NFSAddr': None,
    'NFSBasePath': None,
    'MLFSearchLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MLFSearchImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/mlfsearch:v1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'dependences': ['apps.common.nginx/NginxTool', ]
}