#!/usr/bin/env python2
# -*- coding: utf-8 -8-
import sys, os
sys.path.append('../../..')
import tools

class NFSTools(object):
    def __init__(self, hostname, port, username, password):
        self.SSHClient = tools.ssh_tools.SSHTool(hostname, port, username, password)

    def setupNFSReady(self):
        TmpResult = self.SSHClient.checkConnection()
        return TmpResult

    def checkNFSExistence(self):
        TmpResult = self.setupNFSReady()
        if TmpResult['ret_code'] != 0:
            return TmpResult

        TmpResult = self.SSHClient.ExecCmd('which nfsstat')
        return TmpResult

    def installNFS(self):
        TmpResult = self.checkNFSExistence()
        if TmpResult['ret_code'] == 0 and TmpResult['result']['exitcode'] == 0:
            print ('NFS installed already')
            return {
                "ret_code": 0,
                'result': 'NFS installed already'
            }

        elif TmpResult['ret_code'] != 0:
            print ('Can not install NFS service')
            return TmpResult

        elif TmpResult['ret_code'] == 0 and TmpResult['result']['exitcode'] != 0:
            print ('Going to install NFS service...')
            self.SSHClient.uploadFile(localpath=os.path.abspath('resource/nfs_rpm.tar.gz'), remotepath='/tmp')



if __name__ == '__main__':
    TmpNFSObj = NFSTools('192.168.200.168', 10232, 'root', '!QAZ2wsx1234s')
    print (TmpNFSObj.installNFS())

