#!/usr/bin/env python
"""
https://github.com/octopusengine/py_icon
"""
import os
import pygame as p
import numpy as np
import random
from datetime import datetime

__version__ = "0.2.0" # 2023/06

DEBUG = True
fdatetime = True # False
icon_w, icon_h = 32, 32 #  32,32 / 16,16 / 16,32 / 32,64 / 64,64
I_W_MAX, I_H_MAX = 64,64

path = "data_img/"
image_path = f"{path}test_{icon_w}.bmp"
matrix_name = "mx_test"
text_import_g = f"{path}octopus.txt"
#text_import_d = f"{path}data_noise.txt"
text_import_d = f"{path}data_horse_noise.txt"
mouse_button_pressed = False

# Size of pixels in the editor
pixel_size = 10
if (icon_w + icon_h) > 65:
    pixel_size = 5

icon_array = np.zeros((I_W_MAX, I_H_MAX), dtype=np.uint8)
icon_data = np.zeros((I_W_MAX, I_H_MAX), dtype=bool)

# RGB colors      
WHITE = (255, 255, 255)
SILVER = (64, 64, 64)
SILVER2 = (128, 128, 128)
BLACK2 = (10, 10, 10)
BLACK = (0, 0, 0)
COLOR = (0, 128, 0)
COLOR2 = (0, 196, 0)

x0, y0 = 30, 50
window_width, window_height = 800, 480

xc = window_width/2 - 30
ic = (icon_w * pixel_size + x0) // 2
fstep = 22
resize = 3
input_text = ""
mode = 1
my_icon_matrix_load = []

# test add_matrix
add_bin_txt = """10000001000000000000111000000001
01000001000000000000100100000010
00100001000000000000101100000100
00010001000000000000110000001000
00001001000000000000101000010000
00000101111000000000100100100000
"""
# ...

matrix_txt = []
for line in add_bin_txt.splitlines():
    matrix_txt.append(line)

print(matrix_txt)

p.init()

# window_width, window_height = 16 * pixel_size, 16 * pixel_size
window = p.display.set_mode((window_width, window_height))
p.display.set_caption(f"py_icon (ver. {__version__})")
# window.fill(BLACK)

font_size = 18
font = p.font.SysFont("Arial", font_size)
#font = p.font.SysFont(None, font_size)


def rename_matrix_path(basic="basic"):
    if fdatetime:
        dt = datetime.now().strftime("%Y%m%d_%H%M%S")
        matrix_path = f"{path}_mx_{basic}_{icon_w}-{dt}.txt" 
    else:
        matrix_path = f"{path}_mx_{basic}_{icon_w}.txt"
    return matrix_path

matrix_path = rename_matrix_path("test")

def draw_text(text, x, y, col = COLOR): # Function to draw label/text
    text_surface = font.render(text, True, col)
    window.blit(text_surface, (x, y))


def draw_status(text, x=30, y=390):
    p.draw.rect(window, BLACK2, (x-5, y-5, xc-50, 29))
    text_surface = font.render(str(text), True, COLOR2)
    window.blit(text_surface, (x, y))


def draw_status2(text, x=xc, y=390):
    print("status2:", text)
    p.draw.rect(window, BLACK2, (x-5, y-5, xc-50, 29))
    text_surface = font.render(str(text), True, COLOR2)
    window.blit(text_surface, (x, y))


def draw_input_field():
    draw_text("New filename:",xc, y0+fstep*12, COLOR2)
    p.draw.rect(window, SILVER, (xc, y0+fstep*13, 170, 27))
    p.draw.rect(window, BLACK2, (xc, y0+fstep*13, 170, 27), 2)
    text_surface = font.render(input_text, True, BLACK)
    window.blit(text_surface, (xc+5, y0+fstep*13+3))


