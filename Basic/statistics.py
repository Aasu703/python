import numpy as np

# to generate data in numpy using random

height = np.round(np.random.normal(1.75, 0.20, 5000), 2)
weight = np.round(np.random.normal(60.32, 15, 5000), 2)

np_city = np.column_stack((height,weight))

print(height)
print(weight)


import numpy as np

# Create np_height_in from np_baseball
np_height_in = np.array([70, 71, 72, 73, 74])



# Print out the mean of np_height_in
print(np.mean(np_height_in))

# Print out the median of np_height_in
print(np.median(np_height_in))

print(np.std(np_height_in))
# print out corelation coefficient between first and second column
print(np.corrcoef(np_city[:,0], np_city[:,1]))