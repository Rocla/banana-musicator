import sys
path = sys.path[0]
sys.path.insert(0, path+'/HSBColor')
sys.path.insert(0, path+'/ImageElementDetect')
sys.path.insert(0, path+'/HistogramAnalyzer')


from HSBColor import HSBColor
from ImageElementDetect import ImageElementDetect
from HistogramAnalyzer import HistogramAnalyzer
import cv2

if __name__ == '__main__':


    imagePath = './images/sunset_blue.jpg'

    #Extraction informations
    ##Mama partie

    img = cv2.imread(imagePath)

    histo_tool = HistogramAnalyzer(img)

    #print(histo_tool.get_hue_max())
    #print(histo_tool.get_saturation_max())
    #print(histo_tool.get_brigthness_max())

    ###HSBDecode
    color = HSBColor(histo_tool.get_hue_max() ,histo_tool.get_saturation_max(),histo_tool.get_brigthness_max())

    print(color)
    print("temperature", color.temperature())
    print("luminosite", color.brightness())

    ##FaceDetect

    #Creation musique !


    #Play !


