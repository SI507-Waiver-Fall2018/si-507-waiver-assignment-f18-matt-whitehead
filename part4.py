# Imports -- you may add others but do not need to
import plotly.plotly as py
import plotly.graph_objs as go
import csv

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets

#read in csv file
x_list = []
y_list = []
with open('noun_data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for x,y in csv_reader:
        x_list.append(x)
        y_list.append(y)

#plot and save file
py.sign_in('mww113', 'fyZQZaYVJdcHxyLX9qYf')
trace = go.Bar(x= x_list[1:], y= y_list[1:])
data = [trace]
layout = go.Layout(title='Noun Data Frequencies', width=800, height=640)
fig = go.Figure(data=data, layout=layout)
py.image.save_as(fig, filename='part4_viz_image.png')
