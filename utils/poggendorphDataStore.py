
import json
import random

class Illusion:
    w_param = 10
    alpha = 45
    beta = 0
    vert_length = 100
    
    def __init__(self, w_param, alpha, beta, vert_length):
        self.w_param = w_param
        self.alpha = alpha
        self.beta = beta
        self.vert_length = vert_length

    def __str__(self) -> str:
        return f"w_param = {self.w_param}, alpha = {self.alpha}, beta = {self.beta}, vert_length = {self.vert_length}"
    
    def get_params(self):
        return {
            "w_param": self.w_param,
            "alpha": self.alpha,
            "beta": self.beta,
            "vert_length": self.vert_length
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
                        illusion['w_param'],
                        illusion['alpha'],
                        illusion['beta'],
                        illusion['vert_length']
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
                
             

