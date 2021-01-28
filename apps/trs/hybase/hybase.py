#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import nfs, nfsprovisioner, sqltool
from tools import k8s_tools, ssh_tools
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
import importlib

class TRSIDSTool(object):
    def __init__(self, namespace='default', nfsinfo={},
                 harbor=None, retrytimes=10, *args, **kwargs):

        namespace = namespace.strip()
        kwargs['namespace'] = namespace
        kwargs['nfsinfo'] = nfsinfo
        kwargs['harbor'] = harbor
        self.kwargs = kwargs

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

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.NFSObj = nfs.NFSTool(**nfsinfo)
        self.SSHClient = ssh_tools.SSHTool(**nfsinfo)

        self.DependencyDict ={}
        self.BaseDIRPath= os.path.realpath('../../..')

        if  self.getValues():
            print ('load from file....')
            self.AppInfo = deepcopy(self.getValues())


    def setupNFS(self):
        TmpResponse = self.NFSObj.installNFS(basedir=self.AppInfo['NFSBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        print ('create TRS Hybase NFS successfully')

        #self.NFSObj.createSubFolder(self.AppInfo['TRSIDSDataPath'])


        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['NFSProvisionerImage'] =replaceDockerRepo(self.AppInfo['NFSProvisionerImage'],
                                                               self.AppInfo['HarborAddr'])

        if not self.AppInfo['HyBaseIP']:
            self.AppInfo['HyBaseIP'] = raw_input('input hybase IP Address(e.g 192.168.200.17): ')



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


        print ('Apply TRS Hybase ....')
        TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                                 self.AppInfo['AppName'])
        TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))



        self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'hybase-endpoint.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
        self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'hybase-svc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )


        return {
            'ret_code': 0,
            'result': 'ok',
        }

    def start(self):
        TmpResponse = self.setupNFS()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        self.renderTemplate()

        TmpResponse = self.PreInstall()
        if TmpResponse['ret_code'] != 0:
            print ('Failed to install %s, because of preinstall failure'%(self.AppInfo['AppName'], ))
            return {
                'ret_code': 1,
                'result': 'Failed to install %s, because of preinstall failure'%(self.AppInfo['AppName'], )
            }

        TmpResponse = self.applyYAML()
        if TmpResponse['ret_code'] != 0:
            print ('failed to install TRS IDS')
            return TmpResponse

        print ('install %s successsfully')%(self.AppInfo['AppName'], )
        print ('configging Nginx for %s')%(self.AppInfo['AppName'])
        self.postInstall()

        return {
            'ret_code': 0,
            'result': 'ok'
        }



    def installDependences(self):
        for TmpRawStr in self.AppInfo['dependences']:
            TmpList = TmpRawStr.split('/')
            print (TmpList)
            TmpModuleName, TmpClsName = (TmpList[0], TmpList[1])
            TmpModule = importlib.import_module(TmpModuleName)
            TmpInstance = getattr(TmpModule, TmpClsName)(**self.kwargs)
            TmpResponse = TmpInstance.start()

            if TmpResponse['ret_code'] != 0:
                print ('%s faild to install dependency %s '%(self.AppInfo['AppName'], TmpClsName))
                return TmpResponse

            print ('%s  install dependency %s  successfully' % (self.AppInfo['AppName'], TmpClsName))
            TmpInfo = TmpInstance.getValues()

            if TmpClsName == 'MariaDBTool':
                self.DependencyDict['MariaDBPassword'] = TmpInfo['MariaDBPassword']
            else:
                pass
        return {
            'ret_code': 0,
            'result': 'all dependencies installed'
        }


    def PreInstall(self):
        TmpResponse = self.installDependences()
        if TmpResponse['ret_code'] != 0:
            print ('failed to install %s ,because of dependency failuere'%(self.AppInfo['AppName'], ))
            return {
                'ret_code': 1,
                'result': 'failed to install %s ,because of dependency failuere'%(self.AppInfo['AppName'], )
            }

         ### export mysql SQL ##


        ##### end ###
        return {
            'ret_code': 0,
            'result': '',
        }


    def postInstall(self):
        TmpNginxConfigPath = '-'.join([self.AppInfo['Namespace'], 'nginx-pv-config'])
        TmpNginxConfigPath = os.path.realpath(os.path.join(self.AppInfo['NFSBasePath'], TmpNginxConfigPath))

        print (TmpNginxConfigPath)
        self.SSHClient.ExecCmd('mkdir -p %s' % (TmpNginxConfigPath, ))

        '''
        self.SSHClient.uploadFile(localpath=os.path.join(self.BaseDIRPath, 'downloads', 'trsids.conf'),
                                  remotepath=os.path.join(TmpNginxConfigPath, 'trsids.conf')
                                  )
        '''


        TmpNginxPods = self.k8sObj.filterNamespacedPod(namespace=self.AppInfo['Namespace'], filters={
            "run": "nginx"
        })['result']

        TmpPod = None
        for _ in range(1):
            for pod in TmpNginxPods:
                print ('Config target Nginx POD: '+str(pod.to_dict()['metadata']['name']))
                TmpPod = pod.to_dict()
                break


        self.k8sObj.execNamespacedPod(namespace=self.AppInfo['Namespace'], name=TmpPod['metadata']['name'],
                                      cmd='nginx -s reload'
                                      )


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
    tmp = TRSIDSTool(namespace='sly2', nfsinfo=dict(hostname='192.168.200.168', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))

    print (tmp.start())