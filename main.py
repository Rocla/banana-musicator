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

    #Image used to test
    imagePath = path + '/images/watson.jpg'

    ##Extraction informations
    img = cv2.imread(imagePath)
    histo_tool = HistogramAnalyzer(img)

    colorAverage = HSBColor(histo_tool.get_hue_average(),
                     histo_tool.get_saturation_average(),
                     histo_tool.get_brigthness_average())

    print("### Average : ")
    print(colorAverage)
    print "Temperature : %2f" % colorAverage.temperature()
    print "Brightness : %2f" % colorAverage.brightness()

    colorMax = HSBColor(histo_tool.get_hue_max(),
                     histo_tool.get_saturation_max(),
                     histo_tool.get_brigthness_max())
    
    print("### Maximum : ")
    print(colorMax)
    print "Temperature : %2f" % colorMax.temperature()
    print "Brightness : %2f" % colorMax.brightness()

    #Select the HSBColor to use between colorAverage or colorMax
    colorToUse = colorMax

    ##FaceDetect
    detector = ImageElementDetect(imagePath, False)
    #print("Nb faces : " + detector.countFaces())
    #hasFaces = detector.hasFaces()
    #hasFaces = False

    ##Get mood
    emotion_levels = ["HAPPY", "JAZZ", "EMO", "NEUTRAL", "SAD", "FACES"]
    ### Hot == temperature 1
    ### Cold == temperature 0
    ### Darkness == brightness 0.0
    ### Light == brightness, what is light? baby don't hurt me

    #### Each analyse add 1 unit to the total
    tmp_type_of_analyse = 2  # temperature, brightness

    #### How long should be the song?
    tmp_periods_to_play = 3

    tmp_temperature = colorToUse.temperature()
    tmp_max_luminosity = 1
    tmp_luminosity = colorToUse.brightness()*(1/tmp_max_luminosity)
    tmp_emotion_levels = len(emotion_levels)
    tmp_emotion_unit = 100 / tmp_emotion_levels
    tmp_is_people = detector.hasFaces()

    #### Mood on a scale of -100..100 with 100:happy and -100:sad
    #### Add up of positive values
    mood_value = (tmp_temperature + tmp_luminosity) / tmp_type_of_analyse * 100
    #print(mood_value)

    #Make music !
    #sentiment = (mood_value / tmp_emotion_unit)
    sentiment = 0
    for i in range(0, tmp_emotion_levels+1):
        print("### Sentiment : ")
        if tmp_is_people:
            sentiment = 5
            print(emotion_levels[sentiment])
            break
        elif mood_value < 0 and abs(mood_value) <= i*tmp_emotion_unit:
            sentiment = abs(i-tmp_emotion_levels)
            print(emotion_levels[i])
            break
        elif mood_value >= 0 and mood_value <= i*tmp_emotion_unit:
            sentiment = abs(i-tmp_emotion_levels)
            print(emotion_levels[i])
            break

    #Show Image

    cv2.imshow('press_on_any_keyboard_key_to_play_the_music', img)
    cv2.waitKey(0)

    #Play Music
    play_music(tmp_periods_to_play, sentiment)

    #Ending images
    cv2.destroyAllWindows()

    exit(0)
