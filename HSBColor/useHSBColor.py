__author__ = 'stevevisinand'

from HSBColor import HSBColor


if __name__ == '__main__':
    color = HSBColor(176,0,255)

    print(color)
    print("temperature", color.temperature())
    print("luminosite", color.brightness())
