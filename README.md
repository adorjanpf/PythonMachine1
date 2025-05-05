# PythonMachine1
Python_MachineLearning_Example1

This code serves as a proof of concept for Machine Learning principals, using a 24-LED ring and a Raspberry Pi Micro.

Code Goal: Determine if the current temperature in New York City is hot, temperature, or cold. Once done, light up the LED either red, yellow, or blue respectively.

This is done by first retrieving the meteorological data for every day in the year of 2022 (chosen arbitrarily) for NYC. A K-Means algorithm then trains on this data.

Once trained, the algorithm is provided the current temperature for NYC and sorts it based on temperature. The LED ring then lights up correspondingly.

K-Means is an unsupervised algorithm; I do not tell it "This temperature, which was 5C, is considered cold. This temperature, which was 26C, is considered hot, etc." Rather, it simply receives the data and finds clusters on its own.
