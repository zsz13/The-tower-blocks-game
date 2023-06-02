# Импорт библиотек
import pygame
import random
import sys
import math

# Инициализация Pygame
pygame.init()

# Размер окна игры
window_width = 400
window_height = 600

# Загрузка иконки
icon = pygame.image.load("images/62637.png")
pygame.display.set_icon(icon)

# Загрузка изображения блока этажа здания
block_size = int(window_width / 10)
image_floor = pygame.image.load("images/Снимок экрана (694).png")
image_floor = pygame.transform.scale(image_floor, (block_size, block_size))

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
gray = (128, 128, 128)

# Загрузка изображения фона
background_image = pygame.image.load("images/1495616999_samye-vysokie-zdaniya-v-mire.jpg")
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Загрузка музыки
background_sound = pygame.mixer.Sound("music/ce8e6287c767e45.mp3")

# Создание окна игры
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tower Bloxx")

# Скорость падения блоков
difficulty = input("Выберите уровень сложности для запуска игры (легкий / средний / сложный): ")
if difficulty == "легкий":
    block_speed = 0.3
elif difficulty == "средний":
    block_speed = 1.1
elif difficulty == "сложный":
    block_speed = 1.4
else:
    print("Некорректный выбор уровня сложности. Установлен уровень по умолчанию (средний).")
    block_speed = 1.1
print('Для запуска игры в окне нажмите клавишу "space" или "пробел"')
print('Используйте клавиши для перемещения: "arrow left" или "стрела влево" для перемещения влево, "arrow right" или "стрела вправо" для перемещения вправо')
# Создание блока
def create_block():
    block_x = random.randint(0, window_width - block_size)
    block_y = -block_size
    return {'x': block_x, 'y': block_y}

# Проверка пересечения блоков
def check_collision(block1, block2):
    if block1['x'] < block2['x'] + block_size and block1['x'] + block_size > block2['x'] and \
       block1['y'] < block2['y'] + block_size and block1['y'] + block_size > block2['y']:
        return True
    return False

# Флаг завершения игры
game_over = False

# Создание платформы
platform_x = window_width // 2 - block_size // 2
platform_y = window_height - block_size

# Счет и рекорд
score = 0
high_score = 0

# Количество падений блоков
fallen_blocks = 0

# Создание первого блока
block = create_block()

# Переменные для падения блока с маятника
swing_x = window_width // 2
swing_y = 0
swing_length = window_height // 3
swing_angle = 0

# Скорость маятника
swing_speed = block_speed

# Переменная для определения падения блока с маятника
fall_from_swing = False

# Основной игровой цикл
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        # Движение платформы влево
        platform_x -= block_speed
        if platform_x < 0:
            platform_x = 0
    elif keys[pygame.K_RIGHT]:
        # Движение платформы вправо
        platform_x += block_speed
        if platform_x > window_width - block_size:
            platform_x = window_width - block_size

    if keys[pygame.K_ESCAPE]:
        game_over = True

    # Падение блока с маятника
    if fall_from_swing:
        block['y'] += block_speed
    else:
        swing_angle += swing_speed
        block['x'] = swing_x + math.sin(swing_angle) * swing_length
        block['y'] = swing_y + math.cos(swing_angle) * swing_length * 0.4

    if keys[pygame.K_SPACE]:
        # Падение блока с маятника
        fall_from_swing = True
        swing_angle = 0

    # Проверка столкновения блока с платформой
    if check_collision(block, {'x': platform_x, 'y': platform_y}):
        score += 1
        block = create_block()

    # Проверка падения блока
    if block['y'] > window_height - block_size:
        block = create_block()
        fallen_blocks += 1

    # Проверка окончания игры
    if fallen_blocks >= 3:
        if score > high_score:
            high_score = score
        score = 0
        fallen_blocks = 0

    # Отрисовка заднего фона
    window.blit(background_image, (0, 0))

    # Загрузка фоновой музыки
    background_sound.play()

    # Отрисовка маятника
    pygame.draw.line(window, gray, (swing_x, swing_y), (block['x'] + block_size // 2, block['y'] + block_size // 2), 3)
    pygame.draw.circle(window, gray, (swing_x, swing_y), 10)

    # Отрисовка игровых объектов
    window.blit(image_floor, (platform_x, platform_y))
    window.blit(image_floor, (block['x'], block['y']))

    # Отображение счета и рекорда
    font = pygame.font.Font('fonts/Lobster-Regular.ttf', 36)
    score_text = font.render("Score: " + str(score), True, white)
    high_score_text = font.render("High Score: " + str(high_score), True, white)
    window.blit(score_text, (10, 10))
    window.blit(high_score_text, (10, 50))

    pygame.display.update()

# Завершение игры
pygame.quit()
sys.exit()
