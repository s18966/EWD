import random
from pathlib import Path
import os
class Game:
    def __init__(self, game_name, num_of_players):
        self.game_name = game_name
        self.num_of_players = num_of_players

    def _play(self):
        print(f"Game {self.game_name} started with {self.num_of_players}")

class Hangman(Game):
    def __init__(self, game_name, num_of_players):
        super().__init__(game_name, num_of_players)
        super()._play()
        self.wictory = False
        self.__initial_setup()
        self.__game_loop()

    def __initial_setup(self):
        self.__choose_gamemode()
        self.__setup_lives()
        self.__get_word()

    def __choose_gamemode(self):
        try:
            gamemode = int(input("""
            Choose gamemode:
            0: beginner
            1: intermediate
            2: advanced
            """))
            if gamemode < 0 or gamemode > 2:
                raise ValueError
            
            self.gamemode = gamemode
        except ValueError:
            print("Wrong argument provided. Starting game with beginner gamemode")
            self.gamemode = 0
        
    def __setup_lives(self):
        switcher = {
            0: 10, 
            1: 6,
            2: 4
        }
        self.number_of_lives = switcher.get(self.gamemode)
        print(f"You have {self.number_of_lives} tries")
    
    def __get_word(self):
        if self.num_of_players == 1:
            script_location = Path(__file__).absolute().parent
            file_location = script_location / 'words.txt'
            with file_location.open() as f:
                words = f.readlines()
                more_than_4 = [word for word in words if len(word) > 4]
                self.word = random.choice(more_than_4)
                if self.word[-1] == "\n":
                    self.word = self.word[:-1]
        else:
            self.word = input("Provide a valid english word. Responsibility is on you:")
            os.system("clear")

    def __game_loop(self):
        res = []
        for i in self.word:
            res.append([i, False])
        while self.number_of_lives > 0:
            os.system("clear")
            self.__pretty_print(res)
            player_input = input("Please provide one char: ")
            if len(player_input) != 1:
                print("Provide a valid char!")
                continue
            guessed = self.__check_char(player_input, res)
            self.wictory = self.__check_wictory(res)
            if self.wictory:
                break
            if guessed==False:
                self.number_of_lives = self.number_of_lives - 1
        
        if self.wictory:
            print(f"You've won! The word is: {self.word}")
        else:
            print(f"You've lost. The word is: {self.word}")


    def __pretty_print(self, arr):
        word = ""
        for tup in arr:
            if tup[1]:
                word = word + tup[0]
            else:
                word = word + "*"
        print(f"Current number of lives is: {self.number_of_lives}\nWord is {word}")
        

    def __check_char(self, player_input, arr):
        guessed = False
        for tup in arr:
            if tup[0] == player_input:
                tup[1] = True
                guessed = True
        return guessed
            
    def __check_wictory(self, arr): 
        wictory = True
        for tup in arr:
            if tup[1] == False:
                wictory = False
        return wictory

def task1():
    lambda_x = lambda x : x + 15
    lambda_x_y = lambda x, y: x*y
    print(lambda_x(input_helper("Please provide an argument x: ")))
    x = input_helper("Provide x:")
    y = input_helper("Provide y:")
    print(lambda_x_y(x, y))

def task2():
    dicts = [
        {'make': 'Nokia', 'model': 216, 'color': 'Black'},
        {'make': 'Mi Max', 'model': 2, 'color': 'Gold'},
        {'make': 'Samsung', 'model': 7, 'color': 'Blue'}
    ]
    print(dicts)
    key_to_sort = input("Please input key, which will be used to sort. Possible keys: make, model, color.\n")
    if key_to_sort in dicts[0].keys():
        print(sorted(dicts, key = lambda x: x[key_to_sort]))
    else:
        print("Incorrect key provided")


def task3():
    raise_to_pow = lambda n, pow : n ** pow
    arrs = [1,2,3,4,5,6,7,8,9,10]
    [print(raise_to_pow(x, 2)) for x in arrs]
    [print(raise_to_pow(x, 3)) for x in arrs]

def task4():
    def return_only_valid(x):
        if x == 1 or x == 2:
            return x
        else:
            return 1
    hangman = Hangman("Hangman", return_only_valid(int(input("Provide number of players:"))))


#Casts input to int or throws None if exception
def input_helper(message):
    try:
        input_num = int(input(message))
        return input_num
    except ValueError:
        return None


def task_picker():
    switcher = {
        1: task1,
        2: task2,
        3: task3,
        4: task4
    }
    try:
        task = input_helper("Please pick task from 1 to 4:")
        func = switcher.get(task, None)
        if func is None:
            raise Exception
        func()
    except Exception:
        print("Invalid argument provided. Aborting....")


def main():
    task_picker()

if __name__ == "__main__":
    main()