#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import socket
__all__ = ['common']


def replaceDockerRepo(image, harboraddr):
    if not harboraddr:
        return image

    TmpOriginalRepoList = image.split('/')
    TmpOriginalRepoList[0] = harboraddr
    return '/'.join(TmpOriginalRepoList)

def checkPortState(host='127.0.0.1',port=9200):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)
    try:
       s.connect((host,port))
       return True
    except:
        return False

