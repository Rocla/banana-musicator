from HistogramAnalyzer import HistogramAnalyzer
import cv2

if __name__ == "__main__":
    img = cv2.imread('../images/abstract_landscape.jpg')
    #cv2.imshow('original', img)
    
    histo_tool = HistogramAnalyzer(img)
    #histo_tool.show_hsv()
    #histo_tool.show_hsv_hist()
    print(histo_tool.get_hue_max())
    print(histo_tool.get_saturation_max())
    print(histo_tool.get_brigthness_max())

    #histo_tool.show_rgb()
    #histo_tool.show_rgb_hist()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
