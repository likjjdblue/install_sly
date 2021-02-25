#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import  nfsprovisioner
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


class SQLTool(object):
    def __init__(self, namespace='default', sqlfilepath='sqltool-pv-sql', sqlaccountpath='sqltool-pv-account',
                 harbor=None, retrytimes=600, *args, **kwargs):

        namespace = namespace.strip()
        self.RetryTimes = int(retrytimes)
        self.AppInfo = deepcopy(AppInfo)

        self.AppInfo['DataStorageAddr'] = datastoragenode['hostname']
        self.AppInfo['DataStorageBasePath'] = datastoragenode['basepath']
        self.AppInfo['LogStorageAddr'] = logstoragenode['hostname']
        self.AppInfo['LogStorageBasePath'] = logstoragenode['basepath']


        self.AppInfo['SQLFilePath'] = os.path.join(self.AppInfo['DataStorageBasePath'], '-'.join([namespace, sqlfilepath]))
        self.AppInfo['SQLAccountPath'] = os.path.join(self.AppInfo['DataStorageBasePath'], '-'.join([namespace, sqlaccountpath]))


        self.AppInfo['Namespace'] = namespace

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()



        self.DataStorageObj = getClsObj(datastoragenode['type'])(**datastoragenode)
        self.LogStorageObj = getClsObj(logstoragenode['type'])(**logstoragenode)

    def setupStorage(self):
        TmpResponse = self.DataStorageObj.installStorage(basedir=self.AppInfo['DataStorageBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        TmpResponse = self.DataStorageObj.installStorage(basedir=self.AppInfo['LogStorageBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse


        print ('create SQLTool Storage successfully')

        self.DataStorageObj.createSubFolder(self.AppInfo['SQLFilePath'])
        self.DataStorageObj.createSubFolder(self.AppInfo['SQLAccountPath'])




        print ('setup SQLTool Storage successfully')

        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['SQLToolImage'] = replaceDockerRepo(self.AppInfo['SQLToolImage'], self.AppInfo['HarborAddr'])
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
                    TmpContent = jinja2.Template(TmpContent).render(self.AppInfo)

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


        print ('Apply SQLTool ....')
        if True:
            try:
                print ('delete pod....')
                tmp=self.k8sObj.deleteNamespacedPod(name='sqltool-deploy', namespace=self.AppInfo['Namespace'])
                print (tmp)
            except Exception as e:
                pass

            TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                                 self.AppInfo['AppName'])
            TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'sqltool-pv.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'sqltool-pvc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )


            TmpResponse = self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource',
                                                        'sqltool-deploy.yaml'),namespace=self.AppInfo['Namespace'])
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning=False
        for itime in range(self.RetryTimes):
            print ('current times: '+str(itime))
            TmpResponse = self.k8sObj.getNamespacedPod(name='sqltool-deploy',
                                                                   namespace=self.AppInfo['Namespace'])['result'].to_dict()

            TmpPodStatus = TmpResponse['status']['phase']
            print (TmpPodStatus)

            if TmpPodStatus == 'Failed':
                print ('Pod failed ')
                return {
                    'ret_code': 1,
                    'result': 'Pod failed'
                }
            elif TmpPodStatus == 'Succeeded':
                print ('Pod Succeeded')
                return {
                    'ret_code': 0,
                    'result': 'Pod Succeeded'
                }

            print ('Pod is running, waitting...')
            sleep (10)

        print ('Timeout waitting for pod')
        return {
            'ret_code': 1,
            'result': 'Timeout waitting for pod'
        }



    def start(self):
        TmpResponse = self.setupStorage()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        self.renderTemplate()

        TmpResponse = self.applyYAML()
        return TmpResponse


    def getValues(self):
        TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                             self.AppInfo['AppName'])
        TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


        TmpValuse = None
        if  os.path.isfile(os.path.join(TmpTargetNamespaceDIR, 'values.yaml')):

            with open(os.path.join(TmpTargetNamespaceDIR, 'values.yaml'), mode='rb') as f:
                TmpValuse = yaml.safe_load(f)
        return TmpValuse




if __name__ == "__main__":
    tmp = SQLTool(namespace='sly2', nfsinfo=dict(hostname='192.168.200.168', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
    tmp.start()
