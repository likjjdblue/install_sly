#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from paramiko import SSHClient
import paramiko

class SSHTool(object):
    def __init__(self, hostname, port, username, password, timeout=10):
        self.Hostname = hostname
        self.Port = port
        self.Username = username
        self.Password = password
        self.Timeout = timeout
        self.GoodConnection = False

        self.SSHObj = SSHClient()
        self.SSHObj.load_system_host_keys()
        self.SSHObj.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)

    def checkConnection(self):
        if self.GoodConnection:
            return {
                "ret_code": 0,
                'result': "good connection"
            }

        try:
            self.SSHObj.connect(hostname=self.Hostname, port=self.Port, username=self.Username,
                                password=self.Password, timeout=self.Timeout)
            self.GoodConnection = True
            return {
                "ret_code": 0,
                'result': 'good connection'
            }
        except Exception as e:
            print (str(e))
            self.GoodConnection = False
            return {
                'ret_code': 1,
                'result': str(e)
            }

    def closeConnection(self):
        self.SSHObj.close()
        self.GoodConnection = False

    def ExecCmd(self,command, get_pty=True, *args, **kwargs):
        TmpCheckResult = self.checkConnection()
        if TmpCheckResult['ret_code'] != 0:
            return TmpCheckResult

        try:
            TmpDict = dict(stdout='', stderr='', exitcode=None)
            kwargs['command'] = command
            kwargs['get_pty'] = get_pty
            _, stdout, stderr = self.SSHObj.exec_command(*args, **kwargs)

            TmpDict['stdout'] = stdout.read()
            TmpDict['stderr'] = stderr.read()
            TmpDict['exitcode'] = stdout.channel.recv_exit_status()

            return {
                'ret_code': 0,
                'result': TmpDict
            }
        except Exception as e:
            print (str(e))
            return {
                "ret_code": 1,
                'result': str(e)
            }

    def readRemoteFile(self, filename, *args, **kwargs):
        TmpCheckResult = self.checkConnection()
        if TmpCheckResult['ret_code'] != 0:
            return TmpCheckResult

        TmpFTPClient = self.SSHObj.open_sftp()
        kwargs['filename'] = filename
        kwargs['mode'] = 'rb'
        try:
            with TmpFTPClient.file(*args, **kwargs) as f:
                TmpFileContent = f.read()

            return {
                'ret_code': 0,
                'result': TmpFileContent
            }
        except Exception as e:
            print (str(e))
            return {
                'ret_code': 1,
                'result': str(e)
            }

    def uploadFile(self, localpath, remotepath, *args, **kwargs):
        TmpCheckResult = self.checkConnection()
        if TmpCheckResult['ret_code'] != 0:
            return TmpCheckResult

        try:
            TmpFTPClient = self.SSHObj.open_sftp()
            kwargs['remotepath'] = remotepath
            kwargs['localpath'] = localpath
            TmpFTPClient.put(*args, **kwargs)

            return {
                'ret_code':0,
                'result': 'file uploaded'
            }
        except Exception as e:
            print (str(e))
            return {
                'ret_code': 1,
                'result': str(e)
            }


    def downloadFile(self, remotepath, localpath, *args, **kwargs):
        TmpCheckResult = self.checkConnection()
        if TmpCheckResult['ret_code'] != 0:
            return TmpCheckResult

        try:
            TmpFTPClient = self.SSHObj.open_sftp()
            kwargs['remotepath'] = remotepath
            kwargs['localpath'] = localpath
            TmpFTPClient.get(*args, **kwargs)

            return {
                'ret_code':0,
                'result': 'file downloaded'
            }
        except Exception as e:
            print (str(e))
            return {
                'ret_code': 1,
                'result': str(e)
            }

