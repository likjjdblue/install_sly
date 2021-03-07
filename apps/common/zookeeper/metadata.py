#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'zookeeper',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    #'ZookeeperImage': 'docker.io/bitnami/zookeeper:3.6.2-debian-10-r37',
    'ZookeeperImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/zookeeper:3.6.2-debian-10-r37',
    "NFSProvisionerImage": 'registry.cn-hangzhou.aliyuncs.com/trssly/nfs-client-provisioner:latest',
}