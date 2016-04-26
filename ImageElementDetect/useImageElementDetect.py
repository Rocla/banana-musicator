__author__ = 'stevevisinand'

from imageElementDetect import ImageElementDetector

if __name__ == '__main__':
    detector = ImageElementDetector('watson.jpg', True)

    print("Nb faces : " + detector.countFaces())