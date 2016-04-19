__author__ = 'stevevisinand'

from HSBColor import HSBColor


if __name__ == '__main__':
    color = HSBColor(156,10,10)

    print(color)
    print("temperature :", color.temperature())