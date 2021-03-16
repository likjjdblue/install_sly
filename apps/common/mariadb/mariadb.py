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
from apps import mergeTwoDicts
import storagenode


def installMysqlDriver4Python():
    TmpCWDPath = os.path.abspath(__file__)
    TmpCWDPath = os.path.dirname(TmpCWDPath)
    TmpCWDPath = os.path.join(TmpCWDPath, 'rpm')


    try:
        import mysql.connector
    except:
        subprocess.call('rpm -Uvh --force %s/mysql-connector-python-2.1.7-1.el7.x86_64.rpm'%(TmpCWDPath, ),
                        shell=True)
        import mysql.connector


def checkMysqlConnection(mysqlhost, mysqlport, mysqluser, mysqlpassword):
    try:
        import mysql.connector
        ConnObj=mysql.connector.connect(host=mysqlhost.strip(),
                                        port=str(mysqlport).strip(),
                                        user=str(mysqluser).strip(),
                                        password=str(mysqlpassword).strip(),
                                        connection_timeout=3)
        CursorObj=ConnObj.cursor()
        CursorObj.execute('use mysql;')
        print ('External Mysql is available')
        return {
            'ret_code': 0,
            'result': 'External Mysql check result good'
        }
    except Exception as e:
        print ('External Mysql not available')
        return {
            'ret_code': 1,
            'result': 'External Mysql check result bad'
        }




