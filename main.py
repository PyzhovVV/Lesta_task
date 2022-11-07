import pygame
import numpy as np
import random as rn

white = (255, 255, 255)
gray = (130, 130, 130)
black = (0, 0, 0)
pygame.init()
n = 5  # размерность поля (в клетках)
width = 50  # ширина клетки( и объекта)
height = 50  # высота клетки ( и объекта)
margin = 5  # промежуток между клетками
green_circle = pygame.image.load('images/green.jpg')
red_circle = pygame.image.load('images/red.jpg')
yellow_circle = pygame.image.load('images/yellow.jpg')

pygame.init()
screen = pygame.display.set_mode(((width + margin) * n + margin, (height + margin) * (n + 1) + margin))
pygame.display.set_caption('Lesta task')


def creating_playing_field():
    list_of_chips = [1, ] * 5 + [2, ] * 5 + [3, ] * 5   # список из фишек всех цветов (по 5 штук)
    grid = np.zeros((n + 1, n), dtype=int)
    grid[0] = [1, -2, 2, -2, 3]  # верхнее поле
    for row in range(1, n + 1):
        for column in range(n):
            if row % 2 == 1 and column % 2 == 1:  # заблокированные ячейки
                grid[row][column] = -1
            elif row % 2 == 0 and column % 2 == 1:  # пустые ячейки
                grid[row][column] = 0
            else:
                grid[row][column] = list_of_chips.pop(rn.randint(0, len(list_of_chips) - 1))  # ячейки с фишками
    field_filling(grid)
    return grid


def field_filling(grid):
    for row in range(n + 1):
        for column in range(n):
            x = width * column + (column + 1) * margin  # определение координат для клеток
            y = height * row + (row + 1) * margin  # определение координат для клеток
            match grid[row][column]:
                case -2:
                    pygame.draw.rect(screen, black, (x, y, width, height))
                case -1:
                    pygame.draw.rect(screen, gray, (x, y, width, height))  # прорисовка заблокированных клеток
                case 0:
                    pygame.draw.rect(screen, white, (x, y, width, height))  # прорисовка активных клеток
                case 1:
                    pygame.draw.rect(screen, white, (x, y, width, height))  # прорисовка зеленых фишек
                    screen.blit(green_circle, (x, y))
                case 2:
                    pygame.draw.rect(screen, white, (x, y, width, height))  # прорисовка красных фишек
                    screen.blit(red_circle, (x, y))
                case 3:
                    pygame.draw.rect(screen, white, (x, y, width, height))  # прорисовка желтых фишек
                    screen.blit(yellow_circle, (x, y))



def find_coordinates():  # нахождение координат нажатой клетки
    x_mouse, y_mouse = pygame.mouse.get_pos()  # считывание координат курсора
    column = x_mouse // (width + margin)  # перевод координат в номер столбца
    row = y_mouse // (height + margin)  # перевод координат в номер строки
    if row == 0:
        return None, None
    return row, column


def get_move(grid, row_start, column_start, row_end, column_end):  # это выглядит слишком длинно, я знаю
    if (row_start, column_start) != (row_end, column_end) and None not in (row_start, column_start, row_end, column_end):  # проверка что мы двигаем на играбельную область
        if grid[row_start][column_start] in [1, 2, 3] and grid[row_end][column_end] == 0:  # еще одна проверка что мы взяли именно фишку и передвигаем ее в свообдное место
            if abs(row_start - row_end) + abs(column_start - column_end) == 1:  # супер последняя проверка на то что перемещение происходит на соседнюю клетку
                grid[row_start][column_start], grid[row_end][column_end] = grid[row_end][column_end], grid[row_start][column_start]
                field_filling(grid)


def check_winning(grid):  # проверка, собраны ли линии одноо цвета
    first_column = [grid[i][0] for i in range(1, n + 1)]
    third_column = [grid[i][2] for i in range(1, n + 1)]
    fifth_column = [grid[i][4] for i in range(1, n + 1)]
    if first_column.count(1) == third_column.count(2) == fifth_column.count(3) == 5:
        return True
    return False

grid = creating_playing_field()
running = True
game_over = False
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:  # ситуация нажатия на клетку
            row_start, column_start = find_coordinates()
        elif event.type == pygame.MOUSEBUTTONUP and not game_over:  # ситуация нажатия на клетку
            row_end, column_end = find_coordinates()
            print(row_start, column_start, row_end, column_end)
            if max(column_start, column_end) < 5 and max(row_start, row_end) < 6:
                get_move(grid, row_start, column_start, row_end, column_end)
            game_over = check_winning(grid)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # перезапуск игры нажатием пробела
            screen.fill(black)
            game_over = False
            grid = creating_playing_field()
        if game_over:
            screen.fill(black)
            font = pygame.font.SysFont('stxingkai', 60)
            text1 = font.render("Ты виграл", True, white)
            text_rect = text1.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2  # нахождения геометрического центра
            text_y = screen.get_height() / 2 - text_rect.height / 2  # нахождения геометрического центра
            screen.blit(text1, [text_x, text_y])
        pygame.display.update()
