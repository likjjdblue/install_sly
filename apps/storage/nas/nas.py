#!/usr/bin/env python2
# -*- coding: utf-8 -8-
import sys, os
sys.path.append('../../..')
import tools
import re
import subprocess
from storagenode import datastoragenode, logstoragenode

class NASTool(object):
    def __init__(self, hostname, port, username, password, baseurl, *args, **kwargs):
        self.SSHClient = tools.ssh_tools.SSHTool(hostname, port, username, password)

        baseurl = baseurl.strip()
        baseurl = os.path.join('/', baseurl)
        baseurl = os.path.realpath(baseurl)
        self.BaseURL= baseurl
        TmpURL = self.BaseURL.replace('/', '_')
        self.HostName = hostname

        self.MntPoint = hostname.replace('.', '_')
        self.MntPoint = self.MntPoint + TmpURL

        TmpCWDPath = os.path.abspath(__file__)
        TmpCWDPath = os.path.dirname(TmpCWDPath)
        self.BaseDIRPath = os.path.realpath(os.path.join(TmpCWDPath, '../../..'))
        self.MntPointPath = os.path.join(self.BaseDIRPath, 'mnt', self.MntPoint)

        subprocess.Popen('mkdir -p  %s'%(self.MntPointPath, ), shell=True)



    def checkNASExistence(self):
        TmpMountState = os.path.ismount(self.MntPointPath)

        if TmpMountState:
            return {
                'ret_code': 0,
                'result': 'true',
            }

        return {
            'ret_code': 1,
            'result': 'false'
        }



    def installStorage(self, basedir='/'):
        TmpResult = self.checkNASExistence()

        if TmpResult['ret_code'] != 0:
            print ('Going to mount NFS  %s:%s'%(self.HostName, self.BaseURL))
            subprocess.Popen('mkdir -p  %s' % (self.MntPointPath,), shell=True)
            subprocess.Popen('timeout --signal=9 3 mount -t nfs %s:%s  %s'%(self.HostName, self.BaseURL, self.MntPointPath), shell=True)
            TmpResult = self.checkNASExistence()

        return TmpResult





    def createSubFolder(self, subpath):
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.MntPointPath, subpath)
        print ('create subfolder: '+str(TmpPath))
        subprocess.Popen('mkdir -p %s'%(TmpPath,), shell=True)


        return {
            'ret_code': 0,
            'result': 'NAS create subfolder %s successfully'%(subpath,)
        }

    def close(self):
        self.SSHClient.close()


    def ExecCmd(self,command, get_pty=True, *args, **kwargs):
        self.SSHClient.ExecCmd(command)


    def uploadFile(self, localpath, remotepath, *args, **kwargs):
        print ('NAS uploading.....')
        remotepath = remotepath.strip()

        if (remotepath != '/')  and (remotepath.startswith('/')):
            remotepath = remotepath.strip('/')


        remotepath = os.path.join(self.MntPointPath, remotepath)
        print ('remote path: '+str(remotepath))
        print ('local path: '+str(localpath))

        #self.SSHClient.uploadFile(localpath=localpath, remotepath=remotepath)
        subprocess.Popen('/usr/bin/cp %s %s'%(localpath, remotepath), shell=True)


    def generateRealPath(self, subpath):
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.BaseURL, subpath)
        return os.path.realpath(TmpPath)


    def cleanSubFolder(self, subpath):
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.MntPointPath, subpath)
        #TmpResponse = self.SSHClient.ExecCmd('rm -f -r  %s/*'%(TmpPath,))

        subprocess.call('rm -f -r %s/*'%(TmpPath, ), shell=True)

        return {
            'ret_code': 0,
            'result': 'NFS clean subfolder %s successfully'%(subpath,)
        }


    def unTarFile(self, subpath):
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.MntPointPath, subpath)
        print ('unTAR file: '+str(TmpPath))
        #TmpResponse = self.SSHClient.ExecCmd('tar -C %s -xvzf  %s'%(os.path.dirname(TmpPath), TmpPath))
        subprocess.call('tar -C %s -xvzf  %s'%(os.path.dirname(TmpPath), TmpPath), shell=True)


        return {
            'ret_code': 0,
            'result': 'NAS unTAR file %s successfully'%(subpath,)
        }


    def unZipFile(self, subpath):
        subpath = subpath.strip()
        if (subpath != '/')  and (subpath.startswith('/')):
            subpath = subpath.strip('/')

        TmpPath = os.path.join(self.MntPointPath, subpath)
        print ('unZIP file: ' + str(TmpPath))
        #TmpResponse = self.SSHClient.ExecCmd('cd %s;unzip  %s'%(os.path.dirname(TmpPath), TmpPath))

        subprocess.call('cd %s;unzip  %s'%(os.path.dirname(TmpPath), TmpPath), shell=True)

        return {
            'ret_code': 0,
            'result': 'NAS unZIP file %s successfully'%(subpath,)
        }




if __name__ == "__main__":
    Tmp = NASTool(**datastoragenode)
    print (Tmp.installStorage())
    Tmp.createSubFolder('/HAHs')
    Tmp.uploadFile(localpath='/home/luoy/install_sly/downloads/nacos.tar.gz', remotepath='/HAHs/nacos.tar.gz')
    #print (Tmp.generateRealPath('/TRS/DATA'))
    print (Tmp.unTarFile('/HAHs/nacos.tar.gz'))
    Tmp.cleanSubFolder('/HAHs')




