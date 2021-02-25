#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'redis',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'RedisDataPath': None,
    'RedisStandAlonePassword': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'RedisImage': 'redis:5.0',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
}