#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'mongodb',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    #'MongodbImage': 'docker.io/bitnami/mongodb:4.4.1-debian-10-r39',
    'MongodbImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/mongodb:4.4.1-debian-10-r39',
    #"NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    "NFSProvisionerImage": 'registry.cn-hangzhou.aliyuncs.com/trssly/nfs-client-provisioner:latest',
    'MongoPassword': None,
}