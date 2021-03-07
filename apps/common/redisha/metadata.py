#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'redis_ha',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    #'ShellCheckImage': 'koalaman/shellcheck:v0.5.0',
    #'RedisImage': 'redis:5.0.6-alpine',

    'ShellCheckImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/shellcheck:v0.5.0',
    'RedisImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/redis:5.0.6-alpine',

    "NFSProvisionerImage": 'registry.cn-hangzhou.aliyuncs.com/trssly/nfs-client-provisioner:latest',
    'RedisPassword': None,
}