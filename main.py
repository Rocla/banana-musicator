import sys
path = sys.path[0]
sys.path.insert(0, path+'/HSBColor')
sys.path.insert(0, path+'/ImageElementDetect')


from HSBColor import HSBColor
from ImageElementDetect import ImageElementDetect

if __name__ == '__main__':

    #Extraction informations
    ##Mama partie

    ###HSBDecode

    color = HSBColor(156,10,10)

    print(color)
    print("temperature", color.temperature())
    print("luminosite", color.brightness())

    ##FaceDetect

    #Création musique !


    #Play !


