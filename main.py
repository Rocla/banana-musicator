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
    color = HSBColor(0,0,100) # (50,100,100) == temp: -0.05

    print(color)
    print("temperature", color.temperature())
    print("luminosite", color.brightness())  # luminosity is between 0 and 0,4

    ##FaceDetect

    #Get mood
    emotion_levels = ["HAPPY", "JAZZ", "EMO", "NEUTRAL", "SAD"]
    ### Hot == temperature 1
    ### Cold == temperature 0
    ### Darkness == brightness 0.0
    ### Light == brightness, what is light? baby don't hurt me

    #### Each analyse add 1 unit to the total
    tmp_type_of_analyse = 2  # temperature, brightness

    tmp_temperature = abs(color.temperature()) + 0.001  # avoid absolute 0
    tmp_max_luminosity = 0.4
    tmp_luminosity = (abs(color.brightness()) + 0.001)*(1/tmp_max_luminosity)  # avoid absolute 0
    tmp_emotion_levels = len(emotion_levels)
    tmp_emotion_unit = 100 / tmp_emotion_levels
    tmp_periods_to_play = 10

    #### Mood on a scale of 0..100 with 100:happy and 0:sad
    ####
    #### Add up of positive values
    ##### yellow=(50,100,100), blue=(240,100,100), red=(0,100,100), white(0,0,100), black(0,0,0)
    mood_value = (tmp_temperature + tmp_luminosity) / tmp_type_of_analyse * 100
    print(mood_value)

    #Make music !
    #sentiment = (mood_value / tmp_emotion_unit)
    sentiment = 0
    for i in range(0, tmp_emotion_levels+1):
        if mood_value <= i * tmp_emotion_unit:
            sentiment = abs(i-5)
            break
    print(str(sentiment))

    #Play Music
    play_music(tmp_periods_to_play, sentiment)


