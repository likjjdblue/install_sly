#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import nfsprovisioner, sqltool, servicestatecheck
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
from storagenode import datastoragenode, logstoragenode
from apps.storage import getClsObj
from apps import mergeTwoDicts


class TransferVideoTool(object):
    def __init__(self, namespace='default', transfervideolog='transfer-video-pv-log' ,
                 harbor=None, retrytimes=60, *args, **kwargs):

        namespace = namespace.strip()
        kwargs['namespace'] = namespace
        kwargs['harbor'] = harbor
        self.kwargs = kwargs

        self.RetryTimes = int(retrytimes)
        self.AppInfo = deepcopy(AppInfo)

        self.AppInfo['DataStorageAddr'] = datastoragenode['hostname']
        self.AppInfo['DataStorageBasePath'] = datastoragenode['basepath']
        self.AppInfo['LogStorageAddr'] = logstoragenode['hostname']
        self.AppInfo['LogStorageBasePath'] = logstoragenode['basepath']



        self.AppInfo['TransferVideoLogPath'] = os.path.join(self.AppInfo['LogStorageBasePath'], '-'.join([namespace, transfervideolog]))

        self.AppInfo['Namespace'] = namespace

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.DataStorageObj = getClsObj(datastoragenode['type'])(**datastoragenode)
        self.LogStorageObj = getClsObj(logstoragenode['type'])(**logstoragenode)

        self.DependencyDict ={}
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

        print ('create TransferVideo Storage successfully')


        self.LogStorageObj.createSubFolder(self.AppInfo['TransferVideoLogPath'])

        self.TmpStoragePathDict = dict()
        self.TmpStoragePathDict['TransferVideoLogPath'] = self.LogStorageObj.generateRealPath(self.AppInfo['TransferVideoLogPath'])

        print ('setup TransferVideo Storage successfully')

        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['TransferVideoImage'] = replaceDockerRepo(self.AppInfo['TransferVideoImage'], self.AppInfo['HarborAddr'])
        self.AppInfo['NFSProvisionerImage'] =replaceDockerRepo(self.AppInfo['NFSProvisionerImage'], self.AppInfo['HarborAddr'])

        '''
        if not self.AppInfo['TransferVideoPrimaryDBPassword']:
            self.AppInfo['TransferVideoPrimaryDBPassword'] = crypto_tools.generateRandomAlphaNumericString(lenght=10)
        '''

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


        print ('Apply TransferVideo ....')
        if not self.k8sObj.checkNamespacedResourceHealth(name='transfer-video-deploy', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment'):
            try:
                self.k8sObj.deleteNamespacedDeployment(name='transfer-video-deploy', namespace=self.AppInfo['Namespace'])
            except:
                pass

            TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                                 self.AppInfo['AppName'])
            TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))



            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'transfer_video-cm.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'transfer_video-svc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'pv/transfer_video-pv.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )
            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'pv/transfer_video-pvc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )


            TmpResponse = self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'transfer_video-deploy.yaml'),
                                                         namespace=self.AppInfo['Namespace'])

            #print (os.path.join(TmpTargetNamespaceDIR, 'resource', 'mty-ids-deploy.yaml'))
            #print (os.path.join(TmpTargetNamespaceDIR, 'resource', 'mty-ids-cm.yaml'))
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning=False
        for itime in range(self.RetryTimes):
            TmpResponse = self.k8sObj.getNamespacedDeployment(name='transfer-video-deploy',
                                                                   namespace=self.AppInfo['Namespace'])['result'].to_dict()

            if not self.k8sObj.checkNamespacedResourceHealth(name='transfer-video-deploy', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment'):
                print ('Waitting for Deployment  %s to be ready,replicas: %s, available replicas: %s')%(
                    TmpResponse['metadata']['name'], str(TmpResponse['status']['replicas']),
                    str(TmpResponse['status']['ready_replicas'])
                )
                sleep (5)
                continue

            TmpServiceCheckObj = servicestatecheck.ServiceStateCheckTool(namespace=self.AppInfo['Namespace'],
                                                                         harbor=self.AppInfo['HarborAddr'])
            TmpCheckResult = TmpServiceCheckObj.checkServicePortState(targetaddress='transfer-video-svc:56021')
            print ('transfer-video-svc:56021 is listening....')


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

        return {
            'ret_code': 0,
            'result': 'Deployment: %s is available;replicas: %s'%(TmpResponse['metadata']['name'],
                                                                    str(TmpResponse['status']['replicas']))
        }

    def start(self):
        TmpResponse = self.setupStorage()
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
            print ('failed to install TransferVideo')
            return TmpResponse

        print ('install %s successsfully')%(self.AppInfo['AppName'], )
        print ('configging Nginx for %s')%(self.AppInfo['AppName'])
        self.postInstall()
        self.close()

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
            elif TmpClsName == 'RedisHATool':
                self.AppInfo['RedisHAPassword'] = crypto_tools.DecodeBase64(TmpInfo['RedisPassword'])
            elif TmpClsName == 'TransferResourceAITool':
                self.AppInfo['TransferVideoPrimaryDBPassword'] = TmpInfo['TransferResourceAIPrimaryDBPassword']

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
        print ('import Mysql SQL file....')
        self.generateValues()
        if not os.path.isdir(os.path.join(self.BaseDIRPath, 'tmp')):
            os.mkdir(os.path.join(self.BaseDIRPath, 'tmp'))

        with open(os.path.join(self.BaseDIRPath, 'tmp', 'account.txt'),mode='wb',encoding='utf-8') as f:
            f.write('root root '+self.DependencyDict['MariaDBPassword']+'\n')
            f.write('%s %s %s'%(self.AppInfo['TransferVideoPrimaryDBName'], self.AppInfo['TransferVideoPrimaryDBUser'], self.AppInfo['TransferVideoPrimaryDBPassword'])+'\n')

        TmpSQLToolAccountPath = '-'.join([self.AppInfo['Namespace'], 'sqltool-pv-account'])
        TmpSQLToolAccountPath = os.path.realpath(os.path.join(self.AppInfo['DataStorageBasePath'], TmpSQLToolAccountPath))
        TmpSQLToolSQLPath = '-'.join([self.AppInfo['Namespace'], 'sqltool-pv-sql'])
        TmpSQLToolSQLPath = os.path.realpath(os.path.join(self.AppInfo['DataStorageBasePath'], TmpSQLToolSQLPath))

        print (TmpSQLToolAccountPath)
        print (TmpSQLToolSQLPath)

        self.DataStorageObj.createSubFolder(TmpSQLToolSQLPath)
        self.DataStorageObj.createSubFolder(TmpSQLToolAccountPath)



        self.DataStorageObj.cleanSubFolder(TmpSQLToolAccountPath)
        self.DataStorageObj.cleanSubFolder(TmpSQLToolSQLPath)

        print (os.path.join(self.BaseDIRPath, 'tmp', 'account.txt'))
        #print (os.path.join(self.BaseDIRPath, 'downloads', 'tmy_decision_center.sql'))

        self.DataStorageObj.uploadFile(localpath=os.path.join(self.BaseDIRPath, 'tmp', 'account.txt'),
                                  remotepath=os.path.join(TmpSQLToolAccountPath, 'account.txt')
                                  )

        '''
        self.DataStorageObj.uploadFile(localpath=os.path.join(self.BaseDIRPath, 'downloads', 'tmy_decision_center.sql'),
                                  remotepath=os.path.join(TmpSQLToolSQLPath, 'tmy_decision_center.sql')
                                  )
        '''

        TmpSQLToolObj = sqltool.SQLTool(**self.kwargs)
        TmpResponse = TmpSQLToolObj.start()
        if TmpResponse['ret_code'] != 0:
            print ('Error occured while running SQL Tool')
            return {
                'ret_code': 1,
                'result': 'Error occured while running SQL Tool'
            }

        ##### end ###
        return {
            'ret_code': 0,
            'result': '',
        }


    def postInstall(self):
        TmpNginxConfigPath = '-'.join([self.AppInfo['Namespace'], 'nginx-pv-config'])
        TmpNginxConfigPath = os.path.realpath(os.path.join(self.AppInfo['DataStorageBasePath'], TmpNginxConfigPath))

        print (TmpNginxConfigPath)
        self.DataStorageObj.createSubFolder(TmpNginxConfigPath)


        self.DataStorageObj.uploadFile(localpath=os.path.join(self.BaseDIRPath, 'downloads', 'transfervideo.conf'),
                                  remotepath=os.path.join(TmpNginxConfigPath, 'transfervideo.conf')
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
        self.LogStorageObj.close()



if __name__ == "__main__":
    tmp = TransferVideoTool(namespace='sly2', nfsinfo=dict(hostname='192.168.200.74', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))

    tmp.start()
