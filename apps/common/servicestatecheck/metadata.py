#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'servicestatecheck',
    'NFSAddr': None,
    'NFSBasePath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'ServiceStateCheckImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/service_state_check:latest',
    "NFSProvisionerImage": 'registry.cn-hangzhou.aliyuncs.com/trssly/nfs-client-provisioner:latest',
    'RetryInterval': 2,
    'RetryTimes': 150,
    'ConnectionTimeOut': 5,
}