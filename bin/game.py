## This is where the simulation itself will be.
import mysql.connector
from print_color import print
import random
import os
import pysims_connect as pc
import time

import config

randomEvent = []


def addSim(simName, simAge, gender):
    cursor = pc.mydb.cursor()
    try:
        sql = f"INSERT INTO pysims (name, age, gender) VALUES (%s, %s, %s)"
        val = [simName, str(simAge), gender]
        cursor.execute(sql, val)

        pc.mydb.commit()
        print(cursor.rowcount, "sim created.")
    except:
        print('Something went wrong while creating new Pysim.')

def killSim(simName):
    cursor = pc.mydb.cursor(buffered=True)

    sql = f"SELECT * FROM pysims WHERE name = %s"
    val = [simName]
    cursor.execute(sql, val)
    result = cursor.fetchall()
    for x in result:
        pass

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
    for id, name, age, occupation, gender, partner, married in res:
        if occupation == None:
            if age >= 18:
                newJob = random.choices(jobs)
                
                sql = "UPDATE pysims SET occupation = %s WHERE name = %s"
                val = [newJob[0], simName]
                cursor.execute(sql, val)
                pc.mydb.commit()

                print(f'{simName} got a job as a {newJob[0]}.', tag='Carreer', tag_color='yellow', color='white')

            else:
                print(f'{name} was praised for their marks.', tag='School', color='white', tag_color='yellow')

        else:
            randomJobEvent = random.choices([0, 1], weights= [10, 88])
            if randomJobEvent == 0:
                print(f'{simName} was promoted.', tag="Carreer", tag_color="yellow", color='white')
            elif randomJobEvent == 1:
                print(f'{simName} had a normal day at work.', tag="Carreer", tag_color="yellow", color='white')
 
def newFriend(simName):
    cursor = pc.mydb.cursor()
    sql = 'SELECT * FROM pysims'
    cursor.execute(sql)
    res = cursor.fetchall()
    
    friendpool = []
    for id, name, age, occupation, gender, partner, married in res:
        if name == simName:
            sim1_ID = id
            sim1_name = name
    
    for id, name, age, occupation, gender, partner, married in res:
        if not name == simName:
            friendpool.append([id, name])
            randomFriend = random.choices(friendpool)
            if randomFriend[0] == sim1_ID:
                pass
            else:
                sim2_ID = id
                sim2_name = name
    if sim1_ID == sim2_ID:
        print(f'{sim1_name} Tthought they could be friends with themselves.', tag= 'Friendship', color='white', tag_color='green')
    else:
        try:    
            friendkey = sim1_name + sim2_name
            sql = 'INSERT INTO friendship (pysim_id_1, pysim_id_2, friendKey) VALUES (%s, %s, %s)'
            val = [sim1_ID, sim2_ID, friendkey]
            cursor.execute(sql, val)
            pc.mydb.commit()

            friendkey = sim2_name + sim1_name
            sql = 'INSERT INTO friendship (pysim_id_1, pysim_id_2, friendKey) VALUES (%s, %s, %s)'
            val = [sim1_ID, sim2_ID, friendkey]
            cursor.execute(sql, val)
            pc.mydb.commit()

            print(f'{sim1_name} is now friends with {sim2_name}.', tag='Friendship', color='white', tag_color='green')
        except mysql.connector.errors.IntegrityError:
            print(f'{sim1_name} and {sim2_name} spent some time together.', tag= 'Friendship', color='white', tag_color='green')

