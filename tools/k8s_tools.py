#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from kubernetes import client, config
import os, yaml

class K8SClient(object):
    def __init__(self):
        config.load_kube_config()
        self.K8SAppsV1Client = client.AppsV1Api()
        self.K8SCoreV1Client = client.CoreV1Api()
        self.K8SStorageV1Client = client.StorageV1Api()
        self.K8SRbacAuthorizationV1Client = client.RbacAuthorizationV1Api()



    def getNamespacedDeployment(self, deployment=None, namespace='default'):
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
        TmpDeployment = self.getNamespacedDeployment(deployment=deployment, namespace=namespace)
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


    def getNamespacedSVC(self, service, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_service(name=service, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or SVC %s  not exists'%(namespace, service)
            }

    def deleteNampespacedSVC(self, service, namespace='default'):
        TmpSVC = self.getNamespacedSVC(service=service, namespace=namespace)
        if TmpSVC['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'SVC object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_service(name=service, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'SVC object deleted'
        }


    def getNamespacedConfigMap(self, configmap, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_config_map(name=configmap, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or ConfigMap %s  not exists'%(namespace, configmap)
            }

    def deleteNampespacedConfigMap(self, configmap, namespace='default'):
        TmpSVC = self.getNamespacedConfigMap(configmap=configmap, namespace=namespace)
        if TmpSVC['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ConfigMap object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_config_map(name=configmap, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'ConfigMap object deleted'
        }

    def getNamespacedSecret(self, secret, namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_secret(name=secret, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or Secret %s  not exists'%(namespace, secret)
            }

    def deleteNamespacedSecret(self, secret, namespace='default'):
        TmpSecret = self.getNamespacedSecret(secret=secret, namespace=namespace)
        if TmpSecret['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'Secret object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_secret(name=secret, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'Secret object deleted'
        }

    def getPersistentVolume(self, pv):
        try:
            TmpResponse = self.K8SCoreV1Client.read_persistent_volume(name=pv)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'PV %s  not exists'%(pv,)
            }

    def deletePersistentVolume(self, pv):
        TmpPV = self.getPersistentVolume(pv=pv)
        if TmpPV['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'PV object deleted'
            }

        self.K8SCoreV1Client.delete_persistent_volume(name=pv)
        return {
            "ret_code": 0,
            'result': 'PV object deleted'
        }

    def getNamespacedPVC(self, pvc='', namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_persistent_volume_claim(name=pvc, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or PVC %s  not exists'%(namespace, pvc)
            }

    def deleteNamespacedPVC(self, pvc, namespace='default'):
        TmpSecret = self.getNamespacedPVC(pvc=pvc, namespace=namespace)
        if TmpSecret['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'PVC object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_persistent_volume_claim(name=pvc, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'PVC object deleted'
        }

    def getNamespacedStatefulSet(self, statefulset='', namespace='default'):
        try:
            TmpResponse = self.K8SAppsV1Client.read_namespaced_stateful_set(name=statefulset, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (e)
            return  {
                "ret_code": 1,
                'result': "StatefulSet %s or Namespace %s not exists"%(statefulset, namespace)
            }

    def deleteNamespacedStateFulSet(self, statefulset='', namespace='default'):
        TmpStatefulSet = self.getNamespacedStatefulSet(statefulset=statefulset, namespace=namespace)
        if TmpStatefulSet['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'statefulset object deleted'
            }

        self.K8SAppsV1Client.delete_namespaced_stateful_set(name=statefulset, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'statefulset object deleted'
        }

    def getNamespacedReplicationControler(self, replicationcontroler='', namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_replication_controller(name=replicationcontroler,
                                                                                      namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or ReplicationControler %s  not exists'%(namespace, replicationcontroler)
            }

    def deleteNamespacedReplicationControler(self, replicationcontroler='', namespace='default'):
        TmpReplicationControler = self.getNamespacedReplicationControler(replicationcontroler=replicationcontroler,
                                                           namespace=namespace)
        if TmpReplicationControler['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ReplicationControler object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_replication_controller(name=replicationcontroler, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'ReplicationControler object deleted'
        }

    def getStorageClass(self, storageclass):
        try:
            TmpResponse = self.K8SStorageV1Client.read_storage_class(name=storageclass)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'StorageClass %s  not exists'%(storageclass,)
            }

    def deleteStorageClass(self, storageclass):
        TmpStorageClass = self.getStorageClass(storageclass=storageclass)
        if TmpStorageClass['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'StorageClass object deleted'
            }

        self.K8SStorageV1Client.delete_storage_class(name=storageclass)
        return {
            "ret_code": 0,
            'result': 'StorageClass object deleted'
        }

    def getNamespacedServiceAccount(self, serviceaccount='', namespace='default'):
        try:
            TmpResponse = self.K8SCoreV1Client.read_namespaced_service_account(name=serviceaccount,
                                                                               namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or ServiceAccount %s  not exists'%(namespace, serviceaccount)
            }

    def deleteNamespacedServiceAccount(self, serviceaccount, namespace='default'):
        TmpServiceAccount = self.getNamespacedServiceAccount(serviceaccount=serviceaccount, namespace=namespace)
        if TmpServiceAccount['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ServiceAccount object deleted'
            }

        self.K8SCoreV1Client.delete_namespaced_service_account(name=serviceaccount, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'ServiceAccount object deleted'
        }


    def getClusterRole(self, clusterrole=''):
        try:
            TmpResponse = self.K8SRbacAuthorizationV1Client.read_cluster_role(name=clusterrole)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'CLusterRole %s  not exists'%(clusterrole,)
            }

    def deleteClusterRole(self, clusterrole=''):
        TmpClusterRole = self.getClusterRole(clusterrole=clusterrole)
        if TmpClusterRole['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ClusterRole object deleted'
            }

        self.K8SRbacAuthorizationV1Client.delete_cluster_role(name=clusterrole)
        return {
            "ret_code": 0,
            'result': 'ClusterRole object deleted'
        }



    def getClusterRoleBinding(self, clusterrolebinding=''):
        try:
            TmpResponse = self.K8SRbacAuthorizationV1Client.read_cluster_role_binding(name=clusterrolebinding)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'CLusterRoleBinding %s  not exists'%(clusterrolebinding,)
            }

    def deleteClusterRoleBinding(self, clusterrolebinding=''):
        TmpClusterRoleBinding = self.getClusterRoleBinding(clusterrolebinding=clusterrolebinding)
        if TmpClusterRoleBinding['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'ClusterRoleBinding object deleted'
            }

        self.K8SRbacAuthorizationV1Client.delete_cluster_role_binding(name=clusterrolebinding)
        return {
            "ret_code": 0,
            'result': 'ClusterRoleBinding object deleted'
        }



    def getNamespacedRole(self, role='', namespace='default'):
        try:
            TmpResponse = self.K8SRbacAuthorizationV1Client.read_namespaced_role(name=role, namespace=namespace)
            return {
                "ret_code": 0,
                'result': TmpResponse
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code":1,
                'result': 'namespace %s or Role %s  not exists'%(namespace, role)
            }

    def deleteNamespacedRole(self, role, namespace='default'):
        TmpRole = self.getNamespacedRole(role=role, namespace=namespace)
        if TmpRole['ret_code'] != 0:
            return {
                "ret_code": 0,
                'result': 'Role object deleted'
            }

        self.K8SRbacAuthorizationV1Client.delete_namespaced_role(name=role, namespace=namespace)
        return {
            "ret_code": 0,
            'result': 'Role object deleted'
        }






TmpObj = K8SClient()
#print (TmpObj.getNamespacedDeployment(deployment='redis', namespace='slyk8s'))
#print (TmpObj.checkNamespacedDeploymentState(deployment='redis', namespace='slytest'))
#print (TmpObj.createNamespace('wakaka'))
#print (TmpObj.createNamespacedDeploymentFromYAML('redis/deployment.yaml'))
#print (TmpObj.deleteNamespacedDeployment(deployment='redis'))
#print (TmpObj.getNamespacedSVC('trsmas', 'wakaka'))
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