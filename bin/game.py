## This is where the simulation itself will be.
from print_color import print
import random
import os
import pysims_connect as pc
import time

def addSim(simName, simAge):
    cursor = pc.mydb.cursor()

    sql = f"INSERT INTO pysims (name, age) VALUES (%s, %s)"
    val = [simName, str(simAge)]
    cursor.execute(sql, val)

    pc.mydb.commit()
    print(cursor.rowcount, "sim created.")

def killSim(simName):
    cursor = pc.mydb.cursor(buffered=True)

    sql = f"SELECT * FROM pysims WHERE name = %s"
    val = [simName]
    cursor.execute(sql, val)
    result = cursor.fetchall()
    for x in result:
        print('Killing', x[1])

    sql = "DELETE FROM pysims WHERE name = %s"
    val = [simName]
    cursor.execute(sql, val)
    pc.mydb.commit()

def newCarreer(simName):
    jobs = ['Baker', 'Cook', 'Mechanic', 'Office Worker', 'Singer', 'actor', 'Pilot', 'Firefighter', 'Police officer', 'EMT']
    
    cursor = pc.mydb.cursor()
    sql = 'SELECT * FROM pysims WHERE name = %s'
    val = [simName]
    cursor.execute(sql, val)
    res = cursor.fetchall()
    for id, name, age, occupation in res:
        if occupation == None:
            newJob = random.choices(jobs)
            
            sql = "UPDATE pysims SET occupation = %s WHERE name = %s"
            val = [newJob[0], simName]
            cursor.execute(sql, val)
            pc.mydb.commit()

            print(f'{simName} got a job as a {newJob}.', tag='Carreer', tag_color='yellow')
        else:
            print(f'{simName} was promoted.', tag="Carreer", tag_color="yellow")


def eventSelector(simName):
    eventTypes = ['Regular', 'Friendship', 'carreer', 'Romance', 'Birth', 'Death']
    RandomEvent = random.choices(eventTypes, weights=(75, 10, 4, 3, 1, 1))

    cursor = pc.mydb.cursor()
    sql = "SELECT * FROM pysims"
    cursor.execute(sql)
    result = cursor.fetchall()

    for id, name, age, occupation in result:
        for x in RandomEvent:
            if name == simName:    
                if x == 'Regular':
                    print(f'{simName} had a normal day today', tag='Regular', tag_color='blue')
                elif x == 'friendship':
                    print(f'{simName} dreamt about having friends today. (feature coming soon.)', tag='Friend', tag_color='green')
                elif x == 'carreer':
                    newCarreer(simName)
                elif x == 'Romance':
                    print(f'{simName} is feeling lonely today (feature coming soon.)', tag='Romance', tag_color='magenta')
                elif x == 'Birth':
                    print(f'{simName} is thinking about kids. (feature coming soon.)', tag='Birth', tag_color='cyan')
                else:
                    if age <= 100:
                        print(f'{simName} had a normal day today.', tag="Regular", tag_color="blue")
                    else:
                        print(f'{simName} has died:(', tag="Death", color="red")
                        killSim(simName)

def dailyActivity():
    cursor = pc.mydb.cursor()

    sql = "SELECT * FROM pysims"
    cursor.execute(sql)
    result = cursor.fetchall()

    for id, name, age, occupation in result:
        eventSelector(name)

def playGame():
    while True:
        try:  
            cursor = pc.mydb.cursor()
            sql = 'SELECT * FROM date'
            cursor.execute(sql)
            date = cursor.fetchall()
            for day, month, year in date:
                gameday = day
                gamemonth = month
                gameyear = year
            os.system('cls' if os.name == 'nt' else 'clear')

            dailyActivity()

            print(f"Day {str(gameday)} Month {str(gamemonth)} Year {str(gameyear)}")
            print("1) Next day 2) Create Pysim 3) Kill Pysim 4) Exit")
            choice = int(input('What do you want to do?: '))

            if choice == 1:
                pass
            elif choice == 2:
                name = str(input("What is the new Pysim's name?: "))
                age = str(input(f"What is {name}'s age?: "))
                addSim(name, age)
            elif choice == 3:
                name = str(input("What Pysim do you want to kill?: "))
                killSim(name)
            elif choice == 4:
                print("Goodbye")
                exit()
            
            if gameday <= 31:
                newday = gameday + 1
                sql = 'UPDATE date SET day = %s'
                val = [newday]
                cursor.execute(sql, val)
                pc.mydb.commit()
            else:
                newday = 1
                newmonth = gamemonth + 1
                sql = 'UPDATE date SET day = %s, month = %s'
                val = [newday, newmonth]
                cursor.execute(sql, val)
                pc.mydb.commit()
            if month == 12 and day == 31:
                newday = 1
                newmonth = 1
                newyear = gameyear + 1
                sql = 'UPDATE date SET day = %s, month = %s, year = %s'
                val = [newday, newmonth, newyear]
                cursor.execute(sql, val)
                pc.mydb.commit()

                sql = 'SELECT * FROM pysims'
                cursor.execute(sql)
                result = cursor.fetchall()

                for id, name, age, occupation in result:
                    newAge = age + 1
                    sql = 'UPDATE pysims SET age = %s WHERE name = %s'
                    val = [newAge, name]
                    cursor.execute(sql,val)
                    pc.mydb.commit()
                    sql = 'SELECT * FROM pysims WHERE name = %s'
                    val = [name]
                    cursor.execute(sql, val)
                    result = cursor.fetchall()
                    for x in result:
                        print(f'{name} is now {str(x[2])} years old.')
                print('Happy new year! Game will restart in 5 seconds.', color="green")
                time.sleep(5)
        except ValueError:
            pass