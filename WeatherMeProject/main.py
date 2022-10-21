from pyowm.owm import OWM
from termcolor import *

owm = OWM('da429a9ffad7be0ad02caa787d48be39')
mgr = owm.weather_manager()
isInterested = True

fence = '\t===================================================\t'

while isInterested == True:
    print('\n\tWhat country/city are you interested in?\t')
    city_to_observe = input('\n\tYour answer: ')
    try:
        observation = mgr.weather_at_place(city_to_observe)
        w = observation.weather
        print(fence)
        print('\tThe weather status in '+city_to_observe.upper()+': '+ w.detailed_status)
        print('\tTemperature: '+str(w.temperature('celsius')['temp'])+' \'C')
        print('\tWind speed: '+str(w.wind()['speed'])+' km/hour')
        print(fence)

        user_answer = input('\n\tDo you want to search another place?'
                            '\n\t\t"yes" - to continue\n\t\t"no" - to exit'
                            '\n\tYour answer: ')

        if user_answer.lower() == 'no':
            isInterested = False
        elif user_answer.lower() == 'yes':
            print('\n\tGreat to hear that!')
            pass
        else:
            pass
    except:
        print('\n\tThis country/city does not exist. Try another one')

print('\n\tProgram closed! =)')
