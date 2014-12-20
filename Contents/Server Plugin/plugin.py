#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2014, Steve Avery. All rights reserved.

import indigo
from plexapi import PlexApi


################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.plexApi = PlexApi(pluginPrefs.get('address'), pluginPrefs.get('port'))
        self.debug = pluginPrefs.get('showDebugInfo', False)

    def __del__(self):
        indigo.PluginBase.__del__(self)


    ########################################
    def startup(self):
        self.debugLog(u"startup called")

    def shutdown(self):
        self.debugLog(u"shutdown called")

    def deviceStartComm(self, device):
        self.debugLog(u"Starting device: " + device.name)

    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        if not userCancelled:
            address = valuesDict.get(u"address")
            port = valuesDict.get(u"port")
            self.debugLog(u"Plex Server " + address + ":" + port)
            self.plexApi = PlexApi(self, address, port)

########################################
    def clientListGenerator(self, filter="", valuesDict=None, typeId="", targetId=0):
        return self.plexApi.getClientMachineIds()

    def runConcurrentThread(self):
        try:
            while True:
                for dev in indigo.devices.iter("self"):
                    if not dev.enabled or not dev.configured:
                        continue

                    if dev.deviceTypeId == u"plexClient":
                        clientId = dev.pluginProps.get('clientId', None)
                        state = self.plexApi.getClientState(clientId)
                        # self.debugLog(u"runConcurrentThread loop! " + state)
                        self.updateDeviceState(dev, 'mode', state)

                self.sleep(1)
        except self.StopThread:
            pass

    def updateDeviceState(self, device, state, newValue):
        if newValue != device.states[state]:
            try:
                self.debugLog(u"updateDeviceState: Updating device " + device.name + u" state: " + str(state) + u" = " + str(newValue))
            except Exception, e:
                self.debugLog(u"updateDeviceState: Updating device " + device.name + u" state: (Unable to display state due to error: " + str(e) + u")")

            device.updateStateOnServer(key=state, value=newValue)


    ########################################
    def validateDeviceConfigUi(self, valuesDict, typeId, devId):
        return (True, valuesDict)



