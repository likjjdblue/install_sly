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

    #'MysqlImage': 'nacos/nacos-mysql:5.7',
    #'NacosImage': 'nacos/nacos-server:latest',
    #'NacosPeerFinderImage': 'nacos/nacos-peer-finder-plugin:1.0',
    #"NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'MysqlImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/nacos-mysql:5.7',
    'NacosImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/nacos-server:latest',
    'NacosPeerFinderImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/nacos-peer-finder-plugin:1.0',
    "NFSProvisionerImage": 'registry.cn-hangzhou.aliyuncs.com/trssly/nfs-client-provisioner:latest',
    "MysqlPassword": None,
    "MysqlHostIP": None,
}