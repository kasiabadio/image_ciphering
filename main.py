from tkinter import *
from tkinter import filedialog
import os
import imagesize
import numpy as np
from PIL import Image

root = Tk()
root.geometry("200x160")


def create_blocks(_image, _block_size):

    print("Create blocks ...")
    blocks = []
    block = []
    j = 0
    for i in range(0, len(_image)):
        if j < _block_size:
            block.append(_image[i])
        else:
            blocks.append(block)
            block = []
            j = 0
        j += 1

    while len(blocks[-1]) < _block_size:
        blocks[-1].append(0)

    print("Liczba pixeli: ", len(_image))
    return blocks


def concatenate_blocks(_blocks):

    print("Concatenate blocks ...")
    block = []
    for b in _blocks:
        block.extend(b)

    return block


def block_operations(_curr_block, _prev_block, _key):

    # pixel based bitxor operation
    block = []
    for v_current, v_prev in zip(_curr_block, _prev_block):
        block.append(v_current ^ v_prev)

    i = 0
    for v_block, v_key in zip(_curr_block, _key):
        _curr_block[i] = v_block ^ v_key
        i += 1

    return block


def bytes_to_img(_pixels, _width, _height):

    print("Bytes to image ...")

    pixels_2D = []
    list_comprehension = []
    for _ in range(_height):
        list_comprehension.extend([w for w in range(_width)])

    indices_pixels = [ind for ind in range(len(_pixels))]
    print("Should be this many pixels: ", len(
        list_comprehension), " is: ", len(indices_pixels))

    temp = []
    counter = 0
    for p, i in zip(indices_pixels, list_comprehension):
        if i < _width:
            temp.append(_pixels[p])
        if i == _width - 1:
            pixels_2D.append(temp)
            counter += 1

    array = np.array(pixels_2D, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save("encoded.png")


def encrypt_image():

    # original image file
    file1 = filedialog.askopenfile(
        mode='r', filetypes=(("jpg file", "*.jpg"),))

    if file1 is not None:
        file_name = file1.name
        block_length = 16

        key = os.urandom(block_length)
        fi = open(file_name, 'rb')

        image = fi.read()
        fi.close()
        width, height = imagesize.get("sunflower.jpg")

        image = bytearray(image)
        vector_IV = os.urandom(block_length)
        blocks = create_blocks(image, block_length)
        for round in range(10):
            print("Block operations ... ", str(round))
            prev_block = vector_IV
            for b in range(len(blocks)):
                block = block_operations(blocks[b], prev_block, key)
                blocks[b] = block
                prev_block = block

        blocks_conc = concatenate_blocks(blocks)
        bytes_to_img(blocks_conc, width, height)

        fi1 = open(file_name, 'wb')
        fi1.write(image)
        fi1.close()


if __name__ == '__main__':

    b1 = Button(root, text="encrypt", command=encrypt_image)
    b1.place(x=70, y=10)
    root.mainloop()
