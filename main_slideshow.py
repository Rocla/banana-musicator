import sys
import cv2

path = sys.path[0]
sys.path.insert(0, path+'/HSBColor')
# sys.path.insert(0, path+'/ImageElementDetect')
sys.path.insert(0, path+'/HistogramAnalyzer')
sys.path.insert(0, path+'/MusicGenerator')

from HSBColor import HSBColor
from HistogramAnalyzer import HistogramAnalyzer
from imageElementDetect import ImageElementDetect
from Orchestra import play_music

if __name__ == '__main__':

    #Slideshow
    images_list = ["watson", "abstract_blue_orange_red", "abstract_landscape", "landscape_mountain_lake",
                   "landscape_see_blue_sand", "sunset_blue", "sunset_orange", "sunset_pink",
                   "white"]

    for i in range(0,len(images_list)):

        imagePath = path + '/images/' + images_list[i] + '.jpg'

        img = cv2.imread(imagePath)
        histo_tool = HistogramAnalyzer(img)

        color = HSBColor(histo_tool.get_hue_average(),
                         histo_tool.get_saturation_average(),
                         histo_tool.get_brigthness_average())

        print("Average for: " + str(images_list[i]))
        print(color)
        print("temperature", color.temperature())
        print("luminosite", color.brightness())

        color = HSBColor(histo_tool.get_hue_max(),
                         histo_tool.get_saturation_max(),
                         histo_tool.get_brigthness_max())
        print("Maximum : ")
        print(color)

        detector = ImageElementDetect(imagePath, False)

        # Get mood
        emotion_levels = ["HAPPY", "JAZZ", "EMO", "NEUTRAL", "SAD", "FACES"]
        ### Hot == temperature 1
        ### Cold == temperature 0
        ### Darkness == brightness 0.0
        ### Light == brightness, what is light? baby don't hurt me

        #### Each analyse add 1 unit to the total
        tmp_type_of_analyse = 2  # temperature, brightness

        #### How long should be the song?
        tmp_periods_to_play = 3

        tmp_temperature = color.temperature()
        tmp_max_luminosity = 1
        tmp_luminosity = color.brightness() * (1 / tmp_max_luminosity)
        tmp_emotion_levels = len(emotion_levels)
        tmp_emotion_unit = 100 / tmp_emotion_levels
        tmp_is_people = detector.hasFaces()

        mood_value = (tmp_temperature + tmp_luminosity) / tmp_type_of_analyse * 100

        sentiment = 0
        sentiment_name = ""
        for i in range(0, tmp_emotion_levels + 1):
            if tmp_is_people:
                sentiment = 5
                sentiment_name = emotion_levels[sentiment]
                print(sentiment_name)
                break
            elif mood_value < 0 and abs(mood_value) <= i * tmp_emotion_unit:
                sentiment = abs(i - tmp_emotion_levels)
                sentiment_name = emotion_levels[i]
                print(sentiment_name)
                break
            elif mood_value >= 0 and mood_value <= i * tmp_emotion_unit:
                sentiment = abs(i - tmp_emotion_levels)
                sentiment_name = emotion_levels[i]
                print(sentiment_name)
                break

        cv2.imshow(images_list[i] + ' ->emotion: ' + sentiment_name +' press_on_any_keyboard_key', img)
        cv2.waitKey(0)

        play_music(tmp_periods_to_play, sentiment)
        cv2.destroyAllWindows()




