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
import matplotlib
import matplotlib.pyplot as plt
import threading
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from numpy import arange, sin, pi


def data_generation():
    global final_data
    final_data = []
    global TemperatureList
    TemperatureList = []
    global HumidityList
    HumidityList = []
    global TemperatureListInside
    TemperatureListInside = []
    global HumidityListInside
    HumidityListInside = []
    fake = Faker()

    n = 1000
    no_of_sensor_data = 1000

    # other data
    starting_data = date(2015, 1, 15)
    end_date = date(2020, 12, 5)
    days = end_date - starting_data
    series = fake.time_series(start_date='-' + str(days.days + 1) + 'd',
                              end_date=str(int(no_of_sensor_data / 4) - days.days) + 'd',
                              precision=int(6 * 60 * 60))
    x = [val[0] for val in series]
    dates = []
    times = []
    for i in x:
        dates.append(str(i.year) + "-" + str(i.month) + "-" + str(i.day))
        times.append(str(i.hour) + "-" + str(i.minute) + "-" + str(i.second))

    # getting and storing the data in
    for i in range(n):

        # prepering sensor data
        sensor_data = []
        for j in range(no_of_sensor_data):
            OutsideTemperature = fake.random_int(70, 95)
            OutsideHumidity = fake.random_int(50, 95)

            sensor_data_skeleton = {
                "Date": dates[j],
                "Time": times[j],
                "Outside Temperature": OutsideTemperature,
                "Outside Humidity": OutsideHumidity,
                "Room Temperature": OutsideTemperature - fake.random_int(0, 10),
                "Room Humidity": OutsideHumidity - fake.random_int(0, 10),
            }
            sensor_data.append(sensor_data_skeleton)
        TemperatureList.append(OutsideTemperature)
        HumidityList.append(OutsideHumidity)
        HumidityListInside.append((OutsideHumidity - fake.random_int(0, 10)))
        TemperatureListInside.append(OutsideTemperature - fake.random_int(0, 10))
        # getting profile
        profile = fake.simple_profile()

        # storing for i th user
        data_skeleton = {
            "Firstname": str(profile["name"]).split(" ")[0],
            "Lastname": fake.last_name(),
            "age": fake.random_int(0, 100),
            "gender": profile["sex"],
            "username": profile["username"],
            "address": profile["address"],
            "email": profile["mail"],
            "sensor_data": sensor_data
        }

        final_data.append(data_skeleton)
