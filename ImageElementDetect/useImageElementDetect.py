__author__ = 'stevevisinand'

from imageElementDetect import ImageElementDetect

if __name__ == '__main__':
    detector = ImageElementDetect('../images/watson.jpg', True)

    print("Nb faces : " + str(detector.countFaces()))
