#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'bigdataaccess',
    'NFSAddr': None,
    'NFSBasePath': None,
    'BigdataAccessLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'BigdataAccessImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/bigdata-access-deploy:zmy-devops-v2.8.0',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',
    'BigdataAccessDBHost': 'mariadb-svc',
    'BigdataAccessDBName': 'tmy_decision_center',
    'BigdataAccessDBUser': 'decisioncenter',
    "BigdataAccessDBPassword": None,
    'TRSRedisHost': 'redis-svc',
    'TRSRedisPort': '6379',
    'TRSRedisPassword': None,
    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redis/RedisTool', 'apps.common.nacos/NacosTool',
                    'apps.common.zookeeper/ZookeeperTool', 'apps.common.kafka/KafkaTool',
                    'apps.bigdata.tmydecisioncenter/TmyDecisionCenterTool',
                    ]
}