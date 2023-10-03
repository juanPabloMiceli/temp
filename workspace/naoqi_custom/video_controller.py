# This test degrees(alpha) how to use the ALLandMarkDetection module.
# - We first instantiate a proxy to the ALLandMarkDetection module
#     Note that this module should be loaded on the robot's NAOqi.
#     The module output its results in ALMemory in a variable
#     called "LandmarkDetected"
# - We then read this AlMemory value and check whether we get
#   interesting things.
import time
from os.path import exists

import numpy as np
import cv2
from workspace.utils.logger_factory import LoggerFactory
from workspace.naoqi_custom.nao_properties import NaoProperties

from workspace.naoqi_custom.proxy_factory import ProxyFactory


class ImageContainer:

    # Image Container Array is an array as follows, we will just use the values we need
    # [0]: width.
    # [1]: height.
    # [2]: number of layers.
    # [3]: ColorSpace.
    # [4]: time stamp from qi::Clock (seconds).
    # [5]: time stamp from qi::Clock (microseconds).
    # [6]: binary array of size height * width * nblayers containing image data.
    # [7]: camera ID (kTop=0, kBottom=1).
    # [8]: left angle (radian).
    # [9]: topAngle (radian).
    # [10]: rightAngle (radian).
    # [11]: bottomAngle (radian).
    LOGGER = LoggerFactory.get_logger("ImageContainer")



    def __init__(self, image_container_array):
        if image_container_array is None:
            print("Image read from the nao was None. Maybe you need to restart it :(")
            exit(1)
        self.width = image_container_array[0]
        self.height = image_container_array[1]
        self.layers = image_container_array[2]
        self.color_space = image_container_array[3]
        self.b_array = image_container_array[6]


class VideoController:
    '''
    Image size: 1280x960
    Retrieved image format: Gray image
    '''  
    
    def __init__(self, ip, port):
        self.image_width = 1280
        self.image_height = 960
        self.image_shape = (self.image_height, self.image_width)
        self.LOGGER = LoggerFactory.get_logger("VideoController")
        self.proxy = ProxyFactory.get_proxy("ALVideoDevice", ip, port)
        self.video_id = self.proxy.subscribeCamera("My_Test_Video", 0, 3, 0, 30)
        self.LOGGER.info("Generated new video id {}".format(self.video_id))

    def get_current_gray_image(self):
        nao_image = self.__get_nao_image()
        image_bytes = ImageContainer(nao_image).b_array
        return np.frombuffer(image_bytes, dtype=np.uint8).reshape(self.image_shape)

    def __get_nao_image(self):
        return self.proxy.getImageRemote(self.video_id)

    def __del__(self):
        self.proxy.unsubscribe(self.video_id)
        self.LOGGER.info("Correctly unsuscribed!")


if __name__ == "__main__":
    

    IP, PORT = NaoProperties().get_connection_properties()
    video_controller = VideoController(IP, PORT)

    while True:
        time.sleep(1)
        image = video_controller.get_current_image()
        print("Shape: {}".format(image.shape))
