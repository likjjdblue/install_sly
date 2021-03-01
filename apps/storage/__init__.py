#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import importlib
import sys, os
sys.path.append('../..')

__all__ = [
    'nfs', 'StortageNameMapping', 'getClsObj',
]

StortageNameMapping ={
    'nfs': 'apps.storage.nfs/NFSTool',
    'nas': 'apps.storage.nas/NASTool',
}

def getClsObj(name):
    TmpList = StortageNameMapping[name].split('/')
    TmpModuleName, TmpClsName = (TmpList[0], TmpList[1])
    TmpModule = importlib.import_module(TmpModuleName)
    TmpInstance = getattr(TmpModule, TmpClsName)

    return TmpInstance