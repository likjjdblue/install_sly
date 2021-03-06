#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import nfs, nfsprovisioner, servicestatecheck
from tools import k8s_tools
from metadata import AppInfo
from copy import deepcopy
from apps import replaceDockerRepo
from  tools import crypto_tools, ssh_tools
import jinja2
import yaml
import subprocess
from time import sleep
from tools import k8s_tools
from pprint import pprint
from codecs import open as open
from storagenode import datastoragenode, logstoragenode
from apps.storage import getClsObj
from apps import mergeTwoDicts



class NginxTool(object):
    CachedResult = None

    def __init__(self, namespace='default', nginxdatapath='nginx-pv-web', nginxlogpath='nginx-pv-log',
                 nginxconfigpath='nginx-pv-config', nginxwcmdatapath='trswcm-pv-data/WCMData',
                 nginxwcmpublishdatapath='trswcm-pv-data/WCMPubData', nginxmcndatapath='mcn-pv-data/MCNData',
                 harbor=None, retrytimes=60, *args, **kwargs):

        namespace = namespace.strip()
        self.RetryTimes = int(retrytimes)
        self.AppInfo = deepcopy(AppInfo)

        self.AppInfo['DataStorageAddr'] = datastoragenode['hostname']
        self.AppInfo['DataStorageBasePath'] = datastoragenode['basepath']
        self.AppInfo['LogStorageAddr'] = logstoragenode['hostname']
        self.AppInfo['LogStorageBasePath'] = logstoragenode['basepath']


        self.AppInfo['NginxDataPath'] = os.path.join(self.AppInfo['DataStorageBasePath'], '-'.join([namespace, nginxdatapath]))
        self.AppInfo['NginxLogDataPath'] = os.path.join(self.AppInfo['LogStorageBasePath'], '-'.join([namespace, nginxlogpath]))
        self.AppInfo['NginxConfigDataPath'] = os.path.join(self.AppInfo['DataStorageBasePath'], '-'.join([namespace, nginxconfigpath]))

        self.AppInfo['Namespace'] = namespace


        #### 20210202 ###
        TmpList = nginxwcmdatapath.split('/')
        self.AppInfo['NginxWCMDataPath'] = os.path.join(self.AppInfo['DataStorageBasePath'],
                                          '-'.join([self.AppInfo['Namespace'], TmpList[0]]), *TmpList[1:])

        TmpList = nginxwcmpublishdatapath.split('/')
        self.AppInfo['NginxWCMPublishDataPath'] = os.path.join(self.AppInfo['DataStorageBasePath'],
                                          '-'.join([self.AppInfo['Namespace'], TmpList[0]]), *TmpList[1:])


        TmpList = nginxmcndatapath.split('/')
        self.AppInfo['NginxMCNDataPath'] = os.path.join(self.AppInfo['DataStorageBasePath'],
                                          '-'.join([self.AppInfo['Namespace'], TmpList[0]]), *TmpList[1:])

        #### END ####


        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.DataStorageObj = getClsObj(datastoragenode['type'])(**datastoragenode)
        self.LogStorageObj = getClsObj(logstoragenode['type'])(**logstoragenode)


        TmpCWDPath = os.path.abspath(__file__)
        TmpCWDPath = os.path.dirname(TmpCWDPath)
        self.BaseDIRPath= os.path.realpath(os.path.join(TmpCWDPath, '../../..'))

        if  self.getValues():
            print ('load from file....')
            self.AppInfo = deepcopy(self.getValues())

    def setupStorage(self):
        TmpResponse = self.DataStorageObj.installStorage(basedir=self.AppInfo['DataStorageBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        TmpResponse = self.LogStorageObj.installStorage(basedir=self.AppInfo['LogStorageBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse


        print ('create SQLTool Storage successfully')

        self.DataStorageObj.createSubFolder(self.AppInfo['NginxDataPath'])
        self.LogStorageObj.createSubFolder(self.AppInfo['NginxLogDataPath'])
        self.DataStorageObj.createSubFolder(self.AppInfo['NginxConfigDataPath'])

        #### 20210202 ####
        self.DataStorageObj.createSubFolder(self.AppInfo['NginxWCMDataPath'])
        self.DataStorageObj.createSubFolder(self.AppInfo['NginxWCMPublishDataPath'])
        self.DataStorageObj.createSubFolder(self.AppInfo['NginxMCNDataPath'])

        #### END #####

        self.TmpStoragePathDict = dict()
        self.TmpStoragePathDict['NginxDataPath'] = self.DataStorageObj.generateRealPath(self.AppInfo['NginxDataPath'])
        self.TmpStoragePathDict['NginxLogDataPath'] = self.LogStorageObj.generateRealPath(self.AppInfo['NginxLogDataPath'])
        self.TmpStoragePathDict['NginxConfigDataPath'] = self.DataStorageObj.generateRealPath(self.AppInfo['NginxConfigDataPath'])
        self.TmpStoragePathDict['NginxWCMDataPath'] = self.DataStorageObj.generateRealPath(self.AppInfo['NginxWCMDataPath'])
        self.TmpStoragePathDict['NginxWCMPublishDataPath'] = self.DataStorageObj.generateRealPath(self.AppInfo['NginxWCMPublishDataPath'])
        self.TmpStoragePathDict['NginxMCNDataPath'] = self.DataStorageObj.generateRealPath(self.AppInfo['NginxMCNDataPath'])



        print ('setup Nginx Storage successfully')

        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['NginxImage'] = replaceDockerRepo(self.AppInfo['NginxImage'], self.AppInfo['HarborAddr'])
        self.AppInfo['NFSProvisionerImage'] =replaceDockerRepo(self.AppInfo['NFSProvisionerImage'],
                                                               self.AppInfo['HarborAddr'])



    def renderTemplate(self):
        TmpCWDPath = os.path.abspath(__file__)
        TmpCWDPath = os.path.dirname(TmpCWDPath)
        self.AppInfo['TargetNamespaceDIR'] = os.path.join(TmpCWDPath, self.AppInfo['TargetNamespaceDIR'])

        if not os.path.isdir(os.path.realpath(self.AppInfo['TargetNamespaceDIR'])):
            os.mkdir(os.path.realpath(self.AppInfo['TargetNamespaceDIR']))
        if not os.path.isdir(os.path.realpath(os.path.join(self.AppInfo['TargetNamespaceDIR'],
                                                           self.AppInfo['Namespace']))):
            os.mkdir(os.path.realpath(os.path.join(self.AppInfo['TargetNamespaceDIR'],
                                                           self.AppInfo['Namespace'])))

        TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                             self.AppInfo['AppName'])
        TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


        if not os.path.isdir(TmpTargetNamespaceDIR):
            os.mkdir(TmpTargetNamespaceDIR)

        if not os.path.isfile(os.path.join(TmpTargetNamespaceDIR, 'values.yaml')):
            self.generateValues()

            TmpAppInfo = mergeTwoDicts(self.AppInfo, self.TmpStoragePathDict)

            with open(os.path.join(TmpTargetNamespaceDIR, 'values.yaml'), mode='wb') as f:
                yaml.safe_dump(self.AppInfo, f)

            TmpCWDPath = os.path.abspath(__file__)
            TmpCWDPath = os.path.dirname(TmpCWDPath)

            subprocess.Popen('/usr/bin/cp -r %s %s'%(os.path.join(TmpCWDPath, 'resource'),
                                                     TmpTargetNamespaceDIR), shell=True)
            sleep (5)

            for basepath, _, files in os.walk(os.path.join(TmpTargetNamespaceDIR, 'resource')):
                for file in files:
                    TmpContent = ''
                    with open(os.path.join(basepath, file), mode='rb', encoding='utf-8') as f:
                        TmpContent = f.read()
                    TmpContent = jinja2.Template(TmpContent).render(TmpAppInfo)

                    with open(os.path.join(basepath, file), mode='wb', encoding='utf-8') as f:
                        f.write(TmpContent)

        with open(os.path.join(TmpTargetNamespaceDIR, 'values.yaml'), mode='rb', encoding='utf-8') as f:
            self.AppInfo = yaml.safe_load(f)


    def applyYAML(self):
        print ('Create namespace: '+str(self.AppInfo['Namespace']))
        TmpResponse = self.k8sObj.createNamespace(name=self.AppInfo['Namespace'])
        if TmpResponse['ret_code'] != 0:
            print (TmpResponse)
            return TmpResponse


        print ('Apply Nginx ....')
        if not self.k8sObj.checkNamespacedResourceHealth(name='nginx-deploy', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment'):
            try:
                self.k8sObj.deleteNamespacedDeployment(name='nginx-deploy', namespace=self.AppInfo['Namespace'])
            except:
                pass

            TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                                 self.AppInfo['AppName'])
            TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'nginx-pv.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'nginx-pvc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'nginx-svc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'nginx-cm-nginx.conf.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )


            TmpResponse = self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource',
                                                        'nginx-deploy.yaml'),namespace=self.AppInfo['Namespace'])
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning=False
        for itime in range(self.RetryTimes):
            TmpResponse = self.k8sObj.getNamespacedDeployment(name='nginx-deploy',
                                                                   namespace=self.AppInfo['Namespace'])['result'].to_dict()

            if not self.k8sObj.checkNamespacedResourceHealth(name='nginx-deploy', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment'):
                print ('Waitting for Deployment  %s to be ready,replicas: %s, available replicas: %s')%(
                    TmpResponse['metadata']['name'], str(TmpResponse['status']['replicas']),
                    str(TmpResponse['status']['ready_replicas'])
                )
                sleep (5)
                continue

            TmpServiceCheckObj = servicestatecheck.ServiceStateCheckTool(namespace=self.AppInfo['Namespace'],
                                                                         harbor=self.AppInfo['HarborAddr'])
            TmpCheckResult = TmpServiceCheckObj.checkServicePortState(targetaddress='nginx-svc:80')
            print ('nginx-svc:80 is listening....')

            print ('Deployment: %s is available;replicas: %s')%(TmpResponse['metadata']['name'],
                                                              str(TmpResponse['status']['replicas']))
            isRunning = True
            break

        if not isRunning:
            print ('Failed to apply Deployment: %s')%(TmpResponse['metadata']['name'],)
            return {
                'ret_code': 1,
                'result': 'Failed to apply Deployment: %s'%(TmpResponse['metadata']['name'],)
            }
        print ('Waitting Nginx for running....')

        return {
            'ret_code': 0,
            'result': 'Deployment: %s is available;replicas: %s'%(TmpResponse['metadata']['name'],
                                                                    str(TmpResponse['status']['replicas']))
        }

    def start(self):
        if NginxTool.CachedResult:
            print ('Using cached result')
            return NginxTool.CachedResult

        TmpResponse = self.setupStorage()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        self.renderTemplate()

        TmpResponse = self.applyYAML()
        self.close()

        if TmpResponse['ret_code'] == 0:
            NginxTool.CachedResult = TmpResponse
        return TmpResponse


    def getValues(self):
        TmpTargetNamespaceDIR = os.path.join(self.BaseDIRPath, 'namespaces', self.AppInfo['Namespace'],
                                             self.AppInfo['AppName'])
        TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


        TmpValuse = None
        if  os.path.isfile(os.path.join(TmpTargetNamespaceDIR, 'values.yaml')):

            with open(os.path.join(TmpTargetNamespaceDIR, 'values.yaml'), mode='rb') as f:
                TmpValuse = yaml.safe_load(f)

            NginxTool.CachedResult = {
                'ret_code': 0,
            }
        return TmpValuse


    def close(self):
        self.DataStorageObj.close()
        self.LogStorageObj.close()




if __name__ == "__main__":
    tmp = NginxTool(namespace='sly2', nfsinfo=dict(hostname='192.168.200.168', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
    tmp.start()