class windowClass(wx.Frame):

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

        generatePlot = wx.Menu()

        saveItem.Append(id=0, item='Save as JSON')
        saveItem.Append(id=1, item='Save as CSV')

        plotItem.Append(id=2, item='Plot A')
        plotItem.Append(id=3, item='Plot B')
        plotItem.Append(id=4, item='Plot C')

        #       Build a menu entry - text only
        exitItem = exitButton.Append(wx.ID_EXIT, 'Exit', 'Exit Program ...')
        #        ID_HOST = wx.NewId()

        generateItem = generateButton.AppendSubMenu(saveItem, 'Generate IoT Data')

        # generatePlot = plotItem.AppendSubMenu(generatePlot, 'Generate Plot')

        menuBar.Append(generateButton, 'Generate')
        menuBar.Append(plotItem, 'Plot')
        menuBar.Append(exitButton, 'Exit')

        self.SetMenuBar(menuBar)

        self.Bind(event=wx.EVT_MENU, handler=self.viewGenerate)
        self.Bind(event=wx.EVT_TOOL, handler=self.onHandleButtons)
        self.Bind(event=wx.EVT_TOOL, handler=self.onHandleButtons)

        self.Bind(event=wx.EVT_MENU, handler=self.plotTime)
        self.Bind(event=wx.EVT_TOOL, handler=self.onHandleButtons)
        self.Bind(event=wx.EVT_TOOL, handler=self.onHandleButtons)
        self.Bind(event=wx.EVT_TOOL, handler=self.onHandleButtons)

        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Working... I think')

        self.SetTitle('SAMPLE - My Application ')
        self.Show(True)

    def onHandleButtons(self, e):
        if e.GetId() == 0:
            self.saveJSON(e)
        elif e.GetId() == 1:
            self.saveCSV(e)
        elif e.GetId() == 2:
            self.plotA(e)
        elif e.GetId() == 3:
            self.plotB(e)
        elif e.GetId() == 4:
            self.plotC(e)

    def viewGenerate(self, e):

        self.statusbar.SetStatusText('Generating Data')

    def plotTime(self, e):

        self.statusbar.SetStatusText('Generating Plots... maybe')
        e.Skip()

    def plotA(self, e):
        plt.close()
        plt.clf()
        plt.style.use('fivethirtyeight')

        data = TemperatureList

        plt.hist(data, bins=20, edgecolor='black')

        plt.title('Plot A - Histogram of Outside Temperature')
        plt.xlabel('Degrees')
        plt.ylabel('Occurrences')

        plt.tight_layout()

        fig = plt.gcf()
        fig.show()

        self.statusbar.SetStatusText('Plot A is a Histogram of outside temperature...')

    def plotB(self, e):
        plt.close()
        plt.clf()
        data = TemperatureList
        data3 = TemperatureListInside

        plt.plot(TemperatureList, color='red', marker='o', markersize=3, label='Outside', linewidth=1)
        plt.plot(TemperatureListInside, color='blue', marker='o', markersize=3, label='Inside', linewidth=1)
        plt.title('Outside VS Inside Temperature')
        plt.grid(True)
        plt.legend()

        fig = plt.gcf()
        fig.show()

        self.statusbar.SetStatusText('Plot B is a Line graph of outside vs inside temps...')

    def plotC(self, e):
        plt.close()
        plt.clf()
        data = TemperatureList
        data2 = HumidityList
        data3 = TemperatureListInside
        data4 = HumidityListInside

        plt.style.use('fivethirtyeight')
        fig, axes = plt.subplots(nrows=2, ncols=2)
        ax0, ax1, ax2, ax3 = axes.flatten()

        ax0.hist(data, bins=20, edgecolor='black', label="Outside Temp")
        ax0.set_title('Histogram of Outside Temperature')
        ax0.set_xlabel('Degrees')

        ax1.hist(data2, bins=20, edgecolor='black', label="Outside Humidity")
        ax1.set_title('Histogram of Outside Humidity')
        ax1.set_xlabel(' Humidity Percentage')

        ax2.hist(data3, bins=20, edgecolor='black', label='Inside Temp')
        ax2.set_title('Histogram of Inside Temperature')
        ax2.set_xlabel('Degrees')

        ax3.hist(data4, bins=20, edgecolor='black', label='Inside Humidity')
        ax3.set_title('Histogram of Inside Humidity')
        ax3.set_xlabel('Humidity percentage')

        fig.tight_layout()

        fig = plt.gcf()
        fig.show()

        self.statusbar.SetStatusText('Plot C Histogram of outside vs inside temps and humidity...')

    def saveJSON(self, e):

        name_JSON = input("Save file as?")
        name_JSON = name_JSON + ".json"
        with open(name_JSON, 'w') as json_file:
            json.dump(final_data, json_file)

        # self.statusbar.SetStatusText('Saving as JSON')

    def saveCSV(self, e):

        name_CSV = input("Save file as?" + ".csv")
        name_CSV = name_CSV + ".json"
        with open(name_CSV, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(final_data)

        self.statusbar.SetStatusText('Saving as CSV')


def main():
    th = threading.Thread(target=data_generation())
    th.start()
    app = wx.App()
    windowClass(None, 0, size=(500, 400))
    th2 = threading.Thread(target=app.MainLoop())
    th2.start()


main()
