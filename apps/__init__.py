#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__all__ = ['common']


def replaceDockerRepo(image, harboraddr):
    if not harboraddr:
        return image

    TmpOriginalRepoList = image.split('/')
    TmpOriginalRepoList[0] = harboraddr
    return '/'.join(TmpOriginalRepoList)


