#!/usr/bin/env python2
#-*- coding: utf-8 -*-
import netaddr, ipconflict
import random
import subprocess

def generateNoneOverlapCIDR(ip=None, num=4, prefixlen=16):
    def __generator(start, stop):
        while len(TmpCIDRList) < num+1:
            TmpRandomInt = random.randint(TmpStart, TmpStop)
            TmpRandomCIDRStr = str(netaddr.IPAddress(TmpRandomInt)) + '/'+ str(TmpFinalPrefixLen)
            TmpRandomIPObj = netaddr.IPNetwork(TmpRandomCIDRStr).ip
            if TmpRandomIPObj.is_unicast() or TmpRandomIPObj.is_multicast() or TmpRandomIPObj.is_reserved()\
                    or TmpRandomIPObj.is_netmask() or TmpRandomIPObj.is_hostmask() or TmpRandomIPObj.is_loopback():
                print ('bad ip CIDR')
                continue


            TmpCIDRList.append(TmpRandomCIDRStr)


            print (TmpCIDRList)
            RetCode = subprocess.call("ipconflict %s "%(' '.join(TmpCIDRList)), shell=True)
            if str(RetCode) == '1':
                continue
            elif str(RetCode) != '1':
                TmpCIDRList.pop()

    TmpCIDRList=[]
    try:
        TmpNetworkObj = netaddr.IPNetwork(ip)
        TmpCIDRList.append(str(TmpNetworkObj.ip) + '/' + str(TmpNetworkObj.prefixlen))
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

        __generator(TmpStart, TmpStop)
    else:
        TmpBinStr = TmpNetworkObj.ip.bin[2:]
        TmpPrefixBin = bin(int(TmpBinStr[:TmpPrefixLen], 2) ^ int('1'*TmpPrefixLen, 2))[2:]
        TmpSuffixBin = '0'*(32 - TmpPrefixLen)

        TmpStart = int(TmpPrefixBin + TmpSuffixBin, 2)
        TmpStop = 4294967296 -1

        __generator(TmpStart, TmpStop)


    print ("Final result: "+str(TmpCIDRList))

generateNoneOverlapCIDR(ip='7.2.3.3/8')
