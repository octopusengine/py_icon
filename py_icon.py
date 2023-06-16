#!/usr/bin/env python
"""
https://github.com/octopusengine/py_icon
"""
import os
import pygame
import numpy as np
import random
from datetime import datetime

__version__ = "0.1.5" # 2023/06

DEBUG = True
fdatetime = True # False
icon_w, icon_h = 32, 32 #  32,32 / 16,16 / 16,32
path = "data_img/"
image_path = f"{path}test_{icon_w}.bmp"
matrix_path = f"{path}matrix{icon_w}.txt"
text_import = f"{path}octopus.txt"

# Size of pixels in the editor
PIXEL_SIZE = 10
WHITE = (255, 255, 255)
SILVER = (64, 64, 64)
SILVER2 = (128, 128, 128)
BLACK = (8, 8, 8)
BLACK2 = (0, 0, 0)
COLOR = (0, 128, 0)
COLOR2 = (0, 196, 0)

x0, y0 = 30, 50
window_width, window_height = 720, 480
#if icon_w > 31:
#    window_width = 720

xc = window_width/2
ic = (icon_w * PIXEL_SIZE + x0) // 2
fstep = 23
resize = 3
input_text = ""
mode = 1
my_icon_matrix_load = []

# test matrix
my_icon_matrix = [
"10000000000000010000000000000001",
"01000000000000010000000000000010",
"00100000000000010000000000000100",
"00010000000000010000000000001000",
"00001000000000010000000000010000",
]
# ...


pygame.init()

# Window size
# window_width, window_height = 16 * PIXEL_SIZE, 16 * PIXEL_SIZE
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(f"py_icon (ver. {__version__})")
window.fill((0, 0, 0))

# Initialize an empty icon
icon_data = np.zeros((icon_w, icon_h), dtype=bool)
 
font_size = 18
font = pygame.font.SysFont("Arial", font_size)
#font = pygame.font.SysFont(None, font_size)

def draw_text(text, x, y, col = COLOR): # Function to draw label/text
    text_surface = font.render(text, True, col)
    window.blit(text_surface, (x, y))


def draw_status(text, x=30, y=390):
    pygame.draw.rect(window, (10, 10, 10), (x-5, y-5, xc-50, 29))
    text_surface = font.render(str(text), True, COLOR2)
    window.blit(text_surface, (x, y))
    pygame.display.flip()


def draw_status2(text, x=xc, y=390):
    pygame.draw.rect(window, (10, 10, 10), (x-5, y-5, xc-50, 29))
    text_surface = font.render(str(text), True, COLOR2)
    window.blit(text_surface, (x, y))
    pygame.display.flip()


def draw_input_field():
    draw_text("New filename:",xc, y0+fstep*11, COLOR2)
    pygame.draw.rect(window, SILVER, (xc, y0+fstep*12, 170, 27))
    pygame.draw.rect(window, BLACK, (xc, y0+fstep*12, 170, 27), 2)
    text_surface = font.render(input_text, True, BLACK)
    window.blit(text_surface, (xc+5, y0+fstep*12+3))


