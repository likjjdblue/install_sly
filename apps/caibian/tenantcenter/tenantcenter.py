#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import nfs, nfsprovisioner, nacostool, sqltool
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

class TenantCenterTool(object):
    def __init__(self, namespace='default', tenantcenterlogdata='tenantcenter-pv-log' ,nfsinfo={},
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
        self.AppInfo['TenantCenterLogPath'] = os.path.join(self.AppInfo['NFSBasePath'], '-'.join([namespace, tenantcenterlogdata]))
        self.AppInfo['Namespace'] = namespace

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.NFSObj = nfs.NFSTool(**nfsinfo)
        self.SSHClient = ssh_tools.SSHTool(**nfsinfo)

        self.DependencyDict ={}
        self.BaseDIRPath= os.path.realpath('../../..')

    def setupNFS(self):
        TmpResponse = self.NFSObj.installNFS(basedir=self.AppInfo['NFSBasePath'])
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        print ('create TenantCenter NFS successfully')

        self.NFSObj.createSubFolder((self.AppInfo['TenantCenterLogPath']))

        print ('setup TenantCenter NFS successfully')

        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['TenantCenterImage'] = replaceDockerRepo(self.AppInfo['TenantCenterImage'], self.AppInfo['HarborAddr'])
        self.AppInfo['NFSProvisionerImage'] =replaceDockerRepo(self.AppInfo['NFSProvisionerImage'],
                                                               self.AppInfo['HarborAddr'])
        '''if not self.AppInfo['DDCDBPassword']:
            self.AppInfo['DDCDBPassword'] = crypto_tools.generateRandomAlphaNumericString(lenght=10)
        '''

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


        print ('Apply TenantCenter ....')
        if not self.k8sObj.checkNamespacedResourceHealth(name='tenantcenter-deploy', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment'):
            try:
                self.k8sObj.deleteNamespacedDeployment(name='tenantcenter-deploy', namespace=self.AppInfo['Namespace'])
            except:
                pass

            TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                                 self.AppInfo['AppName'])
            TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))



            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'tenantcenter-cm.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'tenantcenter-svc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'pv/tenantcenter-pv.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'pv/tenantcenter-pvc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )


            TmpResponse = self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'tenantcenter-deploy.yaml'),
                                                         namespace=self.AppInfo['Namespace'])

            #print (os.path.join(TmpTargetNamespaceDIR, 'resource', 'mty-ids-deploy.yaml'))
            #print (os.path.join(TmpTargetNamespaceDIR, 'resource', 'mty-ids-cm.yaml'))
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning=False
        for itime in range(self.RetryTimes):
            TmpResponse = self.k8sObj.getNamespacedDeployment(name='tenantcenter-deploy',
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
        print ('Waitting TenantCenter for running....')
        sleep(120)

        return {
            'ret_code': 0,
            'result': 'Deployment: %s is available;replicas: %s'%(TmpResponse['metadata']['name'],
                                                                    str(TmpResponse['status']['replicas']))
        }

    def start(self):
        TmpResponse = self.setupNFS()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse


        TmpResponse = self.PreInstall()
        if TmpResponse['ret_code'] != 0:
            print ('Failed to install %s, because of preinstall failure'%(self.AppInfo['AppName'], ))
            return {
                'ret_code': 1,
                'result': 'Failed to install %s, because of preinstall failure'%(self.AppInfo['AppName'], )
            }

        self.renderTemplate()

        TmpResponse = self.applyYAML()
        if TmpResponse['ret_code'] != 0:
            print ('failed to install TenantCenter')
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
            elif TmpClsName == 'RedisTool':
                self.AppInfo['PaperReviewRedisPassword'] = TmpInfo['RedisStandAlonePassword']
            #elif TmpClsName == 'RabbitmqHATool':
            #    self.AppInfo['DDCMQPassword'] = crypto_tools.DecodeBase64(TmpInfo['RabbitmqPassword'])

            elif TmpClsName == 'TRSWCMTool':
                self.AppInfo['TenantCenterDBPassword'] = TmpInfo['TRSWCMDBPassword']



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
        '''
        print ('import Mysql SQL file....')
        self.generateValues()
        if not os.path.isdir(os.path.join(self.BaseDIRPath, 'tmp')):
            os.mkdir(os.path.join(self.BaseDIRPath, 'tmp'))

        with open(os.path.join(self.BaseDIRPath, 'tmp', 'account.txt'),mode='wb',encoding='utf-8') as f:
            f.write('root root '+self.DependencyDict['MariaDBPassword']+'\n')
            f.write('%s %s %s'%(self.AppInfo['PaperReviewDBName'], self.AppInfo['PaperReviewDBUser'], self.AppInfo['PaperReviewDBPassword'])+'\n')

        TmpSQLToolAccountPath = '-'.join([self.AppInfo['Namespace'], 'sqltool-pv-account'])
        TmpSQLToolAccountPath = os.path.realpath(os.path.join(self.AppInfo['NFSBasePath'], TmpSQLToolAccountPath))
        TmpSQLToolSQLPath = '-'.join([self.AppInfo['Namespace'], 'sqltool-pv-sql'])
        TmpSQLToolSQLPath = os.path.realpath(os.path.join(self.AppInfo['NFSBasePath'], TmpSQLToolSQLPath))

        print (TmpSQLToolAccountPath)
        print (TmpSQLToolSQLPath)

        self.SSHClient.ExecCmd('mkdir -p %s'%(TmpSQLToolSQLPath, ))
        self.SSHClient.ExecCmd('mkdir -p %s'%(TmpSQLToolAccountPath, ))



        self.SSHClient.ExecCmd('rm -f -r %s/*'%(TmpSQLToolAccountPath, ))
        self.SSHClient.ExecCmd('rm -f -r %s/*'%(TmpSQLToolSQLPath,))

        print (os.path.join(self.BaseDIRPath, 'tmp', 'account.txt'))
        #print (os.path.join(self.BaseDIRPath, 'downloads', 'mty_wcm.sql'))

        self.SSHClient.uploadFile(localpath=os.path.join(self.BaseDIRPath, 'tmp', 'account.txt'),
                                  remotepath=os.path.join(TmpSQLToolAccountPath, 'account.txt')
                                  )

        
        self.SSHClient.uploadFile(localpath=os.path.join(self.BaseDIRPath, 'downloads', 'mty_wcm.sql'),
                                  remotepath=os.path.join(TmpSQLToolSQLPath, 'mty_wcm.sql')
                                  )

        TmpSQLToolObj = sqltool.SQLTool(**self.kwargs)
        TmpResponse = TmpSQLToolObj.start()
        if TmpResponse['ret_code'] != 0:
            print ('Error occured while running SQL Tool')
            return {
                'ret_code': 1,
                'result': 'Error occured while running SQL Tool'
            }


        print ('import Nacos  configuration.....')
        self.generateValues()
        if not os.path.isdir(os.path.join(self.BaseDIRPath, 'tmp')):
            os.mkdir(os.path.join(self.BaseDIRPath, 'tmp'))

        with open(os.path.join(self.BaseDIRPath, 'tmp', 'namespace.txt'),mode='wb',encoding='utf-8') as f:
            f.write('bigdata %s'%(self.AppInfo['PaperReviewNacosID'], )+'\n')

        TmpNacosToolDataPath = '-'.join([self.AppInfo['Namespace'], 'nacostool'])
        TmpNacosToolDataPath = os.path.realpath(os.path.join(self.AppInfo['NFSBasePath'], TmpNacosToolDataPath))


        print (TmpNacosToolDataPath)

        self.SSHClient.ExecCmd('mkdir -p %s'%(TmpNacosToolDataPath, ))



        self.SSHClient.ExecCmd('rm -f -r %s/*'%(TmpNacosToolDataPath, ))


        print (os.path.join(self.BaseDIRPath, 'tmp', 'namespace.txt'))
        #print (os.path.join(self.BaseDIRPath, 'downloads', 'mty_wcm.sql'))

        self.SSHClient.uploadFile(localpath=os.path.join(self.BaseDIRPath, 'tmp', 'namespace.txt'),
                                  remotepath=os.path.join(TmpNacosToolDataPath, 'namespace.txt')
                                  )

        self.SSHClient.uploadFile(localpath=os.path.join(self.BaseDIRPath, 'downloads', 'nacos.tar.gz'),
                                  remotepath=os.path.join(TmpNacosToolDataPath, 'nacos.tar.gz')
                                  )

        self.SSHClient.ExecCmd('cd %s;tar -xvzf nacos.tar.gz'%(TmpNacosToolDataPath, ))

        TmpNacosToolObj = nacostool.NacosTool(**self.kwargs)
        TmpResponse = TmpNacosToolObj.start()
        if TmpResponse['ret_code'] != 0:
            print ('Error occured while running Nacos Tool')
            return {
                'ret_code': 1,
                'result': 'Error occured while running Nacos Tool'
            }
        '''

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

        self.SSHClient.uploadFile(localpath=os.path.join(self.BaseDIRPath, 'downloads', 'tenantcenter.conf'),
                                  remotepath=os.path.join(TmpNginxConfigPath, 'tenantcenter.conf')
                                  )


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
    tmp = TenantCenterTool(namespace='sly2', nfsinfo=dict(hostname='192.168.0.68', port=22, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))

    tmp.start()