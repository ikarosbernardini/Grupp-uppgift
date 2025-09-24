import random
import os


class Visdom:

    def __init__(self, fil= str= 'visdom.txt'  ):  # visdom.txt är påhittat namn, vi ska egentligen lägga in den skapade filen med visdoms orden vi har
        self.fil= fil


    def visa_visdom(self) -> str: #visar alla visdomsord i filen

        with open (self.fil, 'r', encoding='utf-8') as f:
            rader= f.readlines()
            for rad in rader:
                print(rad.strip())

    
    def slumpa(self) ->str: # slumpar fram ord från filen
        with open (self.fil, 'r', encoding='utf-8') as f:
            rader= [rad.strip() for rad in f if rad.strip()]
            print(random.choice(rader))


    
    def radera(self, text) ->str: #raderar ord från filen
        with open (self.fil, 'r', encoding='utf-8') as f:
            rader= [rad.strip() for rad in f  if rad.strip()]
        rader.remove(text)
        with open(self.fil, 'w', encoding='uft-8') as f:
            for rad in rader:
                f.write(rad +'\n')
        print(f'Vi har nu raderat: {text}')

    
    def add(self, text): #lägger till ord i filen
        with open(self.fil, 'a', encoding='utf-8') as f:
            f.write(text + '\n')
        print(f'Vi har nu lagt till: {text}')

        