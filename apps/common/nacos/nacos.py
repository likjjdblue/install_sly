#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append('../../..')
from apps.common import nfs
from tools import k8s_tools

class NacosTool(object):
    def __init__(self, namespace='default', mysqldatapath='nacos_mysql', nacosdatapath='nfs-provisioner', nfsinfo={},
                 harbor=None):
        self.NFSIP = nfsinfo['hostname']
        self.NFSPort = nfsinfo['port']
        self.NFSUsername = nfsinfo['username']
        self.NFSPassword = nfsinfo['password']
        self.NFSBasePath = nfsinfo['basepath']
        self.MysqlDataFolder = mysqldatapath
        self.NacosDataFolder = nacosdatapath

        self.Harbor = harbor
        self.k8sObj = k8s_tools.K8SClient()

        self.NFSObj = nfs.NFSTool(**nfsinfo)

    def setupNFS(self):
        TmpResponse = self.NFSObj.installNFS(basedir=self.NFSBasePath)
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        print ('create NACOS NFS successfully')

        self.NFSObj.createSubFolder(self.MysqlDataFolder)
        self.NFSObj.createSubFolder(self.NacosDataFolder)

        print ('setup NACOS NFS successfully')

        return {
            'ret_code': 0,
            'result': ''
        }





tmp = NacosTool(nfsinfo=dict(hostname='192.168.200.168', port=1022, username='root', password='!QAZ2wsx1234',
                         basepath='/TRS/DATA'))
print (tmp.setupNFS())