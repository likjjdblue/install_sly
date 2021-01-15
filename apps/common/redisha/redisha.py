#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import nfs
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

class RedisHATool(object):
    def __init__(self, namespace='default', nfsinfo={},redisdatapath='nfs-provisioner',harbor=None, retrytimes=10):

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
        self.AppInfo['Namespace'] = namespace
        self.AppInfo['RedisDataPath'] = os.path.join(self.AppInfo['NFSBasePath'], '-'.join([namespace, redisdatapath]))

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.NFSObj = nfs.NFSTool(**nfsinfo)

    def setupNFS(self):
        TmpResponse = self.NFSObj.installNFS(basedir=self.AppInfo['NFSBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse


        print ('create Redis HA NFS successfully')
        self.NFSObj.createSubFolder(self.AppInfo['RedisDataPath'])


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

            subprocess.Popen('/usr/bin/cp -r resource %s'%(TmpTargetNamespaceDIR,), shell=True)
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

            if TmpResponse['status']['replicas'] != TmpResponse['status']['ready_replicas']:
                print ('Waitting for Deployment %s to be ready,replicas: %s, available replicas: %s') % (
                    TmpResponse['metadata']['name'], str(TmpResponse['status']['replicas']),
                    str(TmpResponse['status']['ready_replicas'])
                )
                sleep(20)
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


            if TmpResponse['status']['replicas'] != TmpResponse['status']['ready_replicas']:
                print ('Waitting for Stateful Set %s to be ready,replicas: %s, available replicas: %s')%(
                    TmpResponse['metadata']['name'], str(TmpResponse['status']['replicas']),
                    str(TmpResponse['status']['ready_replicas'])
                )
                sleep (20)
                continue
            sleep (20)
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
        TmpResponse = self.setupNFS()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        self.renderTemplate()

        TmpResponse = self.applyYAML()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse




if __name__ == "__main__":
    tmp = RedisHATool(namespace='sly2', nfsinfo=dict(hostname='192.168.200.168', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
    tmp.start()
