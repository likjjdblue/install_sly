#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'rabbitmq_ha',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'BusyboxImage': 'busybox:1.30.1',
    'RabbitmqImage': 'rabbitmq:3.8.7-alpine',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'RabbitmqPassword': None,
    'VHosts': ['BQXT', 'CHNL', 'CLOUD', 'DC', 'MZ', 'maima', 'messageCenter']
}