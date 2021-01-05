#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from kubernetes import client, config
import os, yaml

class K8SClient(object):
    def __init__(self):
        config.load_kube_config()
        self.K8SAppsV1Client = client.AppsV1Api()
        self.K8SCoreV1Client = client.CoreV1Api()


    def getDeploymentFromNamespace(self, deployment=None, namespace='default'):
        try:
            TmpResponse = self.K8SAppsV1Client.read_namespaced_deployment_status(name=deployment, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (e)
            return  {
                "ret_code": 1,
                'result': "Deployment %s or Namespace %s not exists"%(deployment, namespace)
            }


    def checkNamespacedDeploymentState(self,deployment=None, namespace='default'):
        try:
            TmpResponse = self.K8SAppsV1Client.read_namespaced_deployment_status(name=deployment, namespace=namespace)
            TmpResult = 'ready' if TmpResponse.status.replicas == TmpResponse.status.ready_replicas else 'not ready'
            return {
                "ret_code": 0,
                'result': TmpResult
            }
        except Exception as e:
            print (e)
            return  {
                "ret_code": 1,
                'result': "Deployment %s or Namespace %s not exists"%(deployment, namespace)
            }

    def createNamespacedDeploymentFromYAML(self, filepath='', namespace='default' ):
        TmpNamespaceObj = self.createNamespace(namespace=namespace)
        if TmpNamespaceObj['ret_code'] != 0:
            return {
                "ret_code": 1,
                'result': "Can not create namespace: %s,%s"%(namespace,TmpNamespaceObj['result'])
            }

        if not os.path.isfile(filepath):
            return {
                "ret_code": 1,
                'result': "%s is not a file path"
            }

        try:
            with open(filepath, mode='rb') as f:
                TmpYAMLContent=yaml.safe_load(f)
                TmpResponse = self.K8SAppsV1Client.create_namespaced_deployment(
                    body=TmpYAMLContent, namespace=namespace
                )
                return {
                    "ret_code": 0,
                    'result': TmpResponse
                }
        except Exception as e:
            return {
                "ret_code": 1,
                'result': str(e)
            }

    def deleteNamespacedDeployment(self, deployment='', namespace='default'):
        TmpDeployment = self.getDeploymentFromNamespace(deployment=deployment, namespace=namespace)
        if TmpDeployment['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'deployment object deleted'
            }

        self.K8SAppsV1Client.delete_namespaced_deployment(name=deployment, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'deployment object deleted'
        }

    def getNamespace(self, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.list_namespace()
            for item in TmpResponse.items:
                if item.metadata.name == namespace:
                    return {
                        "ret_code": 0,
                        "result": item
                    }

            return {
                 "ret_code": 0,
                 "result": None
             }
        except Exception as e:
            return {
                "ret_code": 1,
                'result': str(e)
            }

    def createNamespace(self, namespace='default'):
        TmpResult = self.getNamespace(namespace=namespace)
        if TmpResult['ret_code'] != 0 or TmpResult['result'] is  None:
            try:
                TmpResult = self.K8SCoreV1Client.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace)))
            except Exception as e:
                return {
                    "ret_code": 1,
                    'result': str(e)
                }

        return {
            "ret_code": 0,
            'result': TmpResult
        }




TmpObj = K8SClient()
#print (TmpObj.GetDeploymentFromNamespace(deployment='redis', namespace='slytest'))
#print (TmpObj.checkNamespacedDeploymentState(deployment='redis', namespace='slytest'))
#print (TmpObj.createNamespace('wakaka'))
print (TmpObj.createNamespacedDeploymentFromYAML('redis/deployment.yaml'))

print (TmpObj.deleteNamespacedDeployment(deployment='redis'))