def draw_edit_icon():
    pygame.draw.rect(window, BLACK2, (0, 0, window_width, 390))
    draw_text(f"icon {icon_w}x{icon_h}",x0, y0 -30, SILVER2)
    # window.fill((255, 255, 255))  # Clear the window content
    
    for y in range(icon_h):
        for x in range(icon_w):
            if icon_data[x][y]: # 15-y ???
                pygame.draw.rect(window, (0, 0, 0), (x0 + x * PIXEL_SIZE, y0 + y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            else:
                pygame.draw.rect(window, (255, 255, 255), (x0 + x * PIXEL_SIZE, y0 + y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    pygame.draw.rect(window, (0, 128, 255), (x0, y0, icon_w * PIXEL_SIZE, icon_h * PIXEL_SIZE), 2)


    rect_width, rect_height = 180, 320
    xc2 = xc + 35
    pygame.draw.rect(window, BLACK2, (xc-5, y0, rect_width, rect_height))
    draw_text("CTRL + command:",xc, y0, COLOR2)
    
    draw_text("C/F",xc, y0+fstep*1, COLOR2)
    draw_text("Clear / Fill",xc2, y0+fstep*1)
    draw_text("R", xc, y0+fstep*2, COLOR2)
    draw_text("Resize 16/32", xc2, y0+fstep*2)
    draw_text("I",xc, y0+fstep*3, COLOR2)
    draw_text("Invert",xc2, y0+fstep*3)
    draw_text("N/B",xc, y0+fstep*4, COLOR2)
    draw_text("Noise / Border",xc2, y0+fstep*4)
    draw_text("Z/X",xc, y0+fstep*5, COLOR2)
    draw_text("Resize prew.",xc2, y0+fstep*5)
    draw_text("T/M",xc, y0+fstep*6, COLOR2)
    draw_text("Matrix (txt/add)",xc2, y0+fstep*6)
    draw_text("E", xc, y0+fstep*7, COLOR2)
    draw_text("Export (matrix)", xc2, y0+fstep*7)
    draw_text("L/S", xc, y0+fstep*8, COLOR2)
    draw_text("Load / Save", xc2, y0+fstep*8)
    draw_text("Q", xc, y0+fstep*9, COLOR2)
    draw_text("Quit", xc2, y0+fstep*9)

    draw_text(f"T M S E / ...",x0, window_height-35, SILVER2)

    rect_width = 150
    pygame.draw.rect(window, SILVER, (window_width-rect_width-x0, y0, rect_width, rect_height))
    pygame.draw.rect(window, WHITE, (window_width-rect_width-x0, y0, rect_width, 90))
    pygame.draw.rect(window, BLACK, (window_width-rect_width-x0+75, y0, rect_width/2, 90))
    try:
        icon_saved = pygame.image.load(image_path)
        original_width, original_height = icon_saved.get_size()
        current_width, current_height = original_width * resize, original_height * resize
        window.blit(icon_saved, (window_width-rect_width, y0+x0))
        window.blit(icon_saved, (window_width-rect_width+60, y0+x0))
        window.blit(pygame.transform.scale(icon_saved, (current_width, current_height)), (window_width-rect_width-10, y0+fstep*5))
    except:
        draw_status(f"Err. {image_path}")

    draw_input_field()

    pygame.display.flip()


def icon_mode(mode,icon_w,icon_h):
    mode += 1
    if mode > 2: 
        mode = 1
    
    if mode == 2: icon_w, icon_h = 16,16
    if mode == 1: icon_w, icon_h = 32,32
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
        # icon_surface = pygame.image.load(image_path) #ok
        icon_surface = pygame.image.load(image_path).convert_alpha()
        #  icon_surface = pygame.transform.flip(icon_surface, False, True)  # Horizontal flip (for correct orientation)

        # Convert the icon to a data array
        #icon_array = pygame.surfarray.array2d(icon_surface)
        icon_array = pygame.surfarray.pixels2d(icon_surface)
        icon_array = np.asarray(icon_array, dtype=np.uint8)

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
    # Create an empty array for the icon
    icon_array = np.zeros((icon_w, icon_h), dtype=np.uint8)

    # Set the values in the icon array based on the data in the editor icon
    for y in range(icon_h):
        for x in range(icon_w):
            icon_array[x][y] = 0 if icon_data[x][y] else 255

    # Create a surface for the icon and rotate it 180 degrees (upside down)
    icon_surface = pygame.surfarray.make_surface(icon_array)
    #icon_surface = pygame.transform.flip(icon_surface, False, True)

    # Save the icon to a file
    pygame.image.save(icon_surface, image_path)
    print(f"The icon was successfully saved to the file {image_path}.")


def icon_clear():
    draw_status(f"clear > 0")
    icon_data.fill(False)


def icon_fill():
    draw_status(f"fill > 1")
    for y in range(icon_w):
        for x in range(icon_h):
            icon_data[x][y] = True


def icon_invert():
    draw_status(f"invert 0<->1")
    for y in range(icon_w):
        for x in range(icon_h):
            icon_data[x][y] ^= True


def icon_noise():
    draw_status(f"noise")
    for y in range(icon_w):
        for x in range(icon_h):
            icon_data[x][y] = random.randint(0, 1) # True


def icon_border():
    draw_status(f"border")
    for y in range(icon_h): # L vert.
        icon_data[0][y] = 1
        icon_data[icon_w-1][y] = 1

    for x in range(icon_w):
        icon_data[x][0] = 1
        icon_data[x][icon_h-1] = 1


def text_matrix_load(text_file=text_import): # icon or pattern/noise
    my_txt_matrix = []
    draw_status(f"text_matrix_load")
    draw_status2(text_file)
    with open(text_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            cleaned_line = line.strip()
            #str_hex = bin_to_hex(str(cleaned_line),True,8)
            my_txt_matrix.append(cleaned_line)
    return my_txt_matrix

            
def matrix_icon():
    try:
        for y, row in enumerate(my_icon_matrix):
            for x, value in enumerate(row):
                icon_data[x][y] = True if value == '1' else False
    except:
        print("Err. Matrix")


def data_icon():
    draw_status(f"create and save binary data matrix")
    # Load the icon from a file
    icon_surface = pygame.image.load(image_path)

    # Convert the icon to a data array
    icon_array = pygame.surfarray.array2d(icon_surface)
    icon_array = np.asarray(icon_array, dtype=np.uint8)
    

    # Iterate over rows and columns of the icon
    for y in range(icon_array.shape[1]):
        row = ""
        for x in range(icon_array.shape[0]):
            value = icon_array[x][y]
            if value < 128:
                row += "1"
            else:
                row += "0"
        my_icon_matrix_load.append(row)
        print(row)

    if fdatetime:
        dt = datetime.now().strftime("%Y%m%d_%H%M%S")
        matrix_path = f"{path}matrix{icon_w}-{dt}.txt" 
    draw_status2(matrix_path)       

    with open(matrix_path, "w") as file:
        for row in my_icon_matrix_load:
            file.write(row + "\n")


# =================== main loop ===============================
running = True
draw_status(f"Start > {image_path}")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get the click coordinates
                mouse_x, mouse_y = event.pos

                # Convert the coordinates to pixel position in the matrix
                pixel_x = (mouse_x - x0) // PIXEL_SIZE 
                pixel_y = (mouse_y - y0) // PIXEL_SIZE
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
                pixel_x = (mouse_x - x0) // PIXEL_SIZE 
                pixel_y = (mouse_y - y0) // PIXEL_SIZE
                draw_status(f"x:{pixel_x} | y:{pixel_y} > 0")

                try:
                    icon_data[pixel_x][pixel_y] = False
                except:
                    print("out of range")
                draw_edit_icon()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                load_icon()

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_icon()
            
            elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                mode,icon_w,icon_h = icon_mode(mode,icon_w,icon_h)

            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                resize += 1
                if resize > 4: 
                    resize = 4
                draw_status2(f"zoom {resize}")

            elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL:
                resize -= 1
                if resize == 0: 
                    resize = 1
                draw_status2(f"zoom {resize}")

            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                icon_clear()

            elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_CTRL: # create save data matrix
                data_icon()

            elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_CTRL:
                icon_fill()

            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
                icon_noise()

            elif event.key == pygame.K_b and pygame.key.get_mods() & pygame.KMOD_CTRL:
                icon_border()

            elif event.key == pygame.K_i and pygame.key.get_mods() & pygame.KMOD_CTRL:
                icon_invert()

            elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL: # import/load data matrix
                matrix_icon()

            elif event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_CTRL: # load txt data matrix
                my_icon_matrix = text_matrix_load() # octopus / file param

            elif event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                running = False
   
            elif event.key == pygame.K_RETURN:
                # after Enter
                draw_status(f"input text: {input_text}")
                if len(input_text)>2:
                    new_file = f"{path}{input_text}_{icon_w}.bmp"
                    draw_status2(new_file)
                    image_path = new_file
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                # del last char
                input_text = input_text[:-1]
            else:
                # add char
                input_text += event.unicode

    draw_edit_icon()

# ----- finish -----
pygame.quit()