def draw_edit_icon():
    p.draw.rect(window, BLACK, (0, 0, window_width, 390))
    draw_text(f"icon {icon_w}x{icon_h} - {image_path}",x0, y0 -30, SILVER2)
    # window.fill((255, 255, 255))  # Clear the window content
    
    for y in range(icon_h):
        for x in range(icon_w):
            if icon_data[x][y]: # 15-y ???
                p.draw.rect(window, (0, 0, 0), (x0 + x * pixel_size, y0 + y * pixel_size, pixel_size, pixel_size))
            else:
                p.draw.rect(window, (255, 255, 255), (x0 + x * pixel_size, y0 + y * pixel_size, pixel_size, pixel_size))

    p.draw.rect(window, (0, 128, 255), (x0, y0, icon_w * pixel_size, icon_h * pixel_size), 2)

    rect_width, rect_height = 180, 320
    xc2 = xc + 35
    p.draw.rect(window, BLACK2, (xc-7, y0, rect_width, rect_height)) # middle info rect
    draw_text("CTRL + command:",xc, y0, COLOR2)
    
    draw_text("C/F",xc, y0+fstep*1, COLOR2)
    draw_text("Clear / Fill",xc2, y0+fstep*1)
    draw_text("R", xc, y0+fstep*2, COLOR2)
    draw_text("Resize 16/32/64", xc2, y0+fstep*2)
    draw_text("I",xc, y0+fstep*3, COLOR2)
    draw_text("Invert",xc2, y0+fstep*3)
    draw_text("N/B",xc, y0+fstep*4, COLOR2)
    draw_text("Noise / Border",xc2, y0+fstep*4)
    draw_text("Z/X",xc, y0+fstep*5, COLOR2)
    draw_text("Resize prew.",xc2, y0+fstep*5)
    draw_text("D/G",xc, y0+fstep*6, COLOR2)
    draw_text("Data / Graphics",xc2, y0+fstep*6)
    draw_text("A",xc, y0+fstep*7, COLOR2)
    draw_text("add ...",xc2, y0+fstep*7)
    draw_text("E", xc, y0+fstep*8, COLOR2)
    draw_text("Export (matrix)", xc2, y0+fstep*8)
    draw_text("L/S", xc, y0+fstep*9, COLOR2)
    draw_text("Load / Save", xc2, y0+fstep*9)
    draw_text("Q", xc, y0+fstep*10, COLOR2)
    draw_text("Quit", xc2, y0+fstep*10)

    # draw_text(f"R D/G/A S E / ...",x0, window_height-35, SILVER2)

    rect_width = 220
    p.draw.rect(window, SILVER, (window_width-rect_width-x0, y0, rect_width, rect_height))
    p.draw.rect(window, WHITE, (window_width-rect_width-x0, y0, rect_width, 100))
    p.draw.rect(window, BLACK, (window_width-rect_width-x0+110, y0, xc, 100))
    try:
        icon_saved = p.image.load(image_path)
        original_width, original_height = icon_saved.get_size()
        current_width, current_height = original_width * resize, original_height * resize
        window.blit(icon_saved, (window_width-rect_width-8, y0+15))
        window.blit(icon_saved, (window_width-rect_width+100, y0+15))
        window.blit(p.transform.scale(icon_saved, (current_width, current_height)), (window_width-rect_width-10, y0+fstep*5))
    except:
        draw_status(f"Err. {image_path}")

    draw_input_field()
    p.display.flip()


def icon_mode(mode,icon_w,icon_h):
    mode += 1
    if mode > 3: 
        mode = 1
    if mode == 1: icon_w, icon_h = 32,32
    if mode == 2: icon_w, icon_h = 16,16
    if mode == 3: icon_w, icon_h = 64,64
    draw_status(f"Mode > {mode}: {icon_w}x{icon_h}")

    return mode, icon_w, icon_h


def load_icon():
    draw_status("Load >")
    if os.path.exists(image_path):
        size = os.path.getsize(image_path)
        draw_status2(f"{image_path} ({size} Bytes)")
    else:    
        draw_status2(f"The file does not exist.")
    try:
        if DEBUG:
            icon_surface0 = p.image.load(image_path)
            width = icon_surface0.get_width()
            height = icon_surface0.get_height()
            bytes_per_pixel = icon_surface0.get_bytesize()
            file_size = os.path.getsize(image_path)
            print(f"{image_path}: {width}x{height}/{bytes_per_pixel} - ({file_size}B)")

        icon_surface = p.image.load(image_path).convert_alpha()
        #  icon_surface = p.transform.flip(icon_surface, False, True)  # Horizontal flip (for correct orientation)

        # Convert the icon to a data array
        icon_array = p.surfarray.pixels2d(icon_surface) # p.surfarray.array2d(icon_surface)
        icon_array = np.asarray(icon_array, dtype=np.uint8)
        # if DEBUG:
        #    print(icon_array)

        # Set the values in the editor icon based on the data array
        for y in range(icon_h):
            for x in range(icon_w):
                #icon_data[x][icon_h-y] = True if icon_array[x][y] < 128 else False
                icon_data[x][y] = True if icon_array[x][y] < 128 else False
                             ###15
        print("The icon was successfully loaded from the file.")
    except:
        draw_status(f"Err. Load {image_path}")


