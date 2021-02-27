#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'timingscheduler',

    'DataStorageAddr': None,
    'DataStorageBasePath': None,
    'LogStorageAddr': None,
    'LogStorageBasePath': None,

    'TimingSchedulerLogPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,
    'TimingSchedulerImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/timing_scheduler:v1',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'TimingSchedulerPrimaryDBHost': 'mariadb-svc',
    'TimingSchedulerPrimaryDBName': 'timing',
    'TimingSchedulerPrimaryDBUser': 'timing',
    "TimingSchedulerPrimaryDBPassword": None,

    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.redisha/RedisHATool', 'apps.common.nacos/NacosTool',
                     'apps.common.zookeeper/ZookeeperTool','apps.common.kafka/KafkaTool',
                    ]
}