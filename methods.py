# fam = ['liz', 1.73, 'emma', 1.68, 'mom', 1.9,'dad', 1.85]
# fam.index('mom')
# print(fam.index('mom'))
# print(fam.count(1.73))

# string to experiment with: place
# place = "poolhouse"

# # Use upper() on place
# place_up = place.upper()

# # Print out place and place_up
# print(place)
# print(place_up)


# # Print out the number of o's in place
# print(place.count('o'))

# areas = [11.25, 18.0, 20.0, 10.75, 9.50]
# print(areas.index(20.0))
# # Print out how often 9.50 appears in areas
# print(areas.count(9.50))


# Create list areas
areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Use append twice to add poolhouse and garage size

areas.append(24.5)
areas.append(15.45)

# Print out areas
print(areas)

# Reverse the orders of the elements in areas
areas=sorted(areas, reverse=True)
# Print out areas
print(areas)