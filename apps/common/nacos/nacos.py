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

class NacosTool(object):
    def __init__(self, namespace='default', mysqldatapath='nacos_mysql', nacosdatapath='nfs-provisioner', nfsinfo={},
                 harbor=None):

        namespace = namespace.strip()
        self.NFSAddr = nfsinfo['hostname']
        self.NFSPort = nfsinfo['port']
        self.NFSUsername = nfsinfo['username']
        self.NFSPassword = nfsinfo['password']
        self.NFSBasePath = nfsinfo['basepath']
        self.AppInfo = deepcopy(AppInfo)


        self.AppInfo['NFSAddr'] = self.NFSAddr
        self.AppInfo['NFSBasePath'] = self.NFSBasePath
        self.AppInfo['MysqlDataPath'] = os.path.join(self.AppInfo['NFSBasePath'], '-'.join([namespace, mysqldatapath]))
        self.AppInfo['NacosDataPath'] = os.path.join(self.AppInfo['NFSBasePath'], '-'.join([namespace, nacosdatapath]))
        self.AppInfo['Namespace'] = namespace

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.NFSObj = nfs.NFSTool(**nfsinfo)

    def setupNFS(self):
        TmpResponse = self.NFSObj.installNFS(basedir=AppInfo['NFSBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        print ('create NACOS NFS successfully')

        self.NFSObj.createSubFolder(self.AppInfo['MysqlDataPath'])
        self.NFSObj.createSubFolder(self.AppInfo['NacosDataPath'])

        print ('setup NACOS NFS successfully')

        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['NacosImage'] = replaceDockerRepo(self.AppInfo['NacosImage'], self.AppInfo['Namespace'])
        self.AppInfo['MysqlImage'] = replaceDockerRepo(self.AppInfo['MysqlImage'], self.AppInfo['Namespace'])
        self.AppInfo['NFSProvisionerImage'] =replaceDockerRepo(self.AppInfo['NFSProvisionerImage'],
                                                               self.AppInfo['Namespace'])
        self.AppInfo['MysqlPassword'] = crypto_tools.generateRandomString(lenght=10)


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

            subprocess.Popen('/usr/bin/cp -r resource/* %s'%(TmpTargetNamespaceDIR,), shell=True)
            sleep (5)

            for basepath, _, files in os.walk(TmpTargetNamespaceDIR):
                for file in files:
                    TmpContent = ''
                    with open(os.path.join(basepath, file), mode='rb') as f:
                        TmpContent = f.read()
                    TmpContent = jinja2.Template(TmpContent).render(self.AppInfo)

                    with open(os.path.join(basepath, file), mode='wb') as f:
                        f.write(TmpContent)

    def applyYAML(self):
        pass















tmp = NacosTool(namespace='sly', nfsinfo=dict(hostname='192.168.200.168', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
print (tmp.setupNFS())
print (tmp.renderTemplate())