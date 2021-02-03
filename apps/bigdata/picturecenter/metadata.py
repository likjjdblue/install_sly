#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'picturecenter',
    'NFSAddr': None,
    'NFSBasePath': None,
    'PictureCenterLogPath': None,
    'PictureCenterDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,

    'PictureCenterImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/picturecenter-deploy:zmy-devops-v1.0.0.3',
    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'PictureCenterPrimaryDBHost': 'mariadb-svc',
    'PictureCenterPrimaryDBName': 'picture_center',
    'PictureCenterPrimaryDBUser': 'piccenter',
    "PictureCenterPrimaryDBPassword": None,


    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'PictureCenterMongoDBHost': 'mongodb-headless:27017',
    'PictureCenterMongoDBUser': 'root',
    'PictureCenterMongoDBPassword': None,

    'PictureCenterZookeeperHost': 'zookeeper-svc:2181',

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.mongodb/MongodbTool', 'apps.common.nacos/NacosTool',
                    'apps.common.zookeeper/ZookeeperTool', 'apps.common.kafka/KafkaTool',
                    'apps.common.redisha/RedisHATool', 'apps.bigdata.bigdataaccess/BigdataAccessTool',
                    ]
}