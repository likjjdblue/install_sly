#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import nfs, nfsprovisioner
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

class CKMTool(object):
    def __init__(self, namespace='default', ckmdatapath='ckm',
                 nfsinfo={},harbor=None, retrytimes=10):

        namespace = namespace.strip()
        self.RetryTimes = int(retrytimes)
        self.NFSAddr = nfsinfo['hostname']
        self.NFSPort = nfsinfo['port']
        self.NFSUsername = nfsinfo['username']
        self.NFSPassword = nfsinfo['password']
        self.NFSBasePath = nfsinfo['basepath']
        self.AppInfo = deepcopy(AppInfo)

        self.AppInfo['NFSAddr'] = self.NFSAddr
        self.AppInfo['NFSBasePath'] = self.NFSBasePath
        self.AppInfo['CKMDataPath'] = os.path.join(self.AppInfo['NFSBasePath'], '-'.join([namespace, ckmdatapath]))


        self.AppInfo['Namespace'] = namespace

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.NFSObj = nfs.NFSTool(**nfsinfo)
        self.SSHObj = ssh_tools.SSHTool(hostname=nfsinfo['hostname'], port=nfsinfo['port'], username=nfsinfo['username'],
                                password=nfsinfo['password'])

    def setupNFS(self):
        TmpResponse = self.NFSObj.installNFS(basedir=self.AppInfo['NFSBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        print ('create CKM NFS successfully')

        self.NFSObj.createSubFolder(self.AppInfo['CKMDataPath'])



        print ('setup CKM NFS successfully')

        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['CKMImage'] = replaceDockerRepo(self.AppInfo['CKMImage'], self.AppInfo['HarborAddr'])
        self.AppInfo['CKMImage'] = replaceDockerRepo(self.AppInfo['CKMImage'], self.AppInfo['HarborAddr'])
        self.AppInfo['NFSProvisionerImage'] =replaceDockerRepo(self.AppInfo['NFSProvisionerImage'],
                                                               self.AppInfo['HarborAddr'])



    def renderTemplate(self):
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


        print ('Apply CKM ....')
        if not self.k8sObj.checkNamespacedResourceHealth(name='ckm', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment'):
            try:
                self.k8sObj.deleteNamespacedDeployment(name='ckm', namespace=self.AppInfo['Namespace'])
            except:
                pass

            TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                                 self.AppInfo['AppName'])
            TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'ckm-pv-pvc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )



            TmpResponse = self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource',
                                                        'ckm-deploy.yaml'),namespace=self.AppInfo['Namespace'])
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning=False
        for itime in range(self.RetryTimes):
            TmpResponse = self.k8sObj.getNamespacedDeployment(name='ckm',
                                                                   namespace=self.AppInfo['Namespace'])['result'].to_dict()

            if (TmpResponse['status']['replicas'] != TmpResponse['status']['ready_replicas']) and \
                   (TmpResponse['status']['replicas'] is not None):
                print ('Waitting for Deployment  %s to be ready,replicas: %s, available replicas: %s')%(
                    TmpResponse['metadata']['name'], str(TmpResponse['status']['replicas']),
                    str(TmpResponse['status']['ready_replicas'])
                )
                sleep (20)
                continue
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
        print ('Waitting CKM for running....')
        sleep(30)

        return {
            'ret_code': 0,
            'result': 'Deployment: %s is available;replicas: %s'%(TmpResponse['metadata']['name'],
                                                                    str(TmpResponse['status']['replicas']))
        }

    def start(self):
        TmpResponse = self.setupNFS()
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
    tmp = CKMTool(namespace='sly2', nfsinfo=dict(hostname='192.168.0.68', port=22, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
    tmp.start()