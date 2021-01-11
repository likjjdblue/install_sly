#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from kubernetes import client, config
import os, yaml
from kubernetes.stream import stream
from kubernetes.utils import create_from_dict
from time import sleep


class K8SClient(object):
    def __init__(self):
        config.load_kube_config()
        self.K8SAppsV1Client = client.AppsV1Api()
        self.K8SCoreV1Client = client.CoreV1Api()
        self.K8SStorageV1Client = client.StorageV1Api()
        self.K8SRbacAuthorizationV1Client = client.RbacAuthorizationV1Api()



    def getNamespacedDeployment(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SAppsV1Client.read_namespaced_deployment_status(name=name, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (e)
            return  {
                "ret_code": 1,
                'result': "Deployment %s or Namespace %s not exists"%(name, namespace)
            }



    def deleteNamespacedDeployment(self, name, namespace='default'):
        TmpDeployment = self.getNamespacedDeployment(name=name, namespace=namespace)
        if TmpDeployment['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'deployment object deleted'
            }

        self.K8SAppsV1Client.delete_namespaced_deployment(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'deployment object deleted'
        }

    def getNamespace(self, name='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.list_namespace()
            for item in TmpResponse.items:
                if item.metadata.name == name:
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

    def createNamespace(self, name='default'):
        TmpResult = self.getNamespace(name=name)
        if TmpResult['ret_code'] != 0 or TmpResult['result'] is  None:
            try:
                TmpResult = self.K8SCoreV1Client.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name=name)))
            except Exception as e:
                return {
                    "ret_code": 1,
                    'result': str(e)
                }

        return {
            "ret_code": 0,
            'result': TmpResult
        }


    def getNamespacedService(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_service(name=name, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or SVC %s  not exists'%(namespace, name)
            }

    def deleteNampespacedService(self, name, namespace='default'):
        TmpSVC = self.getNamespacedService(name=name, namespace=namespace)
        if TmpSVC['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'SVC object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_service(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'SVC object deleted'
        }


    def getNamespacedConfigMap(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_config_map(name=name, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or ConfigMap %s  not exists'%(namespace, name)
            }

    def deleteNampespacedConfigMap(self, name, namespace='default'):
        TmpSVC = self.getNamespacedConfigMap(name=name, namespace=namespace)
        if TmpSVC['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ConfigMap object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_config_map(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'ConfigMap object deleted'
        }

    def getNamespacedSecret(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_secret(name=name, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or Secret %s  not exists'%(namespace, name)
            }

    def deleteNamespacedSecret(self, name, namespace='default'):
        TmpSecret = self.getNamespacedSecret(name=name, namespace=namespace)
        if TmpSecret['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'Secret object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_secret(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'Secret object deleted'
        }

    def getPersistentVolume(self, name):
        try:
            TmpResponse = self.K8SCoreV1Client.read_persistent_volume(name=name)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'PV %s  not exists'%(name,)
            }

    def deletePersistentVolume(self, name):
        TmpPV = self.getPersistentVolume(name=name)
        if TmpPV['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'PV object deleted'
            }

        self.K8SCoreV1Client.delete_persistent_volume(name=name)
        return {
            "ret_code": 0,
            'result': 'PV object deleted'
        }

    def getNamespacedPersistentVolumeClaim(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_persistent_volume_claim(name=name, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or PVC %s  not exists'%(namespace, name)
            }

    def deleteNamespacedPersistentVolumeClaim(self, name, namespace='default'):
        TmpSecret = self.getNamespacedPersistentVolumeClaim(name=name, namespace=namespace)
        if TmpSecret['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'PVC object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_persistent_volume_claim(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'PVC object deleted'
        }

    def getNamespacedStatefulSet(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SAppsV1Client.read_namespaced_stateful_set(name=name, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (e)
            return  {
                "ret_code": 1,
                'result': "StatefulSet %s or Namespace %s not exists"%(name, namespace)
            }

    def deleteNamespacedStatefulSet(self, name, namespace='default'):
        TmpStatefulSet = self.getNamespacedStatefulSet(name=name, namespace=namespace)
        if TmpStatefulSet['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'statefulset object deleted'
            }

        self.K8SAppsV1Client.delete_namespaced_stateful_set(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'statefulset object deleted'
        }

    def getNamespacedReplicationController(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_replication_controller(name=name,
                                                                                      namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or ReplicationControler %s  not exists'%(namespace, name)
            }

    def deleteNamespacedReplicationController(self, name, namespace='default'):
        TmpReplicationControler = self.getNamespacedReplicationController(name=name,
                                                           namespace=namespace)
        if TmpReplicationControler['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ReplicationControler object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_replication_controller(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'ReplicationControler object deleted'
        }

    def getStorageClass(self, name):
        try:
            TmpResponse = self.K8SStorageV1Client.read_storage_class(name=name)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'StorageClass %s  not exists'%(name,)
            }

    def deleteStorageClass(self, name):
        TmpStorageClass = self.getStorageClass(name=name)
        if TmpStorageClass['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'StorageClass object deleted'
            }

        self.K8SStorageV1Client.delete_storage_class(name=name)
        return {
            "ret_code": 0,
            'result': 'StorageClass object deleted'
        }

    def getNamespacedServiceAccount(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_service_account(name=name,
                                                                               namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or ServiceAccount %s  not exists'%(namespace, name)
            }

    def deleteNamespacedServiceAccount(self, name, namespace='default'):
        TmpServiceAccount = self.getNamespacedServiceAccount(name=name, namespace=namespace)
        if TmpServiceAccount['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ServiceAccount object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_service_account(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'ServiceAccount object deleted'
        }


    def getClusterRole(self, name):
        try:
            TmpResponse = self.K8SRbacAuthorizationV1Client.read_cluster_role(name=name)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'CLusterRole %s  not exists'%(name,)
            }

    def deleteClusterRole(self, name):
        TmpClusterRole = self.getClusterRole(name=name)
        if TmpClusterRole['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ClusterRole object deleted'
            }

        self.K8SRbacAuthorizationV1Client.delete_cluster_role(name=name)
        return {
            "ret_code": 0,
            'result': 'ClusterRole object deleted'
        }



    def getClusterRoleBinding(self, name):
        try:
            TmpResponse = self.K8SRbacAuthorizationV1Client.read_cluster_role_binding(name=name)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'CLusterRoleBinding %s  not exists'%(name,)
            }

    def deleteClusterRoleBinding(self, name):
        TmpClusterRoleBinding = self.getClusterRoleBinding(name=name)
        if TmpClusterRoleBinding['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ClusterRoleBinding object deleted'
            }

        self.K8SRbacAuthorizationV1Client.delete_cluster_role_binding(name=name)
        return {
            "ret_code": 0,
            'result': 'ClusterRoleBinding object deleted'
        }



    def getNamespacedRole(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SRbacAuthorizationV1Client.read_namespaced_role(name=name, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or Role %s  not exists'%(namespace, name)
            }

    def deleteNamespacedRole(self, name, namespace='default'):
        TmpRole = self.getNamespacedRole(name=name, namespace=namespace)
        if TmpRole['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'Role object deleted'
            }

        self.K8SRbacAuthorizationV1Client.delete_namespaced_role(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'Role object deleted'
        }


    def getNamespacedRoleBinding(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SRbacAuthorizationV1Client.read_namespaced_role_binding(name=name,
                                                                                         namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or RoleBinding %s  not exists'%(namespace, name)
            }

    def deleteNamespacedRoleBinding(self, name, namespace='default'):
        TmpRoleBinding = self.getNamespacedRoleBinding(name=name, namespace=namespace)
        if TmpRoleBinding['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'RoleBinding object deleted'
            }

        self.K8SRbacAuthorizationV1Client.delete_namespaced_role_binding(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'RoleBinding object deleted'
        }


    def getNamespacedPod(self, name, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_pod(name=name,namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or Pod %s  not exists'%(namespace, name)
            }

    def deleteNamespacedPod(self, name, namespace='default'):
        TmpPod = self.getNamespacedPod(name=name, namespace=namespace)
        if TmpPod['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'Pod object deleted'
            }

        self.K8SRbacAuthorizationV1Client.delete_namespaced_pod(name=name, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'Pod object deleted'
        }

    def filterNamespacedPod(self, filters={}, namespace='default'):
        TmpFilterList = [str(key)+'='+str(value) for key, value in filters.iteritems()]
        TmpFilterStr = ','.join(TmpFilterList)
        try:
            TmpResponse = self.K8SCoreV1Client.list_namespaced_pod(namespace=namespace, label_selector=TmpFilterStr)
            return {
                'ret_code': 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code": 0,
                'result': TmpResponse.items
            }

    def execNamespacedPod(self, name,namespace='default',cmd=''):
        try:
            TmpCmdList=cmd.split()
            TmpResponse = stream(self.K8SCoreV1Client.connect_get_namespaced_pod_exec,
                                 name=name, namespace=namespace, command=TmpCmdList, stderr=True, stdin=False,
                                 stdout=True, tty=True)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }

        except Exception as e:
            print (str(e))
            return {
                "ret_code": 0,
                'result': str(e)
            }

    def createResourceFromYaml(self,filepath, namespace='default'):
        TmpObjectDict = {
            "created_objs": [],
            "failed_objs": [],
        }
        if not os.path.isfile(os.path.abspath(filepath)):
            return {
                "ret_code": 1,
                'result': "file %s not exists"%(filepath,)
            }
        with open(os.path.abspath(filepath), mode='rb') as f:
            try:
                TmpYAMLDocs = yaml.safe_load_all(f)
                for doc in TmpYAMLDocs:
                    if not doc:
                        continue
                    print ('current kind: '+str(doc['kind'])+ ' name: '+str(doc['metadata']['name']))

                    RawNamespacedFuncName = 'getNamespaced'+doc['kind']
                    RawNoneNamespacedFuncName = 'get'+doc['kind']

                    if hasattr(self, RawNamespacedFuncName):
                        TmpResponse = getattr(self, RawNamespacedFuncName)(name=doc['metadata']['name'],
                                                                           namespace=namespace)
                        if TmpResponse['ret_code'] == 0:
                            TmpObjectDict['created_objs'].append(TmpResponse)
                            continue
                    elif hasattr(self, RawNoneNamespacedFuncName):
                        TmpResponse = getattr(self,RawNoneNamespacedFuncName)(name=doc['metadata']['name'])
                        if TmpResponse['ret_code'] == 0:
                            TmpObjectDict['created_objs'].append(TmpResponse)
                            continue

                    try:
                        TmpResponse = create_from_dict(k8s_client=client.ApiClient(), data=doc, namespace=namespace)
                        TmpObjectDict['created_objs'].append(TmpResponse)
                    except Exception as e:
                        print (str(e))
                        TmpObjectDict['failed_objs'].append(doc)

                return {
                    'ret_code': 0,
                    'result': TmpObjectDict
                }
            except Exception as e:
                print (str(e))
                return {
                    'ret_code': 1,
                    'result': str(e)
                }


    def deleteResourceFromYaml(self,filepath, namespace='default'):
        TmpObjectDict = {
            "deleted_objs": [],
            "failed_objs": [],
        }
        if not os.path.isfile(os.path.abspath(filepath)):
            return {
                "ret_code": 1,
                'result': "file %s not exists"%(filepath,)
            }
        with open(os.path.abspath(filepath), mode='rb') as f:
            try:
                TmpYAMLDocs = yaml.safe_load_all(f)
                for doc in TmpYAMLDocs:
                    if not doc:
                        continue
                    print ('current kind: '+str(doc['kind'])+ ' name: '+str(doc['metadata']['name']))

                    RawNamespacedFuncName = 'deleteNamespaced'+doc['kind']
                    RawNoneNamespacedFuncName = 'delete'+doc['kind']

                    print (RawNamespacedFuncName)
                    print (RawNoneNamespacedFuncName)

                    if hasattr(self, RawNamespacedFuncName):
                        TmpResponse = getattr(self, RawNamespacedFuncName)(name=doc['metadata']['name'],
                                                                           namespace=namespace)
                        print (TmpResponse)
                        if TmpResponse['ret_code'] == 0:
                            TmpObjectDict['deleted_objs'].append(TmpResponse)
                            continue
                    elif hasattr(self, RawNoneNamespacedFuncName):
                        TmpResponse = getattr(self,RawNoneNamespacedFuncName)(name=doc['metadata']['name'])
                        print (TmpResponse)
                        if TmpResponse['ret_code'] == 0:
                            TmpObjectDict['deleted_objs'].append(TmpResponse)
                            continue


                return {
                    'ret_code': 0,
                    'result': TmpObjectDict
                }
            except Exception as e:
                print (str(e))
                return {
                    'ret_code': 1,
                    'result': str(e)
                }






#TmpObj = K8SClient()


#print (TmpObj.getNamespacedDeployment(name='redis', namespace='slyk8s'))
#print (TmpObj.createNamespace('wakaka'))
##print (TmpObj.deleteNamespacedDeployment(deployment='redis'))
#print (TmpObj.getNamespacedService('trsmas', 'wakaka'))
#print (TmpObj.deleteNampespacedSVC('ckm-svc', 'wakaka'))
#print (TmpObj.getNamespacedConfigMap('mariadb-master', 'slyk8s'))
#print (TmpObj.deleteNampespacedConfigMap('nacos-cm', 'wakaka'))
#print (TmpObj.getNamespacedSecret('dicttool-secret', 'wakaka'))
#print (TmpObj.deleteNamespacedSecret('dicttool-secret', 'wakaka'))
#print (TmpObj.getPersistentVolume('pv-dicttool-log-wbd'))
#print (TmpObj.deletePersistentVolume('pv-dicttool-log-wbd'))
#print (TmpObj.getNamespacedPVC('pvc-dicttool-log', 'wakaka'))
#print (TmpObj.deleteNamespacedPVC('pvc-dicttool-log', 'wakaka'))
#print (TmpObj.getNamespacedStatefulSet('nacos','wakaka'))
#print (TmpObj.deleteNamespacedStateFulSet('nacos', 'wakaka'))
#print (TmpObj.getNamespacedReplicationControler('mysql-nacos', 'wakaka'))
#print (TmpObj.deleteNamespacedReplicationControler('mysql-nacos', 'wakaka'))
#print (TmpObj.getStorageClass('managed-nfs-storage-foo'))
#print (TmpObj.deleteStorageClass('managed-nfs-storage-foo'))
#print (TmpObj.getNamespacedServiceAccount('nfs-client-provisioner', 'wakaka'))
#print (TmpObj.deleteNamespacedServiceAccount('nfs-client-provisioner', 'wakaka'))
#print (TmpObj.getClusterRole('nfs-client-provisioner-runner-wbd'))
#print (TmpObj.deleteClusterRole('nfs-client-provisioner-runner-wbd'))
#print (TmpObj.getClusterRoleBinding('run-nfs-client-provisioner-wbd'))
#print (TmpObj.deleteClusterRoleBinding('run-nfs-client-provisioner-wbd'))
#print (TmpObj.getNamespacedRole('leader-locking-nfs-client-provisioner', 'wakaka'))
#print (TmpObj.deleteNamespacedRole('leader-locking-nfs-client-provisioner', 'wakaka'))
#print (TmpObj.getNamespacedPod('nacos-0', 'slytest'))
#print (TmpObj.filterNamespacedPod(namespace='slyk8s', filters={'app':'dicttool','release':'dicttool'}))
#print (TmpObj.execNamespacedPod(pod='rabbitmq-6c6567cc88-qhb74', namespace='yl', cmd='rabbitmqctl delete_vhost bar'))
#print (TmpObj.getNamespacedRoleBinding('leader-locking-nfs-client-provisioner', 'wakaka'))
#print (TmpObj.deleteNamespacedRoleBinding('leader-locking-nfs-client-provisioner', 'wakaka'))

#TmpObj.createNamespace('wakaka')
#for item in ['dicttool-secret.yaml', 'foo-statefulset.yaml', 'foo-clusterrolebinding.yaml']:
#    print (TmpObj.createResourceFromYaml(filepath=item, namespace='wakaka'))
#print (TmpObj.deleteClusterRoleBinding('run-nfs-client-provisioner-wbd'))
#print (TmpObj.deleteNamespacedStateFulSet('nacos', 'wakaka'))

if __name__ == '__main__':
    TmpObj.createNamespace('wakaka')
    for a,b,c in os.walk('tmp'):
        for file in c:
            print (TmpObj.deleteResourceFromYaml(filepath=os.path.join('tmp/', file), namespace='wakaka'))
            print ('+'*20)
            sleep (5)