def romance(simName):
    cursor = pc.mydb.cursor()
    sql = 'SELECT * FROM pysims'
    cursor.execute(sql)
    res = cursor.fetchall()
    romanceList = []
    sim1 = []
    sim2 = []
    inRelationship = False

    for id, name, age, occupation, gender, partner, married in res:
        if partner is None:
            if name == simName and age >= 18:
                sim1 = [id, name, age, gender, partner, married]
        else:
            if name == simName:
                inRelationship = True
                sql = 'SELECT * FROM pysims WHERE sim_id = %s'
                val = [partner]
                cursor.execute(sql, val)
                partner_res = cursor.fetchone()
                
                if partner_res:
                    l = partner_res
                    if married == 0 and partner == l[0]:
                        chance = random.choices([0, 1, 2], weights=[89, 10, 1])[0]
                        if chance == 0:
                            print(f'{simName} went on a date with {l[1]}.', tag='Romance', color='white', tag_color='magenta')
                        elif chance == 1:
                            sql = 'UPDATE pysims SET married = 1 WHERE name = %s'
                            val = [simName]
                            cursor.execute(sql, val)
                            pc.mydb.commit()

                            sql = 'UPDATE pysims SET married = 1 WHERE name = %s'
                            val = [l[1]]
                            cursor.execute(sql, val)
                            pc.mydb.commit()

                            print(f'{simName} and {l[1]} got married.', tag='Romance', color='white', tag_color='magenta')
                        else:
                            sql = 'UPDATE pysims SET partner = NULL WHERE name = %s'
                            val = [simName]
                            cursor.execute(sql, val)
                            pc.mydb.commit()

                            sql = 'UPDATE pysims SET partner = NULL WHERE name = %s'
                            val = [l[1]]
                            cursor.execute(sql, val)
                            pc.mydb.commit()

                            print(f'{simName} and {l[1]} broke up.')
                    elif l[0] != partner:
                        print(f'{simName} took a raincheck', tag='Romance', color='white', tag_color='magenta')
                    else:
                        print(f'{simName} went on a date with {l[1]}.', tag='Romance', color='white', tag_color='magenta')
                break

    if not inRelationship:
        for id, name, age, occupation, gender, partner, married in res:
            if name != simName and age >= 18:
                romanceList.append(id)
                
        if romanceList:
            randomSim = random.choice(romanceList)
            sql = 'SELECT * FROM pysims WHERE sim_id = %s'
            val = [randomSim]
            cursor.execute(sql, val)
            res = cursor.fetchone()
            if res:
                sim2 = res

                if sim1 and sim1[3] != sim2[3]:  # Ensure different genders
                    if abs(sim1[2] - sim2[2]) <= 2:
                        randomNumber = random.choices([0, 1], weights=[99, 1])[0]
                        if randomNumber == 0:
                            print(f'{sim1[1]} asked out {sim2[1]}, but got rejected.', tag='Romance', color='white', tag_color='magenta')
                        else:
                            sql = 'UPDATE pysims SET partner = %s WHERE name = %s'
                            val = [sim2[0], sim1[1]]
                            cursor.execute(sql, val)
                            pc.mydb.commit()
                            
                            sql = 'UPDATE pysims SET partner = %s WHERE name = %s'
                            val = [sim1[0], sim2[1]]
                            cursor.execute(sql, val)
                            pc.mydb.commit()

                            print(f'{sim1[1]} and {sim2[1]} are now in a relationship.', tag='Romance', color='white', tag_color='magenta')
                    elif sim2[2] < 18:
                        print(f'{sim1[1]} tried to date a minor, shame on you!', tag='Romance', color='white', tag_color='red')
                    else:
                        print(f'{sim1[1]} asked out {sim2[1]}, but got rejected.', tag='Romance', color='white', tag_color='magenta')

