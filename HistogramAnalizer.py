import cv2
import numpy as np

import matplotlib.pyplot as plt
import operator

class HistogramAnalizer:

    def __init__(self, img):
        self.img_rgb = img

        # CREATE HISTOGRAM
        self.hist_rgb()
        self.hist_hsv()

    def hist_rgb(self):
        self.img_b,self.img_g,self.img_r = cv2.split(self.img_rgb)

        self.hist_r = cv2.calcHist(self.img_r,[0],None,[256],[0,255])
        self.hist_g = cv2.calcHist(self.img_g,[0],None,[256],[0,255])
        self.hist_b = cv2.calcHist(self.img_b,[0],None,[256],[0,255])

    def hist_hsv(self):
        self.img_hsv = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2HSV)
        self.img_h, self.img_s, self.img_v = cv2.split(self.img_hsv)
        self.hist_hsv = cv2.calcHist([self.img_hsv],[0],None,[180],[0,180])

    def show_rgb(self):
        cv2.imshow('RGB', self.img_rgb)
        cv2.imshow('Red', self.img_r)
        cv2.imshow('Green', self.img_g)    
        cv2.imshow('Blue', self.img_b)
        
    def show_hsv(self):
        cv2.imshow('HSV', self.img_hsv)
        cv2.imshow('Hue', self.img_h)
        cv2.imshow('Saturation', self.img_s)    
        cv2.imshow('Value', self.img_v)
        
    def show_rgb_hist(self):
        cv2.imshow('RGB Histogram', self.img_v)
    
    def show_hsv_hist(self):
        plt.plot(self.hist_hsv)
        plt.xlim([0,180])
        plt.show()

    def get_main_hue(self):
        max_hue_f = float(self.max_indice(self.hist_hsv))
        max_hue = max_hue_f / 180 * 256     #Get a value between 0 and 255
        return int(max_hue)
    
    def moyenne(self, hist):
        total = 0
        somme = 0;
        for i in range(0,len(hist)):
            somme += hist[i]
            total += hist[i] * i
        return int(total/somme)

    def max_indice(self, hist):
        max_i = 0
        max_value = hist[0]
        for i in range(1, len(hist)):
            if max_value < hist[i]:
                max_value = hist[i]
                max_i = i
        return max_i 
