import random


def generate_arr():
    arr = []
    for _ in range(256):
        integer = random.randint(0, 256)
        arr.append(bin(integer))

    arr2 = []
    for i in range(0, 256, 16):
        arr2.append(arr[i:(i+16)])

    return arr, arr2
