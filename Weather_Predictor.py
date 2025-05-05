#import what we neeed.
import time
import board
import neopixel
from datetime import datetime
from sklearn.cluster import KMeans
from meteostat import Point, Daily
import numpy as np

# LED strip configuration. Lets the code talk to the LEDs themselves.
LED_COUNT = 24         # Number of LEDs in the ring. The one I used has 24 LEDs, so I use 24.
LED_PIN = board.D18    # GPIO pin connected to the DIN on the ring
LED_BRIGHTNESS = 0.1   # Brightness (0.0 to 1.0) Check your power settings!
LED_ORDER = neopixel.GRB  # WS2812B order

# Create the NeoPixel object, which is how we'll communicate with the LEDS.
pixels = neopixel.NeoPixel(
    LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False, pixel_order=LED_ORDER
)
#Create a color variable to change the color of the LEDS.
COLOR = (0,0,255)

#METEOSTAT STUFF
#First we get the temperature of NYC every day for a year. Say, 2022.
Year = 2022
print("Getting the temperature data of NYC every day for the year of "+str(Year))
start = datetime(Year, 1, 1)
end = datetime(Year, 12, 31)
Location = Point(40.78325, -73.96565)
#Those coords correspond to New York City. Now get the data.
TempData = Daily(Location, start, end)
TempData = TempData.fetch()
TEMP = TempData['tavg'].mean()
#Now that we have a great big list of data, we need to sort it into something Kmeans can understand: a 2d array. Start with an empty array
KManData = []
#Add our temp data into it
for Data in TempData['tavg']:
        KManData.append([Data])
#CREATE THE KMEANS-MACHINE AND TRAIN IT ON THE DATA. We will call him KMan.
KMan = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(KManData)
#FIND OUR CLUSTERS: Clusters are where KMan thinks the data 'clusters' around. Even if data is relatively spread we told him to find 3 clusters and he does his best.
ClusterCenters = KMan.cluster_centers_.flatten()
Sorted_indices = ClusterCenters.argsort()
#APPLY LABELS. This will be to make the data human-readable.
Labels = {Sorted_indices[0]: "Cold",
        Sorted_indices[1]: "Temperate",
        Sorted_indices[2]: "Hot"}
#KMAN GUESSES CURRENT DAY
#GET OUR CURRENT TEMP
Now = datetime.now()
ModernYear = Now.year
ModernMonth = Now.month
ModernDay = Now.day
NewStart = datetime(ModernYear, ModernMonth, ModernDay)
NewEnd = datetime(ModernYear, ModernMonth, ModernDay)
TodaysData = Daily(Location, NewStart, NewEnd)
TodaysData = TodaysData.fetch()
TodaysActualTemp = TodaysData['tavg'][0]
#KMAN THINKS
KManGuesses = KMan.predict([[TodaysActualTemp]])[0]
KManHumanReadable = Labels[KManGuesses]
#GET KMANS THOUGHTS
print ("KMan has guessed the temperature "+str(TodaysActualTemp)+" is "+str(KManHumanReadable)+" for the date "+str(ModernDay)+"/"+str(ModernMonth)+"/"+str(ModernYear)+" (Day/Month/Year)")
#Depending on KMan's thoughts, we change what the color will be.
if KManHumanReadable=="Cold":
        COLOR = (0,0,255)
elif KManHumanReadable=="Temperate":
        COLOR = (255,255,0)
else:
        COLOR = (255,0,0)

# Function to actually turn the lights on when KMan is done thinking.
def test_leds(delay=0.02): #The delay parameter is a holdover from an earlier test. I leave it in here since it makes no difference one way or another.
    while True:
        for i in range(255):
            pixels.fill((0, 0, 0))# Turn off all LEDs
            pixels.fill(COLOR)    # Light up every LED in color
            pixels.show() #Actually light them.
            time.sleep(delay) #Wait for the delay-time.

try:
    test_leds()

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))  # Turn off LEDs when exiting
    pixels.show()
