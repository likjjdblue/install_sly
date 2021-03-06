#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
import sys, os
import importlib
import re
sys.path.append('.')

import apps
from storagenode import namespace


TmpNamespace = namespace

APPMap = {
    '1': 'apps.common.zookeeper/ZookeeperTool',
    '2': 'apps.common.mariadb/MariaDBTool',
    '3': 'apps.common.mongodb/MongodbTool',
    '4': 'apps.common.nacos/NacosTool',
    '5': 'apps.common.nginx/NginxTool',
    '6': 'apps.common.rabbitmqha/RabbitmqHATool',
    '7': 'apps.common.redis/RedisTool',
    '8': 'apps.common.redisha/RedisHATool',
    '9': 'apps.common.kafka/KafkaTool',
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
    '43': 'apps.caibian.callback/CallbackTool',
    '44': 'apps.bigdata.ifunc/iFuncTool',
    '45': 'apps.trs.hybase/TRSHyBaseTool',
    '46': 'apps.trs.ckm6/TRSCKM6Tool',
    '47': 'apps.common.elasticsearchha/ElasticsearchHATool',
    '48': 'apps.bigdata.interactiontask/InteractionTaskTool',
    '49': 'apps.bigdata.interactionservicecenter/InteractionServiceCenterTool',
}


def showMenu():
    for i in range(1,len(APPMap)+1):
        TmpAppName = APPMap[str(i)].split('/')[1].replace('Tool', '')
        print ('%s : install %s')%(str(i),TmpAppName )
    print ('0 : quit')


def installApps(TmpRawStr):

    try:
        from storagenode import harborAddr
    except:
        harborAddr = None

    TmpList = TmpRawStr.split('/')
    print (TmpList)
    TmpModuleName, TmpClsName = (TmpList[0], TmpList[1])
    TmpModule = importlib.import_module(TmpModuleName)
    TmpInstance = getattr(TmpModule, TmpClsName)(namespace=TmpNamespace, harbor=harborAddr)
    TmpResponse = TmpInstance.start()
    print (TmpResponse)
    return TmpResponse



def parseChoice(choice):
    AutoQuit = False
    choice = choice.strip()
    TmpTargeList = []
    TmpList = choice.split(',')

    for tmp in TmpList:
        tmp = tmp.strip()
        if tmp in APPMap:
            TmpTargeList.append(tmp)
        elif '-' in tmp:
            TmpReObj = re.search(r'^(\d+)\s*-\s*(\d+)$', tmp)
            if not TmpReObj:
                print ('invalid choice %s'%(tmp, ))
                continue

            MinInt = TmpReObj.group(1)
            MaxInt = TmpReObj.group(2)

            if MinInt == '0':
                AutoQuit = True

            MinInt = max(1, int(MinInt))
            MaxInt = min(len(APPMap) + 1, int(MaxInt))

            if int(MinInt) > int(MaxInt):
                print ('invalid choice %s'%(tmp, ))
                continue

            TmpTargeList += [str(_) for _ in range(int(MinInt), int(MaxInt) + 1)]

        elif tmp =='0':
            AutoQuit = True
        else:
            print ('invalid choice %s' % (tmp,))

    TmpTargeList = list(set(TmpTargeList))
    TmpTargeList = [int(x) for x in TmpTargeList]
    TmpTargeList.sort()
    TmpTargeList = [str(x) for x in TmpTargeList ]

    if AutoQuit:
        TmpTargeList.append('0')

    print ('Final choice: '+str(TmpTargeList))
    return TmpTargeList



def applyChoice(choice):
    choice = choice.strip()

    if choice == '0':
        exit(0)

    TmpResponse = installApps(APPMap[choice])
    if TmpResponse['ret_code'] != 0:
        print ('failed to install %s' % (APPMap[choice],))
        exit (1)



def runMenu():
    while True:
        showMenu()
        TmpChoice = raw_input('input number: ')
        TmpChoiceList = parseChoice(TmpChoice)

        for choice in TmpChoiceList:
            print ('current choice: %s\n\n'%(choice))
            applyChoice(choice)


if __name__ == '__main__':
    runMenu()




