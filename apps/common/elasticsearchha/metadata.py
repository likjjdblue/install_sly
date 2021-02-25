#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'elasticsearch_ha',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'ElasticsearchImage': 'registry.cn-hangzhou.aliyuncs.com/trsrd/elasticsearch:7.4.0-ik',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
}