def birth(simName):
    cursor = pc.mydb.cursor()
    randomNum = random.choices([0, 1], weights=[5, 95])[0]  # Access the first element directly
    
    if randomNum == 1:
        print(f'{simName} is thinking about kids.', tag='Birth', tag_color='cyan', color='white')
    else:
        sql = 'SELECT * FROM pysims WHERE name = %s'
        val = [simName]
        cursor.execute(sql, val)
        ures = cursor.fetchone()

        if ures[6] == 1:  # Check if the sim is married
            partner_id = ures[5]  # Assuming partner column is at index 5
            sql = 'SELECT * FROM pysims WHERE sim_id = %s'
            val = [partner_id]
            cursor.execute(sql, val)
            ures2 = cursor.fetchone()

            if ures2:
                randomNum = random.choices([0, 1], weights=[50, 50])[0]  # Adjust weights as necessary
                if randomNum == 1:
                    print(f'{simName} and {ures2[1]} are thinking about kids.', tag='Birth', tag_color='cyan', color='white')
                else:
                    randomNum = random.choices([0, 1])[0]
                    if randomNum == 0:
                        print(f'{simName} and {ures2[1]} had a son!', tag='Birth', tag_color='cyan')
                        name = str(input('Name their son:\n'))
                        addSim(name, 0, 'male')
                    else:
                        print(f'{simName} and {ures2[1]} had a daughter!', tag='Birth', tag_color='cyan')
                        name = str(input('Name their daughter:\n'))
                        addSim(name, 0, 'female')
            else:
                print(f'{simName} does not have a valid partner.', tag='Error', color='red')
        else:
            print(f'{simName} is not married and cannot have children.', tag='Birth', tag_color='cyan', color='white')

def eventSelector(simName):
    eventTypes = ['Regular', 'Friendship', 'Carreer', 'Romance', 'Birth', 'Death']
    RandomEvent = random.choices(eventTypes, weights=(75, 10, 3, 4, 1, 1))

    cursor = pc.mydb.cursor()
    sql = "SELECT * FROM pysims"
    cursor.execute(sql)
    result = cursor.fetchall()

    for id, name, age, occupation, gender, partner, married in result:
        for x in RandomEvent:
            if name == simName:    
                if x == 'Regular':
                    print(f'{simName} had a normal day today', tag='Regular', tag_color='blue', color='white')
                elif x == 'Friendship':
                    newFriend(simName)
                elif x == 'Carreer':
                    newCarreer(simName)
                elif x == 'Romance':
                    romance(simName)
                elif x == 'Birth':
                    birth(simName)
                else:
                    if age <= 80:
                        randomNum = random.choices([0,1], weights= [999999999999999999999, 1])
                        if config.dieInAccident == True:    
                            if randomNum == 0:
                                print(f'{simName} had a normal day today', tag="Regular", tag_color="blue", color='white')
                            else:
                                print(f'{simName} has died in an accident :(', tag="Death", tag_color="red", color='white')
                                killSim(simName)
                        else:
                            print(f'{simName} had a normal day today', tag="Regular", tag_color="blue", color='white')
                    else:
                        print(f'{simName} has died of old age :(', tag="Death", color="white", tag_color='red')
                        killSim(simName)

def childEventSelector(simName):
    childEventTypes = ['regular', 'friendship', 'school']
    randomChildEvent = random.choices(childEventTypes, weights=[65, 15, 20])

    cursor = pc.mydb.cursor()
    sql = "SELECT * FROM pysims"
    cursor.execute(sql)
    result = cursor.fetchall()

    for id, name, age, occupation, gender, partner, married in result:
        if name == simName and age < 18:
            for x in randomChildEvent:
                if x == 'regular':
                    print(f'{name} had a normal day today', tag='Regular (child)', color='white', tag_color='blue')
                elif x == 'friendship':
                    newFriend(simName)
                else:
                    print(f'{name} passed a major test at school', tag='School (child)', color='white', tag_color='yellow')

def dailyActivity():
    cursor = pc.mydb.cursor()

    sql = "SELECT * FROM pysims"
    cursor.execute(sql)
    result = cursor.fetchall()

    for id, name, age, occupation, gender, partner, married in result:
        if age < 18:
            childEventSelector(name)
        else:    
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
            cmd = int(input('What do you want to do?: '))

            if cmd == 1:
                pass
            elif cmd == 2:
                name = str(input("What is the new Pysim's name?: "))
                age = str(input(f"What is {name}'s age?: "))
                gender = str(input(f"What is the gender of this {name}? (male/female): "))
                if gender == 'male' or gender == 'female':
                    addSim(name, age, gender)
                else:
                    print('Invalid gender.')
            elif cmd == 3:
                name = str(input("What Pysim do you want to kill?: "))
                killSim(name)
            elif cmd == 4:
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

                for id, name, age, occupation, gender, partner, married in result:
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