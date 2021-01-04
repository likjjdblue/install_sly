#!/usr/bin/env python2
#-*- coding: utf-8 -*-
import netaddr, ipconflict
import random
import subprocess

def generateNoneOverlapCIDR(ip=None, num=4, prefixlen=16):
    TmpCIDRList=[]
    try:
        TmpNetworkObj = netaddr.IPNetwork(ip)
        TmpCIDRList.append(ip)
    except Exception as e:
        print (str(e))
        return {
            "ret_code":1,
            'result': str(e)
        }

    TmpPrefixLen = TmpNetworkObj.prefixlen
    TmpFinalPrefixLen = TmpPrefixLen if TmpPrefixLen <= prefixlen else TmpPrefixLen

    if num < 2**TmpPrefixLen:
        TmpStart, TmpStop = (TmpNetworkObj[-1].value, 4294967296)
        while len(TmpCIDRList) < num+1:
            TmpRandomInt = random.randint(TmpStart, TmpStop)
            TmpRandomCIDR = str(netaddr.IPAddress(TmpRandomInt)) + '/'+ str(TmpFinalPrefixLen)
            TmpCIDRList.append(TmpRandomCIDR)

            print (TmpCIDRList)

            RetCode = subprocess.call("ipconflict %s "%(' '.join(TmpCIDRList)), shell=True)
            if str(RetCode) == '1':
                continue
            elif str(RetCode) != '1':
                TmpCIDRList.pop()
    else:
        TmpBinStr = TmpNetworkObj.ip.bin[2:]
        TmpPrefixBin = bin(int(TmpBinStr[:TmpPrefixLen], 2) ^ int('1'*TmpPrefixLen, 2))[2:]
        TmpSuffixBin = '0'*(32 - TmpPrefixLen)

        TmpStart = int(TmpPrefixBin + TmpSuffixBin, 2)
        TmpStop = 4294967296 -1

        while len(TmpCIDRList) < num+1:
            TmpRandomInt = random.randint(TmpStart, TmpStop)
            TmpRandomCIDR = str(netaddr.IPAddress(TmpRandomInt)) + '/'+ str(TmpFinalPrefixLen)
            TmpCIDRList.append(TmpRandomCIDR)

            print (TmpCIDRList)

            RetCode = subprocess.call("ipconflict %s "%(' '.join(TmpCIDRList)), shell=True)
            if str(RetCode) == '1':
                continue
            elif str(RetCode) != '1':
                TmpCIDRList.pop()


    print ("Final result: "+str(TmpCIDRList))




generateNoneOverlapCIDR(ip='7.2.3.3/8')


# ['7.2.3.3/8', '55.204.251.0/8', '17.201.140.1/8', '120.95.36.89/8', '235.138.27.57/8']