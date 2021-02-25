#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'nacos',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'MysqlDataPath': None,
    'NacosDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'MysqlImage': 'nacos/nacos-mysql:5.7',
    'NacosImage': 'nacos/nacos-server:latest',
    'NacosPeerFinderImage': 'nacos/nacos-peer-finder-plugin:1.0',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    "MysqlPassword": None,
    "MysqlHostIP": None,
}