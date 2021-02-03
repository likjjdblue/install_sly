#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import nfs, nfsprovisioner, servicestatecheck
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



class MariaDBTool(object):
    CachedResult = None

    def __init__(self, namespace='default', mariadbdatapath='mariadb-pv-data', nfsinfo={},
                 harbor=None, retrytimes=60):

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
        self.AppInfo['MariaDBDataPath'] = os.path.join(self.AppInfo['NFSBasePath'], '-'.join([namespace, mariadbdatapath]))
        self.AppInfo['Namespace'] = namespace

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.NFSObj = nfs.NFSTool(**nfsinfo)

        TmpCWDPath = os.path.abspath(__file__)
        TmpCWDPath = os.path.dirname(TmpCWDPath)
        self.BaseDIRPath= os.path.realpath(os.path.join(TmpCWDPath, '../../..'))

        if  self.getValues():
            print ('load from file....')
            self.AppInfo = deepcopy(self.getValues())

    def setupNFS(self):
        TmpResponse = self.NFSObj.installNFS(basedir=self.AppInfo['NFSBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        print ('create MariaDB NFS successfully')

        '''
        self.NFSObj.createSubFolder(self.AppInfo['MariaDBDataPath'])
        '''

        print ('setup MariaDB NFS successfully')

        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['MariaDBImage'] = replaceDockerRepo(self.AppInfo['MariaDBImage'], self.AppInfo['HarborAddr'])
        self.AppInfo['NFSProvisionerImage'] =replaceDockerRepo(self.AppInfo['NFSProvisionerImage'],
                                                               self.AppInfo['HarborAddr'])
        self.AppInfo['MariaDBPassword'] = crypto_tools.generateRandomAlphaNumericString(lenght=10)

        if not self.AppInfo['MariaDBHostIP']:
            TmpIP = raw_input('input k8s node IP  Address for MariaDB:')
            self.AppInfo['MariaDBHostIP'] = TmpIP.strip()

            print ('Please make sure MariaDB data folder %s@%s  exists!!!'%(self.AppInfo['MariaDBDataPath'], self.AppInfo['MariaDBHostIP']))
            TmpChoice = raw_input('press any key to continue:')



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


        print ('Apply MariaDB ....')
        if not self.k8sObj.checkNamespacedResourceHealth(name='mariadb-deploy', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment'):
            try:
                self.k8sObj.deleteNamespacedDeployment(name='mariadb-deploy', namespace=self.AppInfo['Namespace'])
            except:
                pass

            TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                                 self.AppInfo['AppName'])
            TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))



            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'mariadb-cm.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'mariadb-pv.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'mariadb-pvc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'mariadb-svc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )


            TmpResponse = self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'mariadb-deploy.yaml'),
                                                         namespace=self.AppInfo['Namespace'])
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning=False
        for itime in range(self.RetryTimes):
            TmpResponse = self.k8sObj.getNamespacedDeployment(name='mariadb-deploy',
                                                                   namespace=self.AppInfo['Namespace'])['result'].to_dict()

            if not self.k8sObj.checkNamespacedResourceHealth(name='mariadb-deploy', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment'):
                print ('Waitting for Deployment  %s to be ready,replicas: %s, available replicas: %s')%(
                    TmpResponse['metadata']['name'], str(TmpResponse['status']['replicas']),
                    str(TmpResponse['status']['ready_replicas'])
                )
                sleep (5)
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
        print ('Waitting MariaDB for running....')
        ####sleep(120)

        TmpServiceCheckObj = servicestatecheck.ServiceStateCheckTool(namespace=self.AppInfo['Namespace'], harbor=self.AppInfo['HarborAddr'])
        TmpCheckResult = TmpServiceCheckObj.checkServicePortState(targetaddress='mariadb-svc:3306')
        print ('mariadb-svc:3306 is listening....')


        return {
            'ret_code': 0,
            'result': 'Deployment: %s is available;replicas: %s'%(TmpResponse['metadata']['name'],
                                                                    str(TmpResponse['status']['replicas']))
        }


    def start(self):
        if MariaDBTool.CachedResult:
            print ('Using cached result')
            return MariaDBTool.CachedResult

        TmpResponse = self.setupNFS()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        self.renderTemplate()

        TmpResponse = self.applyYAML()
        self.close()

        if TmpResponse['ret_code'] == 0:
            MariaDBTool.CachedResult = TmpResponse

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
        self.NFSObj.close()





if __name__ == "__main__":
    tmp = MariaDBTool(namespace='sly2', nfsinfo=dict(hostname='192.168.200.168', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
    tmp.start()
