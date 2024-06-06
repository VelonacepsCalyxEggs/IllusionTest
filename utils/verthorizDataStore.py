
import json
import random

class Illusion:
    l_param = 64
    h_param = 75
    d_param = 0
    alpha = 0
    beta = 0
    lines_colour = ["blue", "red"]
    
    def __init__(self, l_param, h_param, d_param, alpha, beta, lines_colour):
        self.l_param = l_param
        self.h_param = h_param
        self.d_param = d_param
        self.alpha = alpha
        self.beta = beta
        self.lines_colour = lines_colour

    def __str__(self) -> str:
        return f'l_param = {self.l_param}, h_param = {self.h_param}, d_param = {self.d_param}, , alpha = {self.alpha}, beta = {self.beta}'
    
    def get_params(self):
        return {
            "l_param": self.l_param,
            "h_param": self.h_param,
            "d_param": self.d_param,
            "alpha": self.alpha,
            "beta": self.beta,
            "lines_colour": self.lines_colour
        }

class Test:

    illusions = []
    illusion_index = 0
    illusion_amount = None
    isTimeLimited = False
    timeLimit = None # seconds

    def __init__(self, path: str):
        '''
        path: str - path to json file with illusions
        '''
        self.readConfig(path)
        self.illusion_amount = len(self.illusions)
        self.randomizeIllusions()
    
    def readConfig(self, path) -> None:
        '''
        return: list[Illusion] - list of Illusion objects
        '''
        with open(path, 'r') as f:
            try:
                file = f.read()
                data = json.loads(file)
                general = data['general']
                if general["isTimeLimited"]:
                    self.timeLimit = general["timeLimitInSec"]
                    self.isTimeLimited = True

                for illusion in data['illusions']:
                    ill = Illusion(
                        illusion['l_param'],
                        illusion['h_param'],
                        illusion['d_param'],
                        illusion['alpha'],
                        illusion['beta'],
                        illusion['lines_colour']
                    )
                    repeats = illusion['repeat']
                    for _ in range(repeats):
                        self.illusions.append(ill)

            except FileNotFoundError as e:
                print("Error: ", e, "\n",  
                      "Could not find file: ", path, "\n")
            except json.decoder.JSONDecodeError as e:
                print(e)

    def randomizeIllusions(self) -> None:
        '''
        Randomizes the illusions in the sequence
        '''
        random.shuffle(self.illusions)

    def get_next_illusion(self) -> Illusion:
        '''
        return: Illusion - next illusion in the sequence
        
        At reaching the end of sequence, returns the first 
        illusion in the sequence
        '''
        self.illusion_index += 1
        if self.illusion_index > len(self.illusions):
            self.illusion_index = 1

        return self.illusions[self.illusion_index-1]
                
             

