#!/usr/bin/env python
"""
https://github.com/octopusengine/py_icon
"""
import pygame
import numpy as np
import random

__version__ = "0.0.3" # 2023/05


# Size of pixels in the editor
PIXEL_SIZE = 10
WHITE = (255, 255, 255)
SILVER = (128, 128, 128)
BLACK = (0, 0, 0)

x0, y0 = 30, 30
icon_w, icon_h = 16, 16 #  32, 32 / 16, 16
#image_path = f"data_img/icon{icon_w}.bmp"
image_path = f"data_img/border1.bmp"
matrix_path = f"data_img/matrix{icon_w}.txt"

my_icon_matrix_load = []

# test matrix
my_icon_matrix = [
    "1000100110001001",
    "0100010011000100",
    "0010001100110001",
    "0001001001100010",
]


pygame.init()

# Window size
#window_width, window_height = 16 * PIXEL_SIZE, 16 * PIXEL_SIZE
window_width, window_height = 640, 480
resize = 2
window = pygame.display.set_mode((window_width, window_height))
window.fill((0, 0, 0))

# Initialize an empty icon
icon_data = np.zeros((icon_w, icon_h), dtype=bool)

# font = pygame.font.SysFont(None, 24)
font_size = 20
font = pygame.font.SysFont("Arial", font_size)
fstep = 23
text_x = icon_w * PIXEL_SIZE + x0 + PIXEL_SIZE * 2

def draw_text(text, x, y): # Function to draw label/text
    text_surface = font.render(text, True, (0, 128, 0))
    window.blit(text_surface, (x, y))


def draw_status(text, x=30, y=450):
    pygame.draw.rect(window, (10, 10, 10), (x-5, y-5, 600, 29))
    text_surface = font.render(str(text), True, (0, 128, 0))
    window.blit(text_surface, (x, y))
    pygame.display.flip()


input_text = ""

def draw_input_field():
    pygame.draw.rect(window, SILVER, (text_x, y0+fstep*15, 200, 25))
    pygame.draw.rect(window, BLACK, (text_x, y0+fstep*15, 200, 25), 2)
    text_surface = font.render(input_text, True, BLACK)
    window.blit(text_surface, (text_x+5, y0+fstep*15+3))


def draw_edit_icon():
    # window.fill((255, 255, 255))  # Clear the window content
    
    for y in range(icon_w):
        for x in range(icon_h):
            if icon_data[x][15-y]:
                pygame.draw.rect(window, (0, 0, 0), (x0 + x * PIXEL_SIZE, y0 + y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            else:
                pygame.draw.rect(window, (255, 255, 255), (x0 + x * PIXEL_SIZE, y0 + y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))


    pygame.draw.rect(window, (0, 128, 255), (x0, y0, icon_w * PIXEL_SIZE, icon_h * PIXEL_SIZE), 2)
    draw_text("CTRL+C  -  Clear",text_x, y0)
    draw_text("CTRL+F  -  Fill", text_x, y0+fstep*1)
    draw_text("CTRL+I  -  Invert",text_x, y0+fstep*2)
    draw_text("CTRL+N  -  Noise",text_x, y0+fstep*3)
    draw_text("CTRL+Z/X - Resize prew.",text_x, y0+fstep*4)
    draw_text("CTRL+D  -  Data", text_x, y0+fstep*5)
    draw_text("CTRL+M  -  Matrix",text_x, y0+fstep*6)
    draw_text("CTRL+L  -  Load", text_x, y0+fstep*7)
    draw_text("CTRL+S  -  Save", text_x, y0+fstep*8)
    draw_text("CTRL+Q  -  Quit", text_x, y0+fstep*9)

    icon_saved = pygame.image.load(image_path)
    original_width, original_height = icon_saved.get_size()
    current_width, current_height = original_width * resize, original_height * resize
    window.blit(icon_saved, (text_x, y0+fstep*12))
    window.blit(pygame.transform.scale(icon_saved, (current_width, current_height)), (text_x + 50, y0+fstep*12))

    draw_input_field()

    pygame.display.flip()


def load_icon():
    icon_surface = pygame.image.load(image_path)
    #  icon_surface = pygame.transform.flip(icon_surface, False, True)  # Horizontal flip (for correct orientation)

    # Convert the icon to a data array
    icon_array = pygame.surfarray.array2d(icon_surface)
    icon_array = np.asarray(icon_array, dtype=np.uint8)

    # Set the values in the editor icon based on the data array
    for y in range(icon_w):
        for x in range(icon_h):
            icon_data[x][15-y] = True if icon_array[x][y] < 128 else False

    print("The icon was successfully loaded from the file.")


def save_icon():
    # Create an empty array for the icon
    icon_array = np.zeros((icon_w, icon_h), dtype=np.uint8)

    # Set the values in the icon array based on the data in the editor icon
    for y in range(icon_w):
        for x in range(icon_h):
            icon_array[x][y] = 0 if icon_data[x][15-y] else 255  # Horizontal flip

    # Create a surface for the icon and rotate it 180 degrees (upside down)
    icon_surface = pygame.surfarray.make_surface(icon_array)
    #icon_surface = pygame.transform.flip(icon_surface, False, True)

    # Save the icon to a file
    pygame.image.save(icon_surface, image_path)
    print(f"The icon was successfully saved to the file {image_path}.")


def clear_icon():
    draw_status(f"clear > 0")
    icon_data.fill(False)


def fill_icon():
    draw_status(f"fill > 1")
    for y in range(icon_w):
        for x in range(icon_h):
            icon_data[x][y] = True


def invert_icon():
    draw_status(f"invert 0<->1")
    for y in range(icon_w):
        for x in range(icon_h):
            icon_data[x][y] ^= True


def noise_icon():
    draw_status(f"noise")
    for y in range(icon_w):
        for x in range(icon_h):
            icon_data[x][y] = random.randint(0, 1) # True


def matrix_icon():
    try:
        for y, row in enumerate(my_icon_matrix):
            for x, value in enumerate(row):
                icon_data[x][15 - y] = True if value == '1' else False
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

    with open(matrix_path, "w") as file:
        for row in my_icon_matrix_load:
            file.write(row + "\n")


# =================== main loop ===============================
running = True
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
                    icon_data[pixel_x][15-pixel_y] = True
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
                    icon_data[pixel_x][15-pixel_y] = False
                except:
                    print("out of range")
                draw_edit_icon()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                load_icon()
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_icon()
            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                resize += 1
            elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL:
                resize -= 1
            #elif event.key == pygame.K_c:
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                clear_icon()
            elif event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_CTRL: # create save data matrix
                data_icon()               
            elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_CTRL:
                fill_icon()
            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
                noise_icon()
            elif event.key == pygame.K_i and pygame.key.get_mods() & pygame.KMOD_CTRL:
                invert_icon()
            elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL: # import/load data matrix
                matrix_icon()
            elif event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                # after Enter
                    draw_status(f"input text: {input_text}")
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
