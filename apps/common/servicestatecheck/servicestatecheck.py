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
import yaml, json
import subprocess, httplib
from time import sleep
from tools import k8s_tools
from pprint import pprint
from codecs import open as open


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


class ServiceStateCheckTool(object):
    def __init__(self, namespace='default', harbor=None, retrytimes=10):

        namespace = namespace.strip()
        self.RetryTimes = int(retrytimes)
        self.AppInfo = deepcopy(AppInfo)

        self.AppInfo['Namespace'] = namespace

        self.AppInfo['HarborAddr'] = harbor
        self.k8sObj = k8s_tools.K8SClient()


        TmpCWDPath = os.path.abspath(__file__)
        TmpCWDPath = os.path.dirname(TmpCWDPath)
        self.BaseDIRPath= os.path.realpath(os.path.join(TmpCWDPath, '../../..'))

        if  self.getValues():
            print ('load from file....')
            self.AppInfo = deepcopy(self.getValues())

    def setupNFS(self):
        return {
            'ret_code': 0,
            'result': ''
        }

    def generateValues(self):
        self.AppInfo['ServiceStateCheckImage'] = replaceDockerRepo(self.AppInfo['ServiceStateCheckImage'], self.AppInfo['HarborAddr'])
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


        print ('Apply ServiceStateCheck ....')
        if not self.k8sObj.checkNamespacedResourceHealth(name='service-state-check-deploy', namespace=self.AppInfo['Namespace'],
                                                         kind='Deployment'):
            try:
                self.k8sObj.deleteNamespacedDeployment(name='service-state-check-deploy', namespace=self.AppInfo['Namespace'])
            except:
                pass

            TmpTargetNamespaceDIR = os.path.join(self.AppInfo['TargetNamespaceDIR'], self.AppInfo['Namespace'],
                                                 self.AppInfo['AppName'])
            TmpTargetNamespaceDIR = os.path.normpath(os.path.realpath(TmpTargetNamespaceDIR))


            self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource', 'service_state_check-svc.yaml'),
                                               namespace=self.AppInfo['Namespace']
                                               )


            TmpResponse = self.k8sObj.createResourceFromYaml(filepath=os.path.join(TmpTargetNamespaceDIR, 'resource',
                                                        'service_state_check-deploy.yaml'),namespace=self.AppInfo['Namespace'])
            if TmpResponse['ret_code'] != 0:
                print (TmpResponse)
                return TmpResponse

        isRunning=False
        for itime in range(self.RetryTimes):
            TmpResponse = self.k8sObj.getNamespacedDeployment(name='service-state-check-deploy',
                                                                   namespace=self.AppInfo['Namespace'])['result'].to_dict()

            if (TmpResponse['status']['replicas'] != TmpResponse['status']['ready_replicas']) and \
                   (TmpResponse['status']['replicas'] is not None):
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
        print ('Waitting ServiceStateCheck for running....')
        sleep(3)

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
        self.close()

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

    def getK8sNodeIP(self):
        TmpRawNodesInfo = self.k8sObj.getNodes()['result'].to_dict()
        for _ in range(1):
            TmpFirstNodeAddress = TmpRawNodesInfo['items'][_]['status']['addresses']

            for _ in TmpFirstNodeAddress:
                if _['type'] == 'InternalIP':
                    return _['address']

    def getServiceNodePort(self):
        TmpResponse = self.k8sObj.getNamespacedService(name='service-state-check-svc',
                                                       namespace=self.AppInfo['Namespace'])['result'].to_dict()

        TmpServiceNodePort = int(TmpResponse['spec']['ports'][0]['node_port'])
        return TmpServiceNodePort


    def checkServicePortState(self, targetaddress):
        self.start()

        TmpNodeIP = self.getK8sNodeIP()
        TmpNodePort = self.getServiceNodePort()

        TmpHttpResponse = sendHttpRequest(host=TmpNodeIP, port=int(TmpNodePort), method='POST',
                                          body={'endpoints': [targetaddress]}, url='/checkservice',
                                          header={'Content-Type': "application/json"}
                                          )

        self.close()

        print (TmpHttpResponse['result'])
        return TmpHttpResponse['result']









if __name__ == "__main__":
    tmp = ServiceStateCheckTool(namespace='sly2')
    tmp.start()
    tmp.checkServicePortState(targetaddress='mariadb-svc:3306')

