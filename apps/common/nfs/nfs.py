#!/usr/bin/env python2
# -*- coding: utf-8 -8-
import sys, os
sys.path.append('../../..')
import tools
import re

class NFSTool(object):
    def __init__(self, hostname, port, username, password, *args, **kwargs):
        self.SSHClient = tools.ssh_tools.SSHTool(hostname, port, username, password)
        self.BaseDir= '/'

    def setupNFSReady(self):
        TmpResult = self.SSHClient.checkConnection()
        return TmpResult

    def checkNFSExistence(self):
        TmpResult = self.setupNFSReady()
        if TmpResult['ret_code'] != 0:
            return TmpResult

        TmpResult = self.SSHClient.ExecCmd('which nfsstat')
        return TmpResult

    def installNFS(self, basedir='/TRS/DATA'):
        self.BaseDir = basedir
        TmpResult = self.checkNFSExistence()
        if TmpResult['ret_code'] == 0 and TmpResult['result']['exitcode'] == 0:
            print ('NFS installed already')


        elif TmpResult['ret_code'] != 0:
            print ('Can not install NFS service')
            return TmpResult

        elif TmpResult['ret_code'] == 0 and TmpResult['result']['exitcode'] != 0:
            print ('Going to install NFS service...')

            TmpCWDPath = os.path.abspath(__file__)
            TmpCWDPath = os.path.dirname(TmpCWDPath)

            TmpResult = self.SSHClient.uploadFile(localpath=os.path.join(TmpCWDPath, 'resource', 'nfs_rpm.tar.gz'),
                                                  remotepath='/tmp/nfs_rpm.tar.gz')

            if TmpResult['ret_code'] != 0:
                print ('Faild to upload NFS rpm tar')
                return TmpResult

            print ('unpacking  NFS rpm tar')

            TmpResult = self.SSHClient.ExecCmd('cd /tmp;tar -xvzf nfs_rpm.tar.gz >/dev/null 2>&1')
            print ('Install NFS rpm...')

            TmpResult = self.SSHClient.ExecCmd('cd /tmp/nfs_rpm;yum localinstall *.rpm -y 1>/dev/null 2>&1')
            if  (TmpResult['ret_code'] != 0) or (TmpResult['result']['exitcode'] != 0):
                print ('Failed to install NFS ')
                return TmpResult

            TmpRuls = 'firewall-cmd --permanent --add-service=nfs;firewall-cmd --permanent --add-service=mountd;firewall-cmd --permanent --add-service=rpc-bind;firewall-cmd --reload'
            self.SSHClient.ExecCmd(TmpRuls)
            self.SSHClient.ExecCmd('systemctl enable nfs')


        print ('Setup NFS .....')
        self.SSHClient.ExecCmd('mkdir -p %s'%(basedir,))
        self.SSHClient.ExecCmd('chown nfsnobody:nfsnobody  %s'%(basedir,))
        self.SSHClient.ExecCmd('touch /etc/exports')

        try:
            TmpFileContent = self.SSHClient.readRemoteFile('/etc/exports')['result']
            TmpMatched = False
            for line in re.findall('.*?\n', TmpFileContent, flags=re.UNICODE|re.DOTALL|re.MULTILINE):
                TmpReObj = re.search(r'^(\s*\n)|(\s*#.*?)$', line, flags=re.UNICODE|re.DOTALL|re.MULTILINE)
                if TmpReObj:
                    continue

                TmpReObj = re.search(r'^\s*%s\s+.*?\n$'%(basedir, ), line)
                if TmpReObj:
                    TmpMatched = True
                    break

            if not TmpMatched:
                TmpFileContent += '\n' + '%s     %s\n'%(basedir, '*(rw,sync,no_root_squash,no_subtree_check)')
                self.SSHClient.writeRemoteFile(filename='/etc/exports', data=TmpFileContent)

            print ('Restart NFS server...')
            self.SSHClient.restartService(name='nfs')
            return {
                "ret_code": 0,
                'result': 'NFS installed already'
            }

        except Exception as e:
            print (str(e))
            return {
                'ret_code': 1,
                'result': str(e)
            }

    def createSubFolder(self, subpath):
        TmpPath = os.path.join(self.BaseDir, subpath)
        TmpResponse = self.SSHClient.ExecCmd('mkdir -p %s'%(TmpPath,))
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        return {
            'ret_code': 0,
            'result': 'NFS create subfolder %s successfully'%(subpath,)
        }