def save_icon():
    draw_status(f"save")
    
    # Set the values in the icon array based on the data in the editor icon
    for y in range(icon_h):
        for x in range(icon_w):
            icon_array[x][y] = 0 if icon_data[x][y] else 255

    # Create a surface for the icon and rotate it 180 degrees (upside down)
    icon_surface = p.surfarray.make_surface(icon_array[:icon_w, :icon_h])
    # exported_array = icon_array[:32, :32]
    #icon_surface = p.transform.flip(icon_surface, False, True)

    # Save the icon to a file
    p.image.save(icon_surface, image_path)
    print(f"The icon was successfully saved to the file {image_path}.")


def icon_clear():
    draw_status(f"clear > 0")
    icon_data.fill(False)


def icon_fill():
    draw_status(f"fill > 1")
    for y in range(icon_h):
        for x in range(icon_w):
            icon_data[x][y] = True


def icon_invert():
    draw_status(f"invert 0<->1")
    for y in range(icon_h):
        for x in range(icon_w):
            icon_data[x][y] ^= True


def icon_noise():
    draw_status(f"noise")
    for y in range(icon_h):
        for x in range(icon_w):
            icon_data[x][y] = random.randint(0, 1) # True


def icon_border():
    draw_status(f"border")
    for y in range(icon_h): # L vert.
        icon_data[0][y] = 1
        icon_data[icon_w-1][y] = 1

    for x in range(icon_w):
        icon_data[x][0] = 1
        icon_data[x][icon_h-1] = 1


def matrix_text_load(matrix_file): # icon or pattern/noise
    my_txt_matrix = []
    draw_status(f"text_matrix_load")
    draw_status2(matrix_file)

    if os.path.exists(matrix_file):    
        with open(matrix_file, "r") as file:
            lines = file.readlines()
            if DEBUG:
                print(f"icon setup: {icon_w}x{icon_h}")
                print(f"{matrix_file} -> lines: {len(lines)} / bites: ")

            for line in lines:
                cleaned_line = line.strip()
                #str_hex = bin_to_hex(str(cleaned_line),True,8)
                my_txt_matrix.append(cleaned_line)
    else:
        my_txt_matrix = matrix_txt
    return my_txt_matrix

            
def matrix_icon(offset):
    xx, yy = 0 , 0
    if icon_w == 64 and offset:
        xx, yy = 16 , 16  # 32 to 64 - offset: 16
    try:
        for y, row in enumerate(my_icon_matrix):
            for x, value in enumerate(row):
                icon_data[x+xx][y+yy] = True if value == '1' else False
    except:
        print("Err. Matrix")


def icon_export():
    draw_status(f"create and save binary data matrix")
    # Load the icon from a file
    if os.path.exists(image_path):
        size = os.path.getsize(image_path)
        draw_status2(f"{image_path} ({size} Bytes)")
    
        icon_surface = p.image.load(image_path)

        # Convert the icon to a data array
        icon_array = p.surfarray.array2d(icon_surface)
        icon_array = np.asarray(icon_array, dtype=np.uint8)
        # exported_array = icon_array[:32, :32]

        # Iterate over rows and columns of the icon
        for y in range(icon_h): # icon_array.shape[1]
            row = ""
            for x in range(icon_w): # icon_array.shape[0]
                value = icon_array[x][y]
                if value < 128:
                    row += "1"
                else:
                    row += "0"
            my_icon_matrix_load.append(row)
            print(row)
        
        draw_status2(matrix_path)       
    else:    
        draw_status2(f"The file does not exist.")

    with open(matrix_path, "w") as file:
        for row in my_icon_matrix_load:
            file.write(row + "\n")


# =================== start / and main loop ===============================
p.draw.rect(window, BLACK, (0, 0, window_width, window_height))
p.display.flip()
draw_text(f"R D/G/A S E / ...",x0, window_height-35, SILVER2)

