# low = 0 # what is the starting point of the array
# high = len(arr) - 1 # what is the ending point of the array

# mid = (low + high) // 2 # what is the middle point of the array
# guess = arr[mid] # what is the value at the middle point of the array

# if guess<item:
#     low = mid + 1 # if the guess is too low, we need to look in the upper half of the array
# elif guess>item:
#     high = mid - 1 # if the guess is too high, we need to look in the lower half of the array


def binary_search(arr, item):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = arr[mid]

        if guess == item:
            return mid
        elif guess < item:
            low = mid + 1
        else:
            high = mid - 1

    return None