#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'kafka',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    #'KafkaImage': 'docker.io/bitnami/kafka:2.4.0-debian-10-r0',
    'KafkaImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/kafka:2.4.0-debian-10-r0',
    "NFSProvisionerImage": 'registry.cn-hangzhou.aliyuncs.com/trssly/nfs-client-provisioner:latest',
}