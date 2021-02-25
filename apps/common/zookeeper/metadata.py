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
    'ZookeeperImage': 'docker.io/bitnami/zookeeper:3.6.2-debian-10-r37',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
}