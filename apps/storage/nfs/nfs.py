#!/usr/bin/env python2
# -*- coding: utf-8 -8-
import sys, os
sys.path.append('../../..')
import tools
import re
from time import sleep

class NFSTool(object):
    def __init__(self, hostname, port, username, password, baseurl, *args, **kwargs):
        self.SSHClient = tools.ssh_tools.SSHTool(hostname, port, username, password)

        baseurl = baseurl.strip()
        baseurl = os.path.join('/', baseurl)
        baseurl = os.path.realpath(baseurl)
        self.BaseDir= baseurl

    def setupNFSReady(self):
        TmpResult = self.SSHClient.checkConnection()
        return TmpResult

    def checkNFSExistence(self):
        TmpResult = self.setupNFSReady()
        if TmpResult['ret_code'] != 0:
            return TmpResult

        TmpResult = self.SSHClient.ExecCmd('which nfsstat')
        return TmpResult

    def installStorage(self, basedir='/'):
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
        #self.SSHClient.ExecCmd('chown nfsnobody:nfsnobody  %s'%(basedir,))
        #self.SSHClient.ExecCmd('chmod -R 777  %s'%(basedir,))
        self.SSHClient.ExecCmd('touch /etc/exports')

        try:
            TmpFileContent = self.SSHClient.readRemoteFile('/etc/exports')['result']
            TmpMatched = False
            for line in re.findall('.*?\n', TmpFileContent, flags=re.UNICODE|re.DOTALL|re.MULTILINE):
                TmpReObj = re.search(r'^(\s*\n)|(\s*#.*?)$', line, flags=re.UNICODE|re.DOTALL|re.MULTILINE)
                if TmpReObj:
                    continue

                TmpReObj = re.search(r'^\s*%s\s+.*?\n$'%(self.BaseDir, ), line)
                if TmpReObj:
                    TmpMatched = True
                    break

            if not TmpMatched:
                TmpFileContent += '\n' + '%s     %s\n'%(self.BaseDir, '*(rw,no_root_squash,sync)')
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
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.BaseDir, subpath)
        print ('create subfolder: '+str(TmpPath))
        TmpResponse = self.SSHClient.ExecCmd('mkdir -p %s'%(TmpPath,))
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        return {
            'ret_code': 0,
            'result': 'NFS create subfolder %s successfully'%(subpath,)
        }

    def close(self):
        self.SSHClient.close()


    def ExecCmd(self,command, get_pty=True, *args, **kwargs):
        self.SSHClient.ExecCmd(command)


    def uploadFile(self, localpath, remotepath, *args, **kwargs):
        print ('NFS uploading.....')
        remotepath = remotepath.strip()

        if (remotepath != '/')  and (remotepath.startswith('/')):
            remotepath = remotepath.strip('/')

        print ('remote path: '+str(remotepath))
        print ('local path: '+str(localpath))
        remotepath = os.path.join(self.BaseDir, remotepath)

        self.SSHClient.uploadFile(localpath=localpath, remotepath=remotepath)


    def generateRealPath(self, subpath):
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.BaseDir, subpath)
        return os.path.realpath(TmpPath)


    def cleanSubFolder(self, subpath):
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.BaseDir, subpath)
        TmpResponse = self.SSHClient.ExecCmd('rm -f -r  %s/*'%(TmpPath,))
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        return {
            'ret_code': 0,
            'result': 'NFS clean subfolder %s successfully'%(subpath,)
        }


    def unTarFile(self, subpath):
        sleep (5)
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.BaseDir, subpath)
        print ('unTAR file: '+str(TmpPath))
        TmpResponse = self.SSHClient.ExecCmd('tar -C %s -xvzf  %s'%(os.path.dirname(TmpPath), TmpPath))
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        return {
            'ret_code': 0,
            'result': 'NFS unTAR file %s successfully'%(subpath,)
        }


    def unZipFile(self, subpath):
        sleep (5)
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.BaseDir, subpath)
        print ('unZIP file: ' + str(TmpPath))
        TmpResponse = self.SSHClient.ExecCmd('cd %s;unzip  %s'%(os.path.dirname(TmpPath), TmpPath))
        if TmpResponse['ret_code'] != 0:
            return TmpResponse

        return {
            'ret_code': 0,
            'result': 'NFS unZIP file %s successfully'%(subpath,)
        }





