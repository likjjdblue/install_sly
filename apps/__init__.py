#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import socket
from copy import deepcopy
__all__ = ['trs']


def replaceDockerRepo(image, harboraddr):
    if not harboraddr:
        return image

    TmpOriginalRepoList = image.split('/')
    if len(TmpOriginalRepoList)<=1:
        TmpOriginalRepoList = [''] + TmpOriginalRepoList

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



def mergeTwoDicts(DictA, DictB):
    TmpDict = deepcopy(DictA)
    TmpDict.update(DictB)

    return TmpDict


