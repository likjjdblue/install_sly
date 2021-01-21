#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'tenantcenter',
    'NFSAddr': None,
    'NFSBasePath': None,
    'TenantCenterLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'TenantCenterImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/tenantcenter:v1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'TenantCenterDBHost': 'mariadb-svc',
    'TenantCenterDBName': 'mty_wcm',
    'TenantCenterDBUser': 'mtywcm',
    "TenantCenterDBPassword": None,
    'TenantCenterNacosAddr': 'nacos-svc',
    'dependences': ['apps.common.nginx/NginxTool','apps.caibian.trswcm/TRSWCMTool',
                    ]
}