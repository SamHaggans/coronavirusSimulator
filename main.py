from tkinter import *
import csv
import time
import math
from math import sin, cos, tan, asin, acos, atan
import random

class Population:
    def __init__(self, canvas, x, y, width, popWidth, infectChance, outsideChance, treatments):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x + width, y + width)
        self.availableTreatments = treatments
        creationWidth = width/popWidth
        self.count = [0, 0, 0, 0, 0, 0]
        self.countText = canvas.create_text(x, y-20, anchor="nw", text = "Healthy: 0; Carriers: 0; Infected: 0; Treated: 0; Recovered: 0; Dead: 0;", font=("Courier", 10))
        self.people = []
        self.surroundings = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        for row in range(popWidth):
            rowArr = []
            for col in range(popWidth):
                status = 0
                if (random.uniform(0,1) < infectChance):
                    status = 1
                rowArr.append(Person(self.canvas, status, outsideChance, row, col, creationWidth, x, y))
            self.people.append(rowArr)
    def run(self):
        people = self.people
        for row in range(len(people)):
            for col in range(len(people)):
                for surrounding in self.surroundings:
                    testRow = row + surrounding[0]
                    testCol = col + surrounding[1]
                    if testRow >=0 and testCol >=0 and testRow < len(people) and testCol < len(people):
                        if people[testRow][testCol].canInfect():
                            people[row][col].getInfected()
        self.count = [0, 0, 0, 0, 0, 0]
        for row in range(len(people)):
            for col in range(len(people)):
                if (people[row][col].status == 2 and self.availableTreatments > 0):
                    people[row][col].getTreatment()
                    self.availableTreatments-=1
                if (people[row][col].status == 4 or people[row][col].status == 5) and people[row][col].hasTreatment:
                    people[row][col].hasTreatment = False
                    self.availableTreatments +=1
                people[row][col].updateSelf()
                val = people[row][col].status
                self.count[val] +=1
        self.canvas.itemconfig(self.countText, text = "Healthy: %d; Carriers: %d; Infected: %d; Treated: %d; Recovered: %d; Dead: %d;"%(self.count[0], self.count[1], self.count[2], self.count[3], self.count[4], self.count[5]))
class Person:
    def __init__(self, canvas, status, outsideChance, col, row, width, initX, initY):
        self.canvas = canvas
        self.status = status
        self.outsideChance = outsideChance
        self.hasTreatment = False
        if (self.status == 0):#healthy
            self.color = "green"
        elif (self.status == 1):#carrier
            self.color = "yellow"
        elif (self.status == 2):#symptoms, untreated
            self.color = "red"
        elif (self.status == 3):#treated
            self.color = "purple"
        elif (self.status == 4):#recovered
            self.color = "blue"
        elif (self.status == 5):#dead
            self.color = "black"
        self.infectedDays = 0
        self.treatedDays = 0
        self.id = canvas.create_rectangle(initX + col * width, initY +row * width, initX + col * width + width, initY +row * width + width, fill = self.color)
    def getInfected(self):
        if self.status == 0 and random.uniform(0,1) < self.outsideChance and random.uniform(0, 1) > 0.66:
            self.status = 1
    def canInfect(self):
        return (random.uniform(0,1) < self.outsideChance and self.status == 1)
    def getTreatment(self):
        self.status = 3
        self.hasTreatment = True
    def updateSelf(self):
        if self.status == 1 or self.status == 2 or self.status == 3:
            self.infectedDays +=1
        if self.status == 3:
            self.treatedDays +=1 
        if self.infectedDays >=10 + 3*random.uniform(-1, 1) and self.status == 1:
            self.status = 2
        if self.infectedDays >= 20 + 3*random.uniform(-1, 1):
            if (self.status == 3 and self.treatedDays > 6):
                self.status = 4
                self.infectedDays = 0
            else:
                if (random.uniform(0, 1) < 0.3):
                    self.status = 5
        if (self.status == 0):#healthy
            self.color = "green"
        elif (self.status == 1):#carrier
            self.color = "yellow"
        elif (self.status == 2):#symptoms, untreated
            self.color = "red"
        elif (self.status == 3):#treated
            self.color = "purple"
        elif (self.status == 4):#recovered
            self.color = "blue"
        elif (self.status == 5):#dead
            self.color = "black"
        self.canvas.itemconfig(self.id, fill = self.color)

def simulation(width, height, dayCount, popDimensions):
    popWidth = int(input("Width (and height) of population (total population is this number squared) (700 needs to be divisible by this number): "))
    infectRate = float(input("% (as a decimal) of people that start infected: "))
    treatmentNum =int(input("Number of treatment stations (ventilators, hospitals, etc.) available: "))
    pop1Outside = float(input("Chance someone goes outside for pop 1: "))
    pop2Outside = float(input("Chance someone goes outside for pop 2: "))
    master = Tk()
    canvas = Canvas(master, 
           width=width,
           height=height)

    canvas.pack()
    master.title("Coronavirus Spread Simulation")
    master.resizable(0, 0)
    master.update_idletasks()
    master.update()
    canvas.create_text(100, 10, anchor="nw", text = "Coronavirus Simulation: ", font=("Courier", 40))
    pop1 = Population(canvas, 100, 150, 700, popWidth, infectRate, pop1Outside, treatmentNum)
    pop2 = Population(canvas, 900, 150, 700, popWidth, infectRate, pop2Outside, treatmentNum)
    day = 0
    dayText = canvas.create_text(805, 300, anchor="nw", text = "Day %d" %(day), font=("Courier", 15))
    while day <= dayCount:
        day += 1
        canvas.itemconfig(dayText, text = "Day %d" %(day))
        pop1.run()
        pop2.run()
        #time.sleep(0.1)
        master.update_idletasks()
        master.update()


canvas_width = 1700
canvas_height = 900


simulation(canvas_width, canvas_height, 500, 1000)
