import sys
path = sys.path[0]
sys.path.insert(0, path+'/HSBColor')
sys.path.insert(0, path+'/ImageElementDetect')
sys.path.insert(0, path+'/MusicGenerator')

from HSBColor import HSBColor
#from imageElementDetect import ImageElementDetect
from Orchestra import play_music

if __name__ == '__main__':

    #Extraction informations
    ##Mama partie

    ###HSBDecode
    ##### yellow=(50,100,100), blue=(240,100,100), red=(0,100,100), white(0,0,100), black(0,0,0)
    ##### blue_cold=(176,0,0), blue_cold_dark(176,0,255)
    color = HSBColor(0,0,255)

    print(color)
    print("temperature", color.temperature())
    print("luminosite", color.brightness())

    ##FaceDetect

    #Get mood
    emotion_levels = ["HAPPY", "JAZZ", "EMO", "NEUTRAL", "SAD"]
    ### Hot == temperature 1
    ### Cold == temperature 0
    ### Darkness == brightness 0.0
    ### Light == brightness, what is light? baby don't hurt me

    #### Each analyse add 1 unit to the total
    tmp_type_of_analyse = 2  # temperature, brightness

    tmp_temperature = color.temperature()
    tmp_max_luminosity = 1
    tmp_luminosity = color.brightness()*(1/tmp_max_luminosity)
    tmp_emotion_levels = len(emotion_levels)
    tmp_emotion_unit = 100 / tmp_emotion_levels
    tmp_periods_to_play = 10

    #### Mood on a scale of -100..100 with 100:happy and -100:sad
    #### Add up of positive values
    mood_value = (tmp_temperature + tmp_luminosity) / tmp_type_of_analyse * 100
    print(mood_value)

    #Make music !
    #sentiment = (mood_value / tmp_emotion_unit)
    sentiment = 0
    for i in range(0, tmp_emotion_levels+1):
        if mood_value < 0 and abs(mood_value) <= i*tmp_emotion_unit:
            sentiment = abs(i-5)
            print("neg")
            break
        if mood_value >= 0 and mood_value <= i*tmp_emotion_unit:
            sentiment = abs(i-5)
            print("pos")
            break

    #Play Music
    play_music(tmp_periods_to_play, sentiment)