running = True
draw_status(f"Start > {image_path}")

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEMOTION:
            if mouse_button_pressed:
                # Get the mouse coordinates
                mouse_x, mouse_y = event.pos

                # Convert the coordinates to pixel position in the matrix
                pixel_x = (mouse_x - x0) // pixel_size 
                pixel_y = (mouse_y - y0) // pixel_size
                draw_status(f"x:{pixel_x} | y:{pixel_y} > 0")

                try:
                    icon_data[pixel_x][pixel_y] = True
                except:
                    print("out of range")

                draw_edit_icon()
        
        elif event.type == p.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get the click coordinates
                mouse_button_pressed = True
                mouse_x, mouse_y = event.pos

                # Convert the coordinates to pixel position in the matrix
                pixel_x = (mouse_x - x0) // pixel_size 
                pixel_y = (mouse_y - y0) // pixel_size
                draw_status(f"x:{pixel_x} | y:{pixel_y} > 1")

                try:
                    icon_data[pixel_x][pixel_y] = 1
                except:
                    print("out of range")    
                draw_edit_icon()

            elif event.button == 3:  # Right mouse button
                # Get the click coordinates
                mouse_x, mouse_y = event.pos

                # Convert the coordinates to pixel position in the matrix
                pixel_x = (mouse_x - x0) // pixel_size 
                pixel_y = (mouse_y - y0) // pixel_size
                draw_status(f"x:{pixel_x} | y:{pixel_y} > 0")

                try:
                    icon_data[pixel_x][pixel_y] = False
                except:
                    print("out of range")
                draw_edit_icon()

        elif event.type == p.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                mouse_button_pressed = False

        elif event.type == p.KEYDOWN:
            if event.key == p.K_l and p.key.get_mods() & p.KMOD_CTRL:
                load_icon()

            elif event.key == p.K_s and p.key.get_mods() & p.KMOD_CTRL:
                save_icon()
            
            elif event.key == p.K_r and p.key.get_mods() & p.KMOD_CTRL:
                mode,icon_w,icon_h = icon_mode(mode,icon_w,icon_h)
                if (icon_w + icon_h) > 65:
                    pixel_size = 5 
                else:
                    pixel_size = 10
                image_path = f"{path}test_{icon_w}.bmp"
                draw_status2(f"zoom {image_path}")
                matrix_path = rename_matrix_path()
                print(matrix_path)

            elif event.key == p.K_z and p.key.get_mods() & p.KMOD_CTRL:
                resize += 1
                if resize > 4: 
                    resize = 4
                draw_status2(f"zoom {resize}")

            elif event.key == p.K_x and p.key.get_mods() & p.KMOD_CTRL:
                resize -= 1
                if resize == 0: 
                    resize = 1
                draw_status2(f"zoom {resize}")

            elif event.key == p.K_c and p.key.get_mods() & p.KMOD_CTRL:
                icon_clear()

            elif event.key == p.K_e and p.key.get_mods() & p.KMOD_CTRL: # create save data matrix
                icon_export()

            elif event.key == p.K_f and p.key.get_mods() & p.KMOD_CTRL:
                icon_fill()

            elif event.key == p.K_n and p.key.get_mods() & p.KMOD_CTRL:
                icon_noise()

            elif event.key == p.K_b and p.key.get_mods() & p.KMOD_CTRL:
                icon_border()

            elif event.key == p.K_i and p.key.get_mods() & p.KMOD_CTRL:
                icon_invert()

            elif event.key == p.K_a and p.key.get_mods() & p.KMOD_CTRL: # import/load data matrix
                print("add")
                my_icon_matrix = matrix_txt # data / prg. include arr / bottom signature?
                matrix_icon(False)

            elif event.key == p.K_d and p.key.get_mods() & p.KMOD_CTRL: # load txt data matrix
                my_icon_matrix = matrix_text_load(text_import_d) # data / file param
                matrix_icon(False)

            elif event.key == p.K_g and p.key.get_mods() & p.KMOD_CTRL: # load txt data matrix
                my_icon_matrix = matrix_text_load(text_import_g) # graphics / octopus
                matrix_icon(True)

            elif event.key == p.K_q and p.key.get_mods() & p.KMOD_CTRL:
                running = False
   
            elif event.key == p.K_RETURN:
                # after Enter
                draw_status(f"input text: {input_text}")
                if len(input_text) > 1:
                    new_file = f"{path}{input_text}_{icon_w}.bmp"
                    draw_status2(new_file)
                    image_path = new_file
                    matrix_path = rename_matrix_path(input_text)
                    print(matrix_path)
                input_text = ""
            elif event.key == p.K_BACKSPACE:
                # del last char
                input_text = input_text[:-1]
            else:
                # add char
                input_text += event.unicode

    draw_edit_icon()

# ----- finish -----
p.quit()
