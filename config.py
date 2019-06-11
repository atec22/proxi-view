'''
    Comp 380 group project
    Group members: Gigi Lucena, Glenda Gonzalez, Daniel Stein,
                   Jonathan Slauter, Andre Tecson
    Date created: 06/24/2018
    Created by: Gigi Lucena
    Data Modified: 06/24/2018
    Modified by:
'''

import json
import os
import errno

class config(object):
    '''
    Config saves and loads the Security cameras setings

    Attributes:
        settings: dictionary with settings
        fileName: name of the file where settings are recorded

    '''

    def __init__(self, fileName ):
        ''' Return a  object with the settings recorded by user '''
        self.settings = {"ips": []}
        self.fileName = fileName


    def loadFile(self):
        ''' Return a object with settings
            file: name of the file to load  '''
        if os.path.exists(self.fileName):
            with open(self.fileName) as f:
                self.settings = json.load(f)

        return self.settings

    def saveFile(self, obj):
        ''' Save settings to file
            obj: dictionary with  settings
            file: name of the file to save settings as json
        '''

        try:
            os.remove(self.fileName)
        except OSError:
            pass


        self.settings = {"ips": []}
        for ip in obj:
            self.settings["ips"].append(ip)
        print(self.settings)

        with open(self.fileName, 'w') as outfile:
            json.dump(self.settings, outfile)
