# Numeric Python (NumPy) library import

import numpy as np
height = [1.73, 1.68, 1.71, 1.89, 1.79]
np_height = np.array(height)
print(np_height)

weight = [65.4, 59.2, 63.6, 88.4, 68.7]
np_weight = np.array(weight)
print((np_height/np_height)**2)

print((height/weight)**2)  # This will raise an error since height and weight are lists


# Import the numpy package as np


baseball = [180, 215, 210, 210, 188, 176, 209, 200]

# Create a numpy array from baseball: np_baseball
np_baseball = np.array(baseball)

# Print out type of np_baseball
print(type(np_baseball))

# Import numpy

# Create a numpy array from height_in: np_height_in
height_in=[65, 68, 69, 71, 72]
np_height_in = np.array(height_in)

# Print out np_height_in
print(np_height_in)

# Convert np_height_in to m: np_height_m
np_height_m = np_height_in * 0.0254 


# Print np_height_m
print(np_height_m)



# Create a numpy array from height_in: np_height_in
height_in=[70,71,72,73,74]
np_height_in=np.array(height_in)
# Print out np_height_in
print(np_height_in)
# Convert np_height_in to m: np_height_m
np_height_m = np_height_in * 0.0254


# Print np_height_m
print(np_height_m)



x=[True, 1, 2]
y=[3,4, False]
np_x=np.array(x)
np_y=np.array(y)

print(np.array([True, 1, 2]) + np.array([3, 4, False]))
print(np_x + np_y)


np_weight_lb = np.array(weight_lb)
np_height_in = np.array(height_in)

# Print out the weight at index 50
print(np_weight_lb[50])

# Print out sub-array of np_height_in: index 100 up to and including index 110
print(np_height_in[100:111])

np_2d = ([1.73, 1.68, 1.71, 1.89, 1.79],
                  [65.4, 59.2, 63.6, 88.4, 68.7])

print(np_2d)

np_2d = np.array(np_2d)
print(np_2d)
print(np_2d.shape) # rows, columns



# Create a 2D numpy array from baseball: np_baseball
baseball = [[180, 215, 210, 210, 188],
            [65.4, 59.2, 63.6, 88.4, 68.7]]
np_baseball = np.array(baseball)

# Print out the shape of np_baseball
print(np_baseball.shape)

np_baseball = np.array(baseball)

# Print out the 50th row of np_baseball
print(np_baseball[49])

# Select the entire second column of np_baseball: np_weight_lb
np_weight_lb = np_baseball[1, :]

# Print out height of 124th player
print(np_baseball[0, 123])

np_baseball = np.array(baseball)

# Print out addition of np_baseball and updated
np_baseball + 10


# Create numpy array: conversion
conversion = np.array([0.0254, 0.453592, 1])


# Print out product of np_baseball and conversion
print(np_baseball * conversion)