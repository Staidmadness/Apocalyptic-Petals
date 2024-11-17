import pygame
import subprocess
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Color library
red = (227, 118, 118)
green = (124, 168, 88)
blue = (169, 207, 212)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (242, 207, 109)

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Apocalyptic Petals')
background = pygame.image.load("apoc-pixel.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
healthyFlower = pygame.image.load('Healthy.png')
healthyFlower = pygame.Surface.convert_alpha(healthyFlower)
healthyFlower = pygame.transform.scale(healthyFlower, (300, 400))
strongFlower = pygame.image.load('Strong.png')
strongFlower = pygame.Surface.convert_alpha(strongFlower)
strongFlower = pygame.transform.scale(strongFlower, (300, 400))
witheredFlower = pygame.image.load('withered.png')
witheredFlower = pygame.Surface.convert_alpha(witheredFlower)
witheredFlower = pygame.transform.scale(witheredFlower, (300, 400))
overwaterFlower = pygame.image.load('overWater.png')
overwaterFlower = pygame.Surface.convert_alpha(overwaterFlower)
overwaterFlower = pygame.transform.scale(overwaterFlower, (300, 500))
waterimg = pygame.image.load('water.png')
waterimg = pygame.Surface.convert_alpha(waterimg)
waterimg = pygame.transform.scale(waterimg, (100, 100))
sunimg = pygame.image.load('sun.png')
sunimg = pygame.Surface.convert_alpha(sunimg)
sunimg = pygame.transform.scale(sunimg, (100, 100))
loveimg = pygame.image.load('love.png')
loveimg = pygame.Surface.convert_alpha(loveimg)
loveimg = pygame.transform.scale(loveimg, (100, 100))
titleimg = pygame.image.load('title.png')
titleimg = pygame.Surface.convert_alpha(titleimg)
titleimg = pygame.transform.scale(titleimg, (400, 200))
burning = pygame.image.load('burning.png')
burning = pygame.Surface.convert_alpha(burning)
burning = pygame.transform.scale(burning, (300, 500))
ohshit = pygame.image.load('ohShit.png')
ohshit = pygame.Surface.convert_alpha(ohshit)
ohshit = pygame.transform.scale(ohshit, (300, 500))

framerate = 60
font = pygame.font.Font('FreeSansBold.ttf', 16)
timer = pygame.time.Clock()

# Game variables
draw_water = False
draw_love = False
draw_light = False
length_water = 100
length_love = 100
length_light = 100
rank = 1
food = 2  # Initial food count

# Plant class
class Plant:
    def __init__(self):
        self.cooldown = 5000
        self.last_water = pygame.time.get_ticks()
        self.last_love = pygame.time.get_ticks()
        self.last_light = pygame.time.get_ticks()

    def lose_life(self, length, last_timer, decrease_rate):
        now = pygame.time.get_ticks()
        if now - last_timer >= self.cooldown:
            last_timer = now
            length -= decrease_rate
        return length, last_timer

    def gain_life(self, length, last_timer):
        now = pygame.time.get_ticks()
        if now - last_timer >= self.cooldown:
            last_timer = now
            length += 1
        return length, last_timer

    def draw_task(self, color, y_coord, draw, length):
        if draw and length < 200:
            length += 2
            draw = False  # Reset draw flag
        task = pygame.draw.circle(screen, color, (30, y_coord), 20, 0)
        pygame.draw.rect(screen, color, [70, y_coord - 15, 200, 30])
        pygame.draw.rect(screen, black, [75, y_coord - 10, 190, 20])
        pygame.draw.rect(screen, color, [70, y_coord - 15, length, 30])
        return task, length, draw

    def check_danger(self, lengths):
        danger_bars = [bar for bar in lengths if bar > 160]

        if len(danger_bars) == len(lengths):
            return "all"
        elif len(danger_bars) >= 1:
            return "partial"
        return False

    def use_food(self, lengths):
        global food
        if food > 0:
            for i in range(len(lengths)):
                if lengths[i] > 160:  # If a bar is in the danger zone
                    lengths[i] = 150  # Reduce it to below the danger threshold
                    food -= 1  # Consume food
                    break  # Exit after fixing one bar
        return lengths

    def death(self, length):
        if length == 0 or length == 200:
            print("Game Over")
            pygame.quit()


def update_rank(lengths):
    global rank
    lowest_length = min(lengths)

    if any(length > 160 for length in lengths):
        rank = "Danger"  # At least one bar is in the danger zone
    elif lowest_length <= 60:
        rank = 1  # Withered
    elif lowest_length <= 120:
        rank = 2  # Healthy
    elif lowest_length <= 160:
        rank = 3  # Strong

plants = Plant()

# Screen states
MAIN_MENU = 0
GAME_SCREEN = 1
THIRD_SCREEN = 2
current_screen = MAIN_MENU

# Main game loop
run = True
while run:
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == MAIN_MENU:
                if play_button.collidepoint(event.pos):
                    current_screen = GAME_SCREEN
            elif current_screen == GAME_SCREEN:
                if third_screen_button.collidepoint(event.pos):
                    subprocess.Popen(["python", "hackathon_connect_4.py"])
                    food += 1
                if task1 and task1.collidepoint(event.pos):
                    draw_water = True
                if task2 and task2.collidepoint(event.pos):
                    draw_love = True
                if task3 and task3.collidepoint(event.pos):
                    draw_light = True
                if food_button and food_button.collidepoint(event.pos):
                    lengths = [length_water, length_love, length_light]
                    lengths = plants.use_food(lengths)
                    length_water, length_love, length_light = lengths

    screen.fill(black)

    if current_screen == MAIN_MENU:
        screen.blit(background,(0,0))
        play_button = pygame.draw.rect(screen, blue, [300, 250, 200, 100])
        play_text = font.render("Play Game", True, black)
        screen.blit(titleimg, (205,0))
        screen.blit(play_text, (365, 285))

    elif current_screen == GAME_SCREEN:
        screen.blit(background, (0, 0))
        task1, length_water, draw_water = plants.draw_task(blue, 50, draw_water, length_water)
        task2, length_love, draw_love = plants.draw_task(red, 110, draw_love, length_love)
        task3, length_light, draw_light = plants.draw_task(yellow, 170, draw_light, length_light)
        screen.blit(waterimg,(-20,5))
        screen.blit(loveimg,(-20,50))
        screen.blit(sunimg,(-20,130))

        food_button = pygame.draw.rect(screen, green, [300, 500, 200, 50])
        food_text = font.render('Use Food', True, black)
        screen.blit(food_text, (375, 515))

        third_screen_button = pygame.draw.rect(screen, white, [10, 550, 200, 30])
        third_screen_text = font.render("Go to Third Screen", True, black)
        screen.blit(third_screen_text, (15, 555))

        danger_mode = plants.check_danger([length_water, length_light])

        if danger_mode == "all":
            length_water, plants.last_water = plants.gain_life(length_water, plants.last_water)
            length_light, plants.last_light = plants.gain_life(length_light, plants.last_light)
        elif danger_mode == "partial":
            if length_water > 160:
                length_water, plants.last_water = plants.gain_life(length_water, plants.last_water)
            else:
                length_water, plants.last_water = plants.lose_life(length_water, plants.last_water, 3)
            if length_love > 160:
                length_love, plants.last_love = plants.lose_life(length_love, plants.last_love, 6)
                length_water, plants.last_water = plants.lose_life(length_water, plants.last_water, 1)
                length_light, plants.last_light = plants.lose_life(length_light, plants.last_light, 1)
            else:
                length_love, plants.last_love = plants.lose_life(length_love, plants.last_love, 6)
            if length_light > 160:
                length_light, plants.last_light = plants.gain_life(length_light, plants.last_light)
            else:
                length_light, plants.last_light = plants.lose_life(length_light, plants.last_light, 3)
        else:
            length_water, plants.last_water = plants.lose_life(length_water, plants.last_water, 3)
            length_love, plants.last_love = plants.lose_life(length_love, plants.last_love, 6)
            length_light, plants.last_light = plants.lose_life(length_light, plants.last_light, 3)

        plants.death(length_light)
        plants.death(length_love)
        plants.death(length_water)
        update_rank([length_water, length_light])

        if rank == 1:
            screen.blit(witheredFlower, (450,50))
        elif rank == 2:
            screen.blit(healthyFlower, (450, 50))
        elif rank == 3:
            screen.blit(strongFlower, (450, 50))
        elif rank == "Danger":
            if length_water >= 160 and length_light >=160:
                screen.blit(ohshit,(450,50))
            elif length_water >= 160:
                screen.blit(overwaterFlower, (450,50))
            elif length_light >= 160:
                screen.blit(burning, (450, 50))
            

        display_rank = font.render('Rank: ' + str(rank), True, white, black)
        screen.blit(display_rank, (400, 5))

        food_display = font.render('Food: ' + str(food), True, white, black)
        screen.blit(food_display, (600, 5))

    elif current_screen == THIRD_SCREEN:
        screen.fill(red)
        third_text = font.render("This is the third screen!", True, black)
        screen.blit(third_text, (300, 250))
        

    pygame.display.flip()

pygame.quit()
