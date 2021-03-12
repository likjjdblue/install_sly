#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'mlfsearch',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'MLFSearchLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MLFSearchImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/mlfsearch-deploy:xjzmy-devops-1.5',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'dependences': ['apps.common.nginx/NginxTool', 'apps.common.elasticsearchha/ElasticsearchHATool']
}