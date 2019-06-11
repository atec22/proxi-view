'''
    Comp 380 group project
    Group members: Gigi Lucena, Glenda Gonzalez, Daniel Stein,
                   Jonathan Slauter, Andre Tecson
    Date created: 07/02/2018
    Created by: Gigi Lucena and Daniel Stein
    Data Modified:
    Modified by:
    Description: Camera class create and control the cameras stream in threadings
'''

import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError


class Camera():

    '''
    Camera class broadcast cameras contents in threads

    Attributes:
        url: URL where the camera is being streamed. The url contains the IP.
    '''

    def __init__(self, url):
        self.url = url
        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        print("camera initialised "+url)


    def start(self):
        self.thread.start()
        self.thread.join()
        print("camera stream started")


    def run(self):
        bytes=''
        global onChange

        while not self.thread_cancelled:
          try:
            bytes+=self.stream.raw.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')

            if a!=-1 and b!=-1:
              jpg = bytes[a:b+2]
              bytes= bytes[b+2:]
              cv2.namedWindow('Camera '+self.url, cv2.WINDOW_FREERATIO)
              img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)

              resized_image = cv2.resize(img, (800,600 ))

              cv2.imshow('Camera '+self.url,resized_image)

              if cv2.waitKey(1) ==27:
                exit(0)
          except ThreadError:
            self.thread_cancelled = True


    def is_running(self):
        return self.thread.isAlive()


    def shut_down(self):
        self.thread_cancelled = True
        #block while waiting for thread to terminate
        while self.thread.isAlive():
          time.sleep(1)
        return True
