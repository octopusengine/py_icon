import pygame
import numpy as np
import random

__version__ = "0.0.2" # 2023/05


# pixel in editor 
PIXEL_SIZE = 10
x0, y0 = 30, 30
icon_w, icon_h = 16, 16 #  32, 32 / 16, 16
#image_path = f"data_img/icon{icon_w}.bmp"
image_path = f"data_img/border1.bmp"
matrix_path = f"data_img/matrix{icon_w}.txt"

my_icon_matrix_load = []
my_icon_matrix = [
    "1000100110001001",
    "0100010011000100",
    "0010001100110001",
    "0001001001100010",
]

pygame.init()

# Velikost okna
#window_width, window_height = 16 * PIXEL_SIZE, 16 * PIXEL_SIZE
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))
window.fill((0, 0, 0))

# Inicializace prázdné ikony
icon_data = np.zeros((icon_w, icon_h), dtype=bool)


# font = pygame.font.SysFont(None, 24)
font = pygame.font.SysFont("Arial", 20)
fstep = 23
text_x = icon_w * PIXEL_SIZE + x0 + PIXEL_SIZE * 2

# Funkce pro vykreslení textu
def draw_text(text, x, y):
    text_surface = font.render(text, True, (0, 128, 0))
    window.blit(text_surface, (x, y))


def draw_status(text, x=30, y=450):
    pygame.draw.rect(window, (10, 10, 10), (x-5, y-5, 600, 29))
    text_surface = font.render(str(text), True, (0, 128, 0))
    window.blit(text_surface, (x, y))
    pygame.display.flip()


def draw_edit_icon():
    # window.fill((255, 255, 255))  # Vymazání obsahu okna
    
    for y in range(icon_w):
        for x in range(icon_h):
            if icon_data[x][15-y]:
                pygame.draw.rect(window, (0, 0, 0), (x0 + x * PIXEL_SIZE, y0 + y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            else:
                pygame.draw.rect(window, (255, 255, 255), (x0 + x * PIXEL_SIZE, y0 + y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))


    pygame.draw.rect(window, (0, 128, 255), (x0, y0, icon_w * PIXEL_SIZE, icon_h * PIXEL_SIZE), 2)
    draw_text("C - Clear",text_x, y0)
    draw_text("F - Fill", text_x, y0+fstep*1)
    draw_text("I - Invert",text_x, y0+fstep*2)
    draw_text("N - Noise",text_x, y0+fstep*3)
    draw_text("D - Data", text_x, y0+fstep*5)
    draw_text("M - Matrix",text_x, y0+fstep*6)
    draw_text("L - Load", text_x, y0+fstep*7)
    draw_text("S - Save", text_x, y0+fstep*8)
    draw_text("Q - Quit", text_x, y0+fstep*9)

    icon_saved = pygame.image.load(image_path)
    window.blit(icon_saved, (text_x, y0+fstep*12))

    pygame.display.flip()


def load_icon():
    icon_surface = pygame.image.load(image_path)
    #  icon_surface = pygame.transform.flip(icon_surface, False, True)  # Horizontální převrácení (pro správnou orientaci)

    # Konverze ikony na pole dat
    icon_array = pygame.surfarray.array2d(icon_surface)
    icon_array = np.asarray(icon_array, dtype=np.uint8)

    # Nastavení hodnot v ikoně editoru na základě pole dat
    for y in range(icon_w):
        for x in range(icon_h):
            icon_data[x][15-y] = True if icon_array[x][y] < 128 else False

    print("Ikona byla úspěšně načtena ze souboru.")


def save_icon():
    # Vytvoření prázdného pole pro ikonu
    icon_array = np.zeros((icon_w, icon_h), dtype=np.uint8)

    # Nastavení hodnot v poli ikony na základě dat v ikoně editoru
    for y in range(icon_w):
        for x in range(icon_h):
            icon_array[x][y] = 0 if icon_data[x][15-y] else 255  # Horizontální převrácení

    # Vytvoření povrchu ikony a otáčení o 180 stupňů (hlavou dolu)
    icon_surface = pygame.surfarray.make_surface(icon_array)
    #icon_surface = pygame.transform.flip(icon_surface, False, True)

    # Uložení ikony do souboru
    pygame.image.save(icon_surface, image_path)
    print(f"Ikona byla úspěšně uložena do souboru {image_path}.")


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
    # Načtení ikony ze souboru
    icon_surface = pygame.image.load(image_path)

    # Převod ikony na pole dat
    icon_array = pygame.surfarray.array2d(icon_surface)
    icon_array = np.asarray(icon_array, dtype=np.uint8)
    

    # Procházení řádků a sloupců ikony
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
            if event.button == 1:  # Levé tlačítko myši
                # Získání souřadnic kliknutí
                mouse_x, mouse_y = event.pos

                # Převod souřadnic na pozici pixelu v matici
                pixel_x = (mouse_x - x0) // PIXEL_SIZE 
                pixel_y = (mouse_y - y0) // PIXEL_SIZE
                draw_status(f"x:{pixel_x} | y:{pixel_y} > 1")

                try:
                    icon_data[pixel_x][15-pixel_y] = True
                except:
                    print("mimo")    
                draw_edit_icon()

            elif event.button == 3:  # Pravé tlačítko myši
                # Získání souřadnic kliknutí
                mouse_x, mouse_y = event.pos

                # Převod souřadnic na pozici pixelu v matici
                pixel_x = (mouse_x - x0) // PIXEL_SIZE 
                pixel_y = (mouse_y - y0) // PIXEL_SIZE
                draw_status(f"x:{pixel_x} | y:{pixel_y} > 0")

                try:
                    icon_data[pixel_x][15-pixel_y] = False
                except:
                    print("mimo")
                draw_edit_icon()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                load_icon()
            elif event.key == pygame.K_s:
                save_icon()
            elif event.key == pygame.K_c:
                clear_icon()
            elif event.key == pygame.K_d: # create save data matrix
                data_icon()               
            elif event.key == pygame.K_f:
                fill_icon()
            elif event.key == pygame.K_n:
                noise_icon()
            elif event.key == pygame.K_i:
                invert_icon()
            elif event.key == pygame.K_m: # import/load data matrix
                matrix_icon()
            elif event.key == pygame.K_q:
                running = False

    draw_edit_icon()

# ----- finish -----
pygame.quit()
