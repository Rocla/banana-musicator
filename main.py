import sys
path = sys.path[0]
sys.path.insert(0, path+'/HSBColor')
sys.path.insert(0, path+'/HistogramAnalyzer')
#sys.path.insert(0, path+'/ImageElementDetect')

import cv2
from HSBColor import HSBColor
from HistogramAnalyzer import HistogramAnalyzer
#from ImageElementDetect import ImageElementDetect

if __name__ == '__main__':

    img = cv2.imread('images/landscape_see_blue_sand.jpg')
    
    #Extraction informations
    histo_tool = HistogramAnalyzer(img)

    print(histo_tool.get_hue_max()*360/255)
    print(histo_tool.get_saturation_max()*100/255)
    print(histo_tool.get_brigthness_max()*100/255)
    
    ###HSBDecode
    color = HSBColor(histo_tool.get_hue_max(),
                     histo_tool.get_saturation_max(),
                     histo_tool.get_brigthness_max())

    print(color)
    print("temperature", color.temperature())
    print("luminosite", color.brightness())

    ##FaceDetect

    #Création musique !


    #Play !


