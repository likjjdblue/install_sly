#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
import sys, os
import importlib
sys.path.append('.')

import apps
from nfsnode import nfsinfo, namespace

TmpNFS = nfsinfo
TmpNamespace = namespace

APPMap = {
    '1': 'apps.common.kafka/KafkaTool',
    '2': 'apps.common.mariadb/MariaDBTool',
    '3': 'apps.common.mongodb/MongodbTool',
    '4': 'apps.common.nacos/NacosTool',
    '5': 'apps.common.nginx/NginxTool',
    '6': 'apps.common.rabbitmqha/RabbitmqHATool',
    '7': 'apps.common.redis/RedisTool',
    '8': 'apps.common.redisha/RedisHATool',
    '9': 'apps.common.zookeeper/ZookeeperTool',
    '10': 'apps.trs.trsids/TRSIDSTool',
    '11': 'apps.trs.ckm/CKMTool',
    '12':  'apps.caibian.ddc/DDCTool',
    '13':  'apps.caibian.downimg/DownImgTool',
    '14':  'apps.caibian.dshare/DshareTool',
    '15':  'apps.caibian.mlfsearch/MLFSearchTool',
    '16': 'apps.caibian.newmcn/MCNTool',
    '17': 'apps.caibian.newmcnadmin/MCNAdminTool',
    '18': 'apps.caibian.paperreview/PaperReviewTool',
    '19': 'apps.caibian.tenantcenter/TenantCenterTool',
    '20': 'apps.caibian.trswcm/TRSWCMTool',
    '21': 'apps.bigdata.bigdataaccess/BigdataAccessTool',
    '22': 'apps.bigdata.datagather/DataGatherTool',
    '23': 'apps.bigdata.dicttool/DicttoolTool',
    '24': 'apps.bigdata.mcbmessage/MCBMessageTool',
    '25': 'apps.bigdata.mcbpm/MCBPMTool',
    '26': 'apps.bigdata.mcbsdmschedule/MCBSDMScheduleTool',
    '27': 'apps.bigdata.mediagateway/MediaGatewayTool',
    '28': 'apps.bigdata.mediaresource/MediaResourceTool',
    '29': 'apps.bigdata.metasearch/MetaSearchTool',
    '30': 'apps.bigdata.picturecenter/PictureCenterTool',
    '31': 'apps.bigdata.propagationserver/PropagationServerTool',
    '32': 'apps.bigdata.pushsyn/PushSynTool',
    '33': 'apps.bigdata.resource/ResourceTool',
    '34': 'apps.bigdata.timingscheduler/TimingSchedulerTool',
    '35': 'apps.bigdata.tmydecisioncenter/TmyDecisionCenterTool',
    '36': 'apps.bigdata.transferresourceai/TransferResourceAITool',
    '37': 'apps.bigdata.transfervideo/TransferVideoTool',
    '38': 'apps.bigdata.webcollection/WebCollectionTool',
    '39': 'apps.caibian.imserver/IMServerTool',
    '40':  'apps.caibian.newmediaplatform/NewMediaPlatformTool',
    '41': 'apps.bigdata.screendataaccess/ScreenDataAccessTool',
    '42': 'apps.bigdata.wcmbigscreenserver/WCMBigScreenServerTool',
}


def showMenu():
    for i in range(1,43):
        TmpAppName = APPMap[str(i)].split('/')[1].replace('Tool', '')
        print ('%s : install %s')%(str(i),TmpAppName )
    print ('0 : quit')


def installApps(TmpRawStr):
    TmpList = TmpRawStr.split('/')
    print (TmpList)
    TmpModuleName, TmpClsName = (TmpList[0], TmpList[1])
    TmpModule = importlib.import_module(TmpModuleName)
    TmpInstance = getattr(TmpModule, TmpClsName)(namespace=TmpNamespace, nfsinfo=TmpNFS)
    TmpResponse = TmpInstance.start()
    print (TmpResponse)
    return TmpResponse

def runMenu():
    while True:
        showMenu()
        choice = raw_input('input number: ')
        choice = choice.strip()
        if choice not in  APPMap and choice != '0':
            print ('invalid number,retry....')
            continue

        if choice == '0':
             break

        TmpResponse = installApps(APPMap[choice])
        if TmpResponse['ret_code'] != 0:
            print ('failed to install %s'%(APPMap[choice], ))
            break


runMenu()



