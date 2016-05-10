__author__ = 'margauxdivernois'

import cv2
import numpy as np
import matplotlib.pyplot as plt
import operator

class HistogramAnalyzer:

    def __init__(self, img):
        """
        Init the HistogramAnalyzer Object.
        Calculate the histogram of the given image.
        """
        
        self.img_rgb = img

        # CREATE HISTOGRAM
        self.hist_rgb()
        self.hist_hsv()

    def hist_rgb(self):
        """Calculate the RGB histograms and save in attribute"""
            
        self.img_b,self.img_g,self.img_r = cv2.split(self.img_rgb)

        self.hist_r = cv2.calcHist(self.img_r,[0],None,[256],[0,255])
        self.hist_g = cv2.calcHist(self.img_g,[0],None,[256],[0,255])
        self.hist_b = cv2.calcHist(self.img_b,[0],None,[256],[0,255])

    def hist_hsv(self):
        """Calculate the HSV histograms and save in attribute"""
        self.img_hsv = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2HSV)
        self.img_h, self.img_s, self.img_v = cv2.split(self.img_hsv)

        self.hist_h = cv2.calcHist([self.img_hsv],[0],self.img_s,[180],[0,180])
        self.hist_s = cv2.calcHist([self.img_hsv],[1],None,[256],[0,256])
        self.hist_v = cv2.calcHist([self.img_hsv],[2],None,[256],[0,256])

    def show_rgb(self):
        """Show the RGB Images"""
        cv2.imshow('RGB', self.img_rgb)
        cv2.imshow('Red', self.img_r)
        cv2.imshow('Green', self.img_g)    
        cv2.imshow('Blue', self.img_b)
        
    def show_hsv(self):
        """Show the HSV Images"""
        cv2.imshow('HSV', self.img_hsv)
        cv2.imshow('Hue', self.img_h)
        cv2.imshow('Saturation', self.img_s)    
        cv2.imshow('Value', self.img_v)
        
    def show_rgb_hist(self):
        """Show the RGB Histograms"""
        plt.plot(self.hist_r)
        plt.plot(self.hist_g)
        plt.plot(self.hist_b)
        plt.xlim([0,255])
        plt.title('RGB')
        plt.show()
    
    def show_hsv_hist(self):
        """Show the HSV Histograms"""
        plt.plot(self.hist_h)
        plt.xlim([0,180])
        plt.title('Hue')
        plt.show()

        plt.plot(self.hist_s)
        plt.xlim([0,256])
        plt.title('Saturation')
        plt.show()

        plt.plot(self.hist_v)
        plt.xlim([0,256])
        plt.title('Brightness / Value')
        plt.show()

    def get_hue_max(self):
        """Return the maximum hue between 0 and 255"""
        max_hue_f = float(self.max_index(self.hist_h))
        max_hue = max_hue_f / 180 * 256     #Get a value between 0 and 255
        return int(max_hue)

    def get_hue_average(self):
        """Return the average hue between 0 and 255"""
        average_hue = self.average(self.hist_h)
        average_hue = average_hue * 256 / 180
        return average_hue
        
    def get_saturation_max(self):
        """Return the maximum saturation"""
        return int(self.max_index(self.hist_s))

    def get_saturation_average(self):
        """Return the average saturation"""
        average_saturation = self.average(self.hist_s)
        return average_saturation

    def get_brigthness_max(self):
        """Return the maximum brightness"""
        return int(self.max_index(self.hist_v))

    def get_brigthness_average(self):
        """Return the average brightness"""
        average_saturation = self.average(self.hist_v)
        return average_saturation
    
    def average(self, hist):
        """Calculate and return the average of an histogram"""
        total = 0
        somme = 0;
        for i in range(0,len(hist)):
            somme += hist[i]
            total += hist[i] * i
        return int(total/somme)

    def max_index(self, hist):
        """Calculate and return the maximum value of an histogram"""
        max_i = 0
        max_value = hist[0]
        for i in range(1, len(hist)):
            if max_value < hist[i]:
                max_value = hist[i]
                max_i = i
        return max_i 