class MariaDBTool(object):
    CachedResult = None

    def __init__(self, namespace='default', mariadbdatapath='mariadb-pv-data',
                 harbor=None, retrytimes=60):

        namespace = namespace.strip()
        self.RetryTimes = int(retrytimes)
        self.AppInfo = deepcopy(AppInfo)


        self.AppInfo['DataStorageAddr'] = datastoragenode['hostname']
        self.AppInfo['DataStorageBasePath'] = datastoragenode['basepath']
        self.AppInfo['LogStorageAddr'] = logstoragenode['hostname']
        self.AppInfo['LogStorageBasePath'] = logstoragenode['basepath']

        #self.AppInfo['MariaDBDataPath'] = os.path.join(self.AppInfo['DataStorageBasePath'], '-'.join([namespace, mariadbdatapath]))


        ### MariaDB data path not changeable   ###
        self.AppInfo['MariaDBDataPath'] = os.path.join('/TRS/DATA', '-'.join([namespace, mariadbdatapath]))
        self.AppInfo['Namespace'] = namespace

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()

        #self.DataStorageObj = getClsObj(datastoragenode['type'])(**datastoragenode)
        #self.LogStorageObj = getClsObj(logstoragenode['type'])(**logstoragenode)

        TmpCWDPath = os.path.abspath(__file__)
        TmpCWDPath = os.path.dirname(TmpCWDPath)
        self.BaseDIRPath= os.path.realpath(os.path.join(TmpCWDPath, '../../..'))

        if  self.getValues():
            print ('load from file....')
            self.AppInfo = deepcopy(self.getValues())

    def setupStorage(self):
        self.TmpStoragePathDict = dict()

        if hasattr(storagenode, 'externalMariadbnode'):
            return {
                'ret_code': 0,
                'result': ''
            }

        print ('create MariaDB Storage successfully')

        '''
        self.NFSObj.createSubFolder(self.AppInfo['MariaDBDataPath'])
        '''


        #self.TmpStoragePathDict['MariaDBDataPath'] = self.DataStorageObj.generateRealPath(self.AppInfo['MariaDBDataPath'])

        print ('setup MariaDB Storage successfully')

        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['MariaDBImage'] = replaceDockerRepo(self.AppInfo['MariaDBImage'], self.AppInfo['HarborAddr'])
        self.AppInfo['NFSProvisionerImage'] =replaceDockerRepo(self.AppInfo['NFSProvisionerImage'],
                                                               self.AppInfo['HarborAddr'])

        if not hasattr(storagenode, 'externalMariadbnode'):
            self.AppInfo['MariaDBPassword'] = crypto_tools.generateRandomAlphaNumericString(lenght=10)
        else:
            installMysqlDriver4Python()

            from storagenode import externalMariadbnode
            TmpMysqlCheckResult = checkMysqlConnection(**externalMariadbnode)
            if TmpMysqlCheckResult['ret_code'] != 0:
                print (TmpMysqlCheckResult['result'])
                print ('Fatal Error, Quit....')
                raise Exception('External Mysql  check result bad')

            self.AppInfo['MariaDBHostIP'] = str(externalMariadbnode['mysqlhost']).strip()
            self.AppInfo['MariaDBHostPort'] = str(externalMariadbnode['mysqlport']).strip()
            self.AppInfo['MariaDBUser'] = str(externalMariadbnode['mysqluser']).strip()
            self.AppInfo['MariaDBPassword'] = str(externalMariadbnode['mysqlpassword'])


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

        subprocess.call('mkdir -p %s'%(os.path.join(TmpTargetNamespaceDIR, 'resource')), shell=True)

        if not os.path.isfile(os.path.join(TmpTargetNamespaceDIR, 'values.yaml')):
            self.generateValues()

            TmpAppInfo = mergeTwoDicts(self.AppInfo, self.TmpStoragePathDict)

            with open(os.path.join(TmpTargetNamespaceDIR, 'values.yaml'), mode='wb') as f:
                yaml.safe_dump(TmpAppInfo, f)

            TmpCWDPath = os.path.abspath(__file__)
            TmpCWDPath = os.path.dirname(TmpCWDPath)

            TmpNoneExternalTargetFiles = ['mariadb-cm.yaml', 'mariadb-deploy.yaml', 'mariadb-pv.yaml',
                                          'mariadb-pvc.yaml', 'mariadb-svc.yaml',
                                          ]

            TmpExternalTargetFiles = ['mariadb-svc-external.yaml', 'mariadb-endpoint.yaml']



            if hasattr(storagenode, 'externalMariadbnode'):
                for file in TmpExternalTargetFiles:
                    print ('copyint file: %s')%(file, )
                    subprocess.Popen('/usr/bin/cp  %s %s' % (os.path.join(TmpCWDPath, 'resource', file),
                                                               os.path.join(TmpTargetNamespaceDIR, 'resource', file)), shell=True)
            elif not hasattr(storagenode, 'externalMariadbnode'):
                for file in TmpNoneExternalTargetFiles:
                    print ('copyint file: %s')%(file, )
                    subprocess.Popen('/usr/bin/cp  %s %s' % (os.path.join(TmpCWDPath, 'resource', file),
                                                               os.path.join(TmpTargetNamespaceDIR, 'resource', file)), shell=True)


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


        print ('Apply MariaDB ....')
        isRunning = False

        if (not self.k8sObj.checkNamespacedResourceHealth(name='mariadb-deploy', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment')) \
                    and (not hasattr(storagenode, 'externalMariadbnode')):
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

        elif hasattr(storagenode, 'externalMariadbnode'):
            TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                                 self.AppInfo['AppName'])
            TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))

            self.k8sObj.createResourceFromYaml(
                filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'mariadb-svc-external.yaml'),
                namespace=self.AppInfo['Namespace']
                )


            self.k8sObj.deleteNamespacedEndpoint(name='mariadb-svc', namespace=self.AppInfo['Namespace'])

            self.k8sObj.createResourceFromYaml(
                filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'mariadb-endpoint.yaml'),
                namespace=self.AppInfo['Namespace']
                )
            isRunning = True





        for itime in range(self.RetryTimes):
            if isRunning:
                break

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

        if hasattr(storagenode, 'externalMariadbnode'):
            return {
                'ret_code': 0,
                'result': 'External Mysql is available now',
            }



        return {
            'ret_code': 0,
            'result': 'Deployment: %s is available;replicas: %s'%(TmpResponse['metadata']['name'],
                                                                    str(TmpResponse['status']['replicas']))
        }


    def start(self):
        if MariaDBTool.CachedResult:
            print ('Using cached result')
            return MariaDBTool.CachedResult

        TmpResponse = self.setupStorage()
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
        pass





if __name__ == "__main__":
    tmp = MariaDBTool(namespace='sly2', nfsinfo=dict(hostname='192.168.200.168', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
    tmp.start()
