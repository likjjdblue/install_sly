#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'paperreview',
    'NFSAddr': None,
    'NFSBasePath': None,
    'PaperReviewLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'PaperReviewImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/paperreview:v1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'PaperReviewDBHost': 'mariadb-svc',
    'PaperReviewDBName': 'mty_wcm',
    'PaperReviewDBUser': 'mtywcm',
    "PaperReviewDBPassword": None,
    'PaperReviewRedisHost': 'redis-svc',
    'PaperReviewRedisPort': '6379',
    'PaperReviewRedisPassword': None,
    'PaperReviewNacosAddr': 'nacos-svc',
    'PaperReviewNacosID': '8953ca45-4cfb-469a-bc55-7e3bce569994',
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.redis/RedisTool',
                    'apps.common.nacos/NacosTool', 'apps.caibian.trswcm/TRSWCMTool',
                    ]
}