#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import nfsprovisioner, servicestatecheck
from tools import k8s_tools
from metadata import AppInfo
from copy import deepcopy
from apps import replaceDockerRepo
from  tools import crypto_tools
import jinja2
import yaml
import subprocess
from time import sleep
from tools import k8s_tools
from pprint import pprint
from codecs import open as open
from storagenode import datastoragenode, logstoragenode
from apps.storage import getClsObj



class RedisHATool(object):
    CachedResult = None

    def __init__(self, namespace='default', redisdatapath='nfs-provisioner',harbor=None, retrytimes=60):

        namespace = namespace.strip()
        self.RetryTimes = int(retrytimes)
        self.AppInfo = deepcopy(AppInfo)


        self.AppInfo['DataStorageAddr'] = datastoragenode['hostname']
        self.AppInfo['DataStorageBasePath'] = datastoragenode['basepath']
        self.AppInfo['LogStorageAddr'] = logstoragenode['hostname']
        self.AppInfo['LogStorageBasePath'] = logstoragenode['basepath']

        self.AppInfo['Namespace'] = namespace
        self.AppInfo['RedisDataPath'] = os.path.join(self.AppInfo['DataStorageBasePath'], '-'.join([namespace, redisdatapath]))
        self.AppInfo['ProvisionerPath'] = redisdatapath

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


        print ('create Redis HA NFS successfully')
        self.DataStorageObj.createSubFolder(self.AppInfo['RedisDataPath'])


        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['ShellCheckImage'] = replaceDockerRepo(self.AppInfo['ShellCheckImage'], self.AppInfo['HarborAddr'])
        self.AppInfo['RedisImage'] = replaceDockerRepo(self.AppInfo['RedisImage'], self.AppInfo['HarborAddr'])
        self.AppInfo['NFSProvisionerImage'] =replaceDockerRepo(self.AppInfo['NFSProvisionerImage'],
                                                               self.AppInfo['HarborAddr'])
        self.AppInfo['RedisPassword'] = crypto_tools.EncodeBase64(crypto_tools.generateRandomAlphaNumericString(lenght=10))


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
                    with open(os.path.join(basepath, file), mode='rb') as f:
                        TmpContent = f.read()
                    TmpContent = jinja2.Template(TmpContent).render(self.AppInfo)

                    with open(os.path.join(basepath, file), mode='wb') as f:
                        f.write(TmpContent)

        with open(os.path.join(TmpTargetNamespaceDIR, 'values.yaml'), mode='rb', encoding='utf-8') as f:
            self.AppInfo = yaml.safe_load(f)


    def applyYAML(self):
        print ('Create namespace: ' + str(self.AppInfo['Namespace']))
        TmpResponse = self.k8sObj.createNamespace(name=self.AppInfo['Namespace'])
        if TmpResponse['ret_code'] != 0:
            print (TmpResponse)
            return TmpResponse

        print ('setup  NFS provisioner for %s'%(self.AppInfo['AppName'], ))


        TmpNFSProvisionser = nfsprovisioner.NFSProvisionerTool(namespace=self.AppInfo['Namespace'],
                                                               nfsdatapath=self.AppInfo['ProvisionerPath'],
                                                               harbor=self.AppInfo['HarborAddr']
                                                               )

        TmpResponse = TmpNFSProvisionser.start()
        if TmpResponse['ret_code'] != 0:
            print ('failed setup NFS provisioner for %s'%(self.AppInfo['AppName'],))
            return TmpResponse

        print ('setup NFS provisioner for  %s successfully '%(self.AppInfo['AppName'],))


        print ('Apply Redis HA YAML ...')
        TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                             self.AppInfo['AppName'])
        TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


        print ('Apply  Redis HA ....')
        if not self.k8sObj.checkNamespacedResourceHealth(name='redis-ha-server', namespace=self.AppInfo['Namespace'],
                                                         kind='StatefulSet'):
            try:
                self.k8sObj.deleteNamespacedStatefulSet(name='redis-ha-server', namespace=self.AppInfo['Namespace'])
            except:
                pass

            TmpResponse = self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'redis-ha.yaml'),
                                                         namespace=self.AppInfo['Namespace'])
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning=False
        for itime in range(self.RetryTimes):
            TmpResponse = self.k8sObj.getNamespacedStatefulSet(name='redis-ha-server',
                                                                   namespace=self.AppInfo['Namespace'])['result'].to_dict()


            if not self.k8sObj.checkNamespacedResourceHealth(name='redis-ha-server', namespace=self.AppInfo['Namespace'],
                                                         kind='StatefulSet'):
                print ('Waitting for Stateful Set %s to be ready,replicas: %s, available replicas: %s')%(
                    TmpResponse['metadata']['name'], str(TmpResponse['status']['replicas']),
                    str(TmpResponse['status']['ready_replicas'])
                )
                sleep (5)
                continue
            #sleep (20)
            TmpServiceCheckObj = servicestatecheck.ServiceStateCheckTool(namespace=self.AppInfo['Namespace'],
                                                                         harbor=self.AppInfo['HarborAddr'])
            TmpCheckResult = TmpServiceCheckObj.checkServicePortState(targetaddress='redis-ha:6379')
            print ('redis-ha:6379 is listening....')


            print ('Stateful Set: %s is available;replicas: %s')%(TmpResponse['metadata']['name'],
                                                              str(TmpResponse['status']['replicas']))
            isRunning = True
            break

        if not isRunning:
            print ('Failed to apply Stateful Set: %s')%(TmpResponse['metadata']['name'],)
            return {
                'ret_code': 1,
                'result': 'Failed to apply Stateful Set: %s'%(TmpResponse['metadata']['name'],)
            }

        return {
            'ret_code': 0,
            'result': 'Stateful Set: %s is available;replicas: %s'%(TmpResponse['metadata']['name'],
                                                                    str(TmpResponse['status']['replicas']))
        }

    def start(self):
        if RedisHATool.CachedResult:
            print ('Using cached result')
            return RedisHATool.CachedResult

        TmpResponse = self.setupStorage()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        self.renderTemplate()

        TmpResponse = self.applyYAML()
        self.close()

        if TmpResponse['ret_code'] == 0:
            RedisHATool.CachedResult = TmpResponse

        return TmpResponse



    def getValues(self):
        TmpTargetNamespaceDIR = os.path.join(self.BaseDIRPath, 'namespaces', self.AppInfo['Namespace'],
                                             self.AppInfo['AppName'])
        TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


        TmpValuse = None
        if  os.path.isfile(os.path.join(TmpTargetNamespaceDIR, 'values.yaml')):

            with open(os.path.join(TmpTargetNamespaceDIR, 'values.yaml'), mode='rb') as f:
                TmpValuse = yaml.safe_load(f)
        return TmpValuse



    def close(self):
        self.DataStorageObj.close()
        self.LogStorageObj.close




if __name__ == "__main__":
    tmp = RedisHATool(namespace='sly2', nfsinfo=dict(hostname='192.168.0.68', port=22, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
    tmp.start()
