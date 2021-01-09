#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import string
import random
import subprocess
import base64

def generateRandomString(lenght):
    length = int(lenght)
    TmpRawStr = string.ascii_letters + string.digits + string.punctuation
    TmpStr = ''.join(random.choice(TmpRawStr) for _ in range(length))
    return TmpStr

def generateTRSSecret(input):
    rawinfo = input.strip()
    TmpResult = subprocess.Popen('java -jar IDSDesEncrypt.jar  %s'%(rawinfo,), shell=True, stdout=subprocess.PIPE).communicate()[0]
    return TmpResult.strip()


def EncodeBase64(input):
    return base64.b64encode(input)

def DecodeBase64(input):
    return base64.b64decode(input)

