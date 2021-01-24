#!/usr/bin/env python2
# -*- coding: utf-8 -*-

AppInfo = {
    'AppName': 'mcbsdmschedule',
    'NFSAddr': None,
    'NFSBasePath': None,
    'MCBSDMScheduleLogPath': None,
    'MCBSDMScheduleDataPath': None,
    'Namespace': None,
    'TargetNamespaceDIR': '../../.././namespaces',
    'HarborAddr': None,

    'MCBSDMPushAppImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-push-app:v1',
    'MCBSDMWebiteTouTiaoImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-websitetoutiao:v1',
    'MCBSDMFeifanImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-feifan-app:v1',
    'MCBSDMWeixinImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-weixin:v1',
    'MCBSDMSZBOriginalImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-szboriginal:v5',
    'MCBSDMProductImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-product:v1',
    'MCBSDMWeiBoYuQingImage': ' registry.cn-hangzhou.aliyuncs.com/trssly/sdm-weiboyuqing:v1',
    'MCBSDMNewMediaImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-newmedia:v1',
    'MCBSDMTraditionalYuQingImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-traditionalyuqing:v1',
    'MCBSDMWeiboImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-weibo:v1',
    'MCBSDMWebiteImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-website:v1',
    'MCBSDMWeixinYuQingImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-weixinyuqing:v1',
    'MCBSDMEpaperbmImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-epaperbm:v1',
    'MCBSDMMeiziImage': 'registry.cn-hangzhou.aliyuncs.com/trssly/sdm-meizi:v1',

    "NFSProvisionerImage": 'quay.io/external_storage/nfs-client-provisioner:latest',

    'MCBSDMSchedulePrimaryDBHost': 'mariadb-svc',
    'MCBSDMSchedulePrimaryDBName': 'mcb_dicttool',
    'MCBSDMSchedulePrimaryDBUser': 'mcbdicttool',
    "MCBSDMSchedulePrimaryDBPassword": None,


    'RedisHAHost': 'redis-ha-announce-0:26379,redis-ha-announce-1:26379,redis-ha-announce-2:26379',
    'RedisHAMasterName': 'mymaster',
    'RedisHAPassword': None,

    'MCBSDMScheduleMongoDBHost': 'mongodb-headless:27017',
    'MCBSDMScheduleMongoDBUser': 'root',
    'MCBSDMScheduleMongoDBPassword': None,

    'MCBSDMScheduleZookeeperHost': 'zookeeper-svc:2181',

    'dependences': ['apps.common.mariadb/MariaDBTool', 'apps.common.nginx/NginxTool',
                    'apps.common.mongodb/MongodbTool', 'apps.common.nacos/NacosTool',
                    'apps.common.zookeeper/ZookeeperTool', 'apps.common.kafka/KafkaTool',
                    'apps.common.redisha/RedisHATool', 'apps.bigdata.dicttool/DicttoolTool',
                    ]
}