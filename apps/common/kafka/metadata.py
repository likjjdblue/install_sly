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
    'KafkaImage': 'docker.io/bitnami/kafka:2.4.0-debian-10-r0',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
}