#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2014, Steve Avery. All rights reserved.

import urllib2

from xml.dom.minidom import parseString, Element

STATE = 'state'
MACHINE_IDENTIFIER = 'machineIdentifier'
PLAYER = 'Player'


class PlexApi():
    def __init__(self, server, port):
        self.server = server
        self.port = port
        pass

    def getStatusSession(self):
        try:
            return self.callPlex("/status/sessions")
        except urllib2.URLError, e:
            return ""

    def callPlex(self, path):
        plexUrl = "%s:%s" % (self.server, self.port)
        request = urllib2.Request(("http://%s" + path) % plexUrl, "")
        result = urllib2.urlopen(request, timeout=3)

        return result.read()

    def getClientMachineIds(self):
        resultXml = self.getStatusSession()
        dom = parseString(resultXml)

        machineIds = list()

        for node in dom.getElementsByTagName(PLAYER):
            assert isinstance(node, Element)
            machineId = node.getAttribute(MACHINE_IDENTIFIER)
            assert isinstance(machineId, unicode)
            machineIds.append(machineId)

        return machineIds

    @staticmethod
    def getNodeForMachineId(dom, requestMachineId):
        nodeForMachine = None
        for node in dom.getElementsByTagName(PLAYER):
            assert isinstance(node, Element)
            machineId = node.getAttribute(MACHINE_IDENTIFIER)
            assert isinstance(machineId, unicode)
            if machineId == requestMachineId:
                nodeForMachine = node
                break
        return nodeForMachine

    def getClientState(self, requestMachineId):
        resultXml = self.getStatusSession()
        if resultXml == "":
            return 'server_offline'

        dom = parseString(resultXml)

        nodeForMachine = self.getNodeForMachineId(dom, requestMachineId)

        if nodeForMachine is None:
            return 'client_offline'

        state = nodeForMachine.getAttribute(STATE)
        return self.convertState(state)

    @staticmethod
    def convertState(x):
        return {
            'paused': 'paused',
            'playing': 'playing',
            }[x]