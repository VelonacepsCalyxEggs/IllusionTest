
import json
import random

class Illusion:
    r_param = 10
    d_param = 45
    alpha = 0
    fill = ["blue", "blue", "red"]
    outline = ["black","black","black"]
    
    def __init__(self, r_param, d_param, alpha, fill, outline):
        self.r_param = r_param
        self.d_param = d_param
        self.alpha = alpha
        self.fill = fill
        self.outline = outline

    def __str__(self) -> str:
        return f'r_param = {self.r_param}, d_param = {self.d_param}, aplha = {self.alpha}'
    
    def get_params(self):
        return {
            "r_param": self.r_param,
            "d_param": self.d_param,
            "alpha": self.alpha,
            "fill": self.fill,
            "outline": self.outline
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
                        illusion['r_param'],
                        illusion['d_param'],
                        illusion['alpha'],
                        illusion['circle_fill'],
                        illusion['circle_outline']
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
                
             

