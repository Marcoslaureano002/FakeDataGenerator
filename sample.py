# import requests 
# import json
# import sys
# import pyodbc
import os
import wx
import json
import csv
import arrow
from pandas import DataFrame
import pandas as pd
from faker import Faker
from datetime import date
from collections import Counter

class windowClass(wx.Frame):
    words1=[]
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, **kwargs)

        self.Centre()
        self.basicGUI()

    def basicGUI(self):

        panel = wx.Panel(self)

        menuBar = wx.MenuBar()

        generateButton = wx.Menu()
        exitButton = wx.Menu()
        plotItem = wx.Menu()
        saveItem = wx.Menu()
        viewItem = wx.Menu()
        
        saveItem.Append(wx.ID_ANY, 'Save as JSON')
        saveItem.Append(wx.ID_ANY, 'Save as CSV')
        
        plotItem.Append(wx.ID_ANY, 'Plot A')
        plotItem.Append(wx.ID_ANY, 'Plot B')
        plotItem.Append(wx.ID_ANY, 'Plot C')
       

        #       Build a menu entry - text only
        exitItem = exitButton.Append(wx.ID_EXIT, 'Exit', 'Exit Program ...')
        #        ID_HOST = wx.NewId()
        
        generateItem = generateButton.AppendMenu(wx.ID_ANY, 'Generate IoT Data', saveItem)
        generatePlot = generateButton.AppendMenu(wx.ID_ANY, 'Generate Plot', plotItem)        

        menuBar.Append(generateButton, 'Generate')
        menuBar.Append(exitButton, 'Exit')

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.viewGenerate, generateItem)
        self.Bind(wx.EVT_TOOL, self.saveJSON)
        self.Bind(wx.EVT_TOOL, self.saveCSV)
        
        self.Bind(wx.EVT_MENU, self.plotTime, generatePlot)
        self.Bind(wx.EVT_TOOL, self.plotA)
        self.Bind(wx.EVT_TOOL, self.plotB)
        self.Bind(wx.EVT_TOOL, self.plotC)

        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Working... I think')

        self.SetTitle('SAMPLE - My Application ')
        self.Show(True)
        
      
        
    def viewGenerate(self, e):

        self.statusbar.SetStatusText('Generating Data')
        
                
    def saveJSON(self, e):
        fake = Faker() 


        # In[649]:


        #finalData
        #finalData will be list of element (list of dictionerys(same as data_skeleton))
        final_data = []

        #noof data required
        n = 1000
        no_of_sensor_data = 1000


        #other data
        starting_data = date(2015, 1, 15)
        end_date = date(2020, 12, 5)
        days = end_date - starting_data
        series = fake.time_series(start_date='-'+str(days.days + 1)+'d', end_date=str(int(no_of_sensor_data/4)-days.days)+'d', precision=int(6*60*60))
        x = [val[0] for val in series]
        dates = []
        times = []
        for i in x:
            dates.append(str(i.year)+"-"+str(i.month)+"-"+str(i.day))
            times.append(str(i.hour)+"-"+str(i.minute)+"-"+ str(i.second))


        # In[650]:


        #getting and storing the data in 
        for i in range(n):
            
            #prepering sensor data
            sensor_data = []
            for j in range(no_of_sensor_data):
                OutsideTemperature = fake.random_int(70, 95)
                OutsideHumidity = fake.random_int(50, 95) 
                sensor_data_skeleton = {
                    "Date":dates[j],
                    "Time":times[j],
                    "Outside Temperature":OutsideTemperature,
                    "Outside Humidity":OutsideHumidity,
                    "Room Temperature":OutsideTemperature - fake.random_int(0, 10),
                    "Room Humidity":OutsideHumidity - fake.random_int(0, 10)
                }
                sensor_data.append(sensor_data_skeleton)
            
            #getting profile
            profile = fake.simple_profile()
            
            #storing for i th user
            data_skeleton = {
                 "Firstname":str(profile["name"]).split(" ")[0],
                 "Lastname": fake.last_name(), 
                 "age":fake.random_int(0, 100),
                 "gender": profile["sex"],
                 "username": profile["username"],
                 "address":profile["address"],
                 "email": profile["mail"],
                 "sensor_data" : sensor_data
            }
            
            final_data.append(data_skeleton)
            
        name_JSON = input("Save file as?")
        with open(name_JSON, 'w') as json_file:
            json.dump(final_data, json_file)
                   
        self.statusbar.SetStatusText('Saving as JSON')
    #saveJSON(final_data)
        
        
    def saveCSV(self, e):
        fake = Faker() 


        # In[649]:


        #finalData
        #finalData will be list of element (list of dictionerys(same as data_skeleton))
        final_data = []

        #noof data required
        n = 1000
        no_of_sensor_data = 1000


        #other data
        starting_data = date(2015, 1, 15)
        end_date = date(2020, 12, 5)
        days = end_date - starting_data
        series = fake.time_series(start_date='-'+str(days.days + 1)+'d', end_date=str(int(no_of_sensor_data/4)-days.days)+'d', precision=int(6*60*60))
        x = [val[0] for val in series]
        dates = []
        times = []
        for i in x:
            dates.append(str(i.year)+"-"+str(i.month)+"-"+str(i.day))
            times.append(str(i.hour)+"-"+str(i.minute)+"-"+ str(i.second))


        # In[650]:


        #getting and storing the data in 
        for i in range(n):
            
            #prepering sensor data
            sensor_data = []
            for j in range(no_of_sensor_data):
                OutsideTemperature = fake.random_int(70, 95)
                OutsideHumidity = fake.random_int(50, 95) 
                sensor_data_skeleton = {
                    "Date":dates[j],
                    "Time":times[j],
                    "Outside Temperature":OutsideTemperature,
                    "Outside Humidity":OutsideHumidity,
                    "Room Temperature":OutsideTemperature - fake.random_int(0, 10),
                    "Room Humidity":OutsideHumidity - fake.random_int(0, 10)
                }
                sensor_data.append(sensor_data_skeleton)
            
            #getting profile
            profile = fake.simple_profile()
            
            #storing for i th user
            data_skeleton = {
                 "Firstname":str(profile["name"]).split(" ")[0],
                 "Lastname": fake.last_name(), 
                 "age":fake.random_int(0, 100),
                 "gender": profile["sex"],
                 "username": profile["username"],
                 "address":profile["address"],
                 "email": profile["mail"],
                 "sensor_data" : sensor_data
            }
            
            final_data.append(data_skeleton)
        name_CSV= input("Save file as?")
        with open(name_CSV, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(final_data)
                   
        self.statusbar.SetStatusText('Saving as CSV')
        
    def plotTime(self, e):

                
        self.statusbar.SetStatusText('Plotting Time...')
        
    def plotA(self, e):
        self.statusbar.SetStatusText('Plotting A - Histogram of outside temperature...')
    def plotB(self, e):
        self.statusbar.SetStatusText('Plotting B - Line graph of outside vs room temperature...')
    def plotC(self, e):
        self.statusbar.SetStatusText('Plotting C - Histogram of room and outside temperature and humidity...')
        
                        
                    
def main():
    app = wx.App()
    windowClass(None, 0, size=(500, 400))
    
    app.MainLoop()
    
main()

