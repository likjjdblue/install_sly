#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
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
from storagenode import datastoragenode, logstoragenode
from apps.storage import getClsObj



class NFSProvisionerTool(object):
    def __init__(self, namespace='default', nfsdatapath='nfs-provisioner',harbor=None, retrytimes=60):

        namespace = namespace.strip()
        self.RetryTimes = int(retrytimes)
        self.AppInfo = deepcopy(AppInfo)

        self.AppInfo['DataStorageAddr'] = datastoragenode['hostname']
        self.AppInfo['DataStorageBasePath'] = datastoragenode['basepath']
        self.AppInfo['LogStorageAddr'] = logstoragenode['hostname']
        self.AppInfo['LogStorageBasePath'] = logstoragenode['basepath']

        self.AppInfo['Namespace'] = namespace
        self.AppInfo['NFSDataPath'] = os.path.join(self.AppInfo['DataStorageBasePath'], '-'.join([namespace, nfsdatapath]))

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.DataStorageObj = getClsObj(datastoragenode['type'])(**datastoragenode)
        self.LogStorageObj = getClsObj(logstoragenode['type'])(**logstoragenode)


    def setupStorage(self):
        TmpResponse = self.DataStorageObj.installStorage(basedir=self.AppInfo['DataStorageBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse


        print ('create  NFS successfully')
        self.DataStorageObj.createSubFolder(self.AppInfo['NFSDataPath'])


        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
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
                    with open(os.path.join(basepath, file), mode='rb') as f:
                        TmpContent = f.read()
                    TmpContent = jinja2.Template(TmpContent).render(self.AppInfo)

                    with open(os.path.join(basepath, file), mode='wb') as f:
                        f.write(TmpContent)

    def applyYAML(self):
        print ('Create namespace: ' + str(self.AppInfo['Namespace']))
        TmpResponse = self.k8sObj.createNamespace(name=self.AppInfo['Namespace'])
        if TmpResponse['ret_code'] != 0:
            print (TmpResponse)
            return TmpResponse

        print ('Apply  RBAC...')
        TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                             self.AppInfo['AppName'])
        TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))

        TmpResponse = self.k8sObj.createResourceFromYaml(
            filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'rbac.yaml'),
            namespace=self.AppInfo['Namespace'])
        if TmpResponse['ret_code'] != 0:
            print (TmpResponse)
            return TmpResponse

        print ('Create ServiceAccount and deploy NFS-Client Provisioner....')
        if not self.k8sObj.checkNamespacedResourceHealth(name='nfs-client-provisioner', kind='Deployment',
                                                         namespace=self.AppInfo['Namespace']):
            print ('NOT health......')
            try:
                self.k8sObj.deleteNamespacedDeployment(name='nfs-client-provisioner',
                                                       namespace=self.AppInfo['Namespace'])
            except:
                pass

            TmpResponse = self.k8sObj.createResourceFromYaml(
                filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'deployment.yaml'),
                namespace=self.AppInfo['Namespace'])
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning = False
        for itime in range(self.RetryTimes):
            TmpResponse = self.k8sObj.getNamespacedDeployment(name='nfs-client-provisioner',
                                                              namespace=self.AppInfo['Namespace'])['result'].to_dict()

            if (TmpResponse['status']['replicas'] != TmpResponse['status']['ready_replicas']) or \
                (TmpResponse['status']['replicas'] is None):
                print ('Waitting for Deployment %s to be ready,replicas: %s, available replicas: %s') % (
                    TmpResponse['metadata']['name'], str(TmpResponse['status']['replicas']),
                    str(TmpResponse['status']['ready_replicas'])
                )
                sleep(5)
                continue
            print ('Deployment: %s is available;replicas: %s') % (TmpResponse['metadata']['name'],
                                                                  str(TmpResponse['status']['replicas']))
            isRunning = True
            break

        if not isRunning:
            print ('Failed to apply Deployment: %s') % (TmpResponse['metadata']['name'],)
            return {
                'ret_code': 1,
                'result': 'Failed to apply Deployment: %s' % (TmpResponse['metadata']['name'],)
            }

        print ('Apply StorageClass.....')
        TmpResponse = self.k8sObj.createResourceFromYaml(
            filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'class.yaml'),
            namespace=self.AppInfo['Namespace'])
        if TmpResponse['ret_code'] != 0:
            print (TmpResponse)
            return {
                'ret_code': 1,
                'result': TmpResponse
            }

        return {
            'ret_code': 0,
            'result': 'setup NFS provisioner successfully '
        }


    def start(self):
        TmpResponse = self.setupStorage()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        self.renderTemplate()

        TmpResponse = self.applyYAML()

        return TmpResponse




if __name__ == "__main__":
    tmp = NFSProvisionerTool(namespace='sly2', nfsinfo=dict(hostname='192.168.200.168', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
    tmp.start()
