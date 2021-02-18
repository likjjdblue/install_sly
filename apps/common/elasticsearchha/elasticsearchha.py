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
import yaml, json, httplib
import subprocess
from time import sleep
from tools import k8s_tools
from pprint import pprint
from codecs import open as open
from ESScript import  ESMetaData

def sendHttpRequest(host='127.0.0.1', port=9200, url='/', method='GET', body={}, header={}):
    #### 调用特定的 web API,并获取结果 ###
    ### 函数返回Dict 类型，其中'RetCode'，标识是否异常 0:正常，非0：异常
    ### 'Result'是具体结果

    try:
        if (not isinstance(body, dict)) or (not isinstance(header, dict)):
            raise Exception("需要传入Dict类型，参数调用异常！")

        tmpBody = json.dumps(body)
        HttpObj = httplib.HTTPConnection(host, port)
        HttpObj.request(url=url, method=method, body=tmpBody, headers=header)
        response = json.loads(HttpObj.getresponse().read())
        return {'ret_code': 0,
                'result': response}
    except Exception as e:
        return {'ret_code': 1,
                'result': str(e)}



class ElasticsearchHATool(object):
    CachedResult = None

    def __init__(self, namespace='default', nfsinfo={},elasticsearchdatapath='nfs-provisioner',harbor=None, retrytimes=60):

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
        self.AppInfo['ElasticsearchDataPath'] = os.path.join(self.AppInfo['NFSBasePath'], '-'.join([namespace, elasticsearchdatapath]))
        self.AppInfo['ProvisionerPath'] = elasticsearchdatapath

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


        print ('create Elasticsearch HA NFS successfully')
        self.NFSObj.createSubFolder(self.AppInfo['ElasticsearchDataPath'])


        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['ElasticsearchImage'] = replaceDockerRepo(self.AppInfo['ElasticsearchImage'], self.AppInfo['HarborAddr'])
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

        with open(os.path.join(TmpTargetNamespaceDIR, 'values.yaml'), mode='rb', encoding='utf-8') as f:
            self.AppInfo = yaml.safe_load(f)


    def applyYAML(self):
        print ('Create namespace: ' + str(self.AppInfo['Namespace']))
        TmpResponse = self.k8sObj.createNamespace(name=self.AppInfo['Namespace'])
        if TmpResponse['ret_code'] != 0:
            print (TmpResponse)
            return TmpResponse

        print ('setup  NFS provisioner for %s'%(self.AppInfo['AppName'], ))
        TmpNFSInfo={
            'hostname': self.NFSAddr,
            'port': self.NFSPort,
            'username': self.NFSUsername,
            'password': self.NFSPassword,
            'basepath': self.NFSBasePath,
        }

        TmpNFSProvisionser = nfsprovisioner.NFSProvisionerTool(nfsinfo=TmpNFSInfo, namespace=self.AppInfo['Namespace'],
                                                               nfsdatapath=self.AppInfo['ProvisionerPath'],
                                                               harbor=self.AppInfo['HarborAddr']
                                                               )

        TmpResponse = TmpNFSProvisionser.start()
        if TmpResponse['ret_code'] != 0:
            print ('failed setup NFS provisioner for %s'%(self.AppInfo['AppName'],))
            return TmpResponse

        print ('setup NFS provisioner for  %s successfully '%(self.AppInfo['AppName'],))



        print ('Apply Elasticsearch HA YAML ...')
        TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                             self.AppInfo['AppName'])
        TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


        print ('Apply  Elasticsearch HA ....')
        if not self.k8sObj.checkNamespacedResourceHealth(name='elasticsearch-master', namespace=self.AppInfo['Namespace'],
                                                         kind='StatefulSet'):
            try:
                self.k8sObj.deleteNamespacedStatefulSet(name='elasticsearch-master', namespace=self.AppInfo['Namespace'])
            except:
                pass

            self.k8sObj.createResourceFromYaml(
                filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'elasticsearchha-svc.yaml'),
                namespace=self.AppInfo['Namespace'])

            TmpResponse = self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'elasticsearch-ha.yaml'),
                                                         namespace=self.AppInfo['Namespace'])
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning=False
        for itime in range(self.RetryTimes):
            TmpResponse = self.k8sObj.getNamespacedStatefulSet(name='elasticsearch-master',
                                                                   namespace=self.AppInfo['Namespace'])['result'].to_dict()


            if not self.k8sObj.checkNamespacedResourceHealth(name='elasticsearch-master', namespace=self.AppInfo['Namespace'],
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
            TmpCheckResult = TmpServiceCheckObj.checkServicePortState(targetaddress='elasticsearch-svc:9200')
            print ('elasticsearch-svc:9200 is listening....')

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
        if ElasticsearchHATool.CachedResult:
            print ('Using cached result')
            return ElasticsearchHATool.CachedResult

        TmpResponse = self.setupNFS()
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        self.renderTemplate()

        TmpResponse = self.applyYAML()
        self.close()

        if TmpResponse['ret_code'] == 0:
            ElasticsearchHATool.CachedResult = TmpResponse

        if TmpResponse['ret_code'] == 0:
            TmpResponse = self.createIndex()

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



    def getK8sNodeIP(self):
        TmpRawNodesInfo = self.k8sObj.getNodes()['result'].to_dict()
        for _ in range(1):
            TmpFirstNodeAddress = TmpRawNodesInfo['items'][_]['status']['addresses']

            for _ in TmpFirstNodeAddress:
                if _['type'] == 'InternalIP':
                    return _['address']

    def getServiceNodePort(self):
        TmpResponse = self.k8sObj.getNamespacedService(name='elasticsearch-svc',
                                                       namespace=self.AppInfo['Namespace'])['result'].to_dict()

        #TmpServiceNodePort = int(TmpResponse['spec']['ports'][0]['node_port'])
        TmpServiceNodePortList = TmpResponse['spec']['ports']

        TmpServiceNodePort = None
        for _ in TmpServiceNodePortList:
            if _['port'] == 9200:
                TmpServiceNodePort = _['node_port']
                break

        return int(TmpServiceNodePort)





    def createIndex(self):
        TmpNodeIP = self.getK8sNodeIP()
        TmpPort = self.getServiceNodePort()

        TmpResponse =  sendHttpRequest(host=TmpNodeIP, port=TmpPort, method='PUT', url='/trs_mlf_log',
                        header={'Content-Type':'application/json'}, body=ESMetaData.DictA)

        return TmpResponse





if __name__ == "__main__":
    tmp = ElasticsearchHATool(namespace='sly2', nfsinfo=dict(hostname='192.168.200.74', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
    tmp.start()
