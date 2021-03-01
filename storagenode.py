#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
datastoragenode = {
    'type': 'nfs',
    'hostname':  '192.168.200.74',
    'port': 1022,
    'username': 'root',
    'password': '!QAZ2wsx1234',
    'basepath': '/',
    'baseurl': '/TRS/DATA',
}


logstoragenode = {
    'type': 'nfs',
    'hostname':  '192.168.200.74',
    'port': 1022,
    'username': 'root',
    'password': '!QAZ2wsx1234',
    'basepath': '/',
    'baseurl': '/TRS/LOG'
}
'''

datastoragenode = {
    'type': 'nas',
    'hostname':  '192.168.200.66',
    'port': 1022,
    'username': 'root',
    'password': '!QAZ2wsx1234',
    'basepath': '/TRS/DATA',
    'baseurl': '/volume1/NFS',
}


logstoragenode = {
    'type': 'nas',
    'hostname':  '192.168.200.66',
    'port': 1022,
    'username': 'root',
    'password': '!QAZ2wsx1234',
    'basepath': '/TRS/LOG',
    'baseurl': '/volume1/NFS2'
}

namespace = 'sly2'