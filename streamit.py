import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure
import time
import datetime
import sys
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4
username = ''
api_key = ''
stream_token = ''

py.sign_in(username, api_key)

trace1 = Scatter(
    x=[],
    y=[],
    stream=dict(
        token=stream_token,
        maxpoints=200
    )
)

layout = Layout(
    title='Raspberry Pi Streaming Sensor Data',
    xaxis=dict(
        autorange=True
    ),
    yaxis=dict(
        autorange=True
    )
)

fig = Figure(data=[trace1], layout=layout)

print py.plot(fig, filename='Raspberry Pi Streaming Temp Data')

stream = py.Stream(stream_token)
stream.open()
while True:
    try:
        now = datetime.datetime.now()
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        f = open("temp_and_humidity.csv", "a")
        f.write("\r\n" + str(now) + "," + str(temperature) + "," + str(humidity))
        stream.write({'x': now, 'y': temperature})
        time.sleep(60)  # delay between stream posts
    except Exception as error:
        print("Exception occured: " + str(error))
