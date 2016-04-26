__author__ = 'stevevisinand'

from ImageElementDetect import ImageElementDetect

if __name__ == '__main__':
    detector = ImageElementDetect('../images/watson.jpg', True)

    print("Nb faces : " + detector.countFaces())