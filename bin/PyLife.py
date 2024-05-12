"""
PyLife: Life simulation in Python.
Author: Brian van der Schaaf A.K.A. MassGaming25
Description: Simulate life using RNG.
"""

# PSL imports
import random
import os
import datetime
# External imports
from print_color import print
# local imports
import config


while True:    
    try:    
        print(
            """
            ______      _     _  __     
            | ___ \    | |   (_)/ _|    
            | |_/ /   _| |    _| |_ ___ 
            |  __/ | | | |   | |  _/ _ |
            | |  | |_| | |___| | ||  __/
            \_|   \__, \_____/_|_| \___|
                  __/ |                
                  |___/               
            +------------------------------+
            |  1: Start game               |
            |  2: Guide                    |
            |  3: Credits                  |
            |  4: Options                  |
            |  5: Quit                     |
            +------------------------------+
            """, color='cyan4'
        )
        choice = int(input("input> "))

    except KeyboardInterrupt:
        print('')
        print("EXIT", color='red')
        exit()
    except:
        pass
        
    if choice == 1 or choice == 2 or choice == 3 or choice == 4:
        break

    else:
        conf = str(input("Are you sure? (y/n): "))

        if conf == "y" or conf == "Y":
            print('Goodbye!', color='green')
            exit()

if choice == 1:
    print('WIP', color='yellow')
elif choice == 2:
    print('WIP', color='yellow')
elif choice == 3:
    print('WIP', color='yellow')
elif choice == 4:
    while True:    
        print('##  Options  ##', color='cyan')
        print('+---------------------------------------+', color='blue')
        print(f'1: Player can kill Pysims: {config.playerKillPysim}', color='white') 
        print(f'2: Player can spawn new Pysims: {config.playerSpawnPysim}', color='green')
        print(f'3: Failure conditions: {config.failureConditions}', color='white')
        print('=========================================', color='white')
        print(f'4: Delete save data', color='red', format='blink')
        print('+---------------------------------------+', color='blue')
        choice = int(input('input>'))
        if choice == 1 or choice == 2 or choice == 3:
            print('W.I.P', color='yellow')
        elif choice == 4:
            print('This will remove ALL save data.', tag='WARN', tag_color='yellow', color='white')
            print('This action can NOT be reversed!', tag='WARN', tag_color='yellow', color='red')
            conf = str(input('Are you absolutly sure? (y/n): '))
            if conf == 'y' or conf == 'Y':
                print('WIP', color='yellow')
                exit()
            else:
                break