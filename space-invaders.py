import pygame
import random
from helpers_pygame import get_image, display_text

# Initialize pygame module, constants(with which you can modify the game), sprite groups and fonts
pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BOUNDARY = 500
SPEED = 65
BULLET_SPEED = 5
ENEMIES_SPEED_HORI = 2
ENEMIES_SPEED_VERTI = 0
ENEMIES_NUMBER = 15
PLAYER_SPEED = 3
FLAG = False
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)
player_bullets = pygame.sprite.RenderPlain()
enemy_bullets = pygame.sprite.RenderPlain()
enemies = pygame.sprite.RenderPlain()
players = pygame.sprite.RenderPlain()
explosions = pygame.sprite.RenderPlain()
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 64)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Player(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.frame = 0
        self.images = image_file
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    def image_swap(self):
        self.frame = (self.frame + 1) % len(self.images)
        self.image = self.images[self.frame]

class Bullet(pygame.sprite.Sprite):
    # Init bullet object, add to a sprite group depending on the shooter
    def __init__(self, image_file, location, side):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.side = side
        if self.side == "player":
            player_bullets.add(self)
        else:
            enemy_bullets.add(self)

    def update(self):
        if self.side == "player":
            self.rect.top -= BULLET_SPEED
            if self.rect.top < -30:
                self.kill()
        else:
            self.rect.top += BULLET_SPEED
            if self.rect.top > game.SCREEN_HEIGHT - 30:
                self.kill()

class Enemy(pygame.sprite.Sprite):
    # Initialize enemy sprite 
    def __init__(self, image_file1, image_file2, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.current_image = random.randint(0, 1)
        self.frame_timer = 60
        self.verti_move = 0
        self.images = (pygame.image.load(image_file1), pygame.image.load(image_file2))
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        enemies.add(self)
    # Update position and flag, swap image for animation
    def update(self):
        global FLAG
        self.rect.left += ENEMIES_SPEED_HORI
        self.verti_move += ENEMIES_SPEED_VERTI
        if self.verti_move > 1:
            self.rect.top += 1
            self.verti_move -= 1
        if self.rect.left <= 0 or self.rect.left >= game.SCREEN_WIDTH - 40:
            FLAG = True
        if self.frame_timer < pygame.time.get_ticks():
            self.image_swap()
            self.frame_timer += 500

    def shoot(self):
        Bullet("images/laser.png", [self.rect.left+18, self.rect.top+40], "enemy")

    def image_swap(self):
        if self.current_image == 1:
            self.current_image = 0
        else:
            self.current_image = 1
        self.image = self.images[self.current_image]

class Explosion(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.frame = 0
        self.images = image_file
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        explosions.add(self)
    def image_swap(self):
        self.frame = (self.frame + 1) % len(self.images)
        self.image = self.images[self.frame]
        if self.frame == 31:
            self.kill()
    def update(self):
        self.image_swap()        

class Game:
    # Initialize the games display, necesarry timers and players spreadsheet
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.display = pygame.display.set_mode(size=(self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.can_shoot = True
        self.score = 0
        self.game_over = False
        self.bg = Background("images/bg.png",[0,0])
        player_sheet = pygame.image.load("images/statek.png")
        explosion_sheet = pygame.image.load("images/explosion.png")
        # Get image is a function for getting individual images from a spritesheet
        ship_images = [get_image(player_sheet, x, 39, 39, scale=1.5) for x in range(8)]
        self.explosion_images = []
        for i in range(4):
            for j in range(8):
                self.explosion_images.append(get_image(explosion_sheet, j, 256, 251, row=i,scale=0.16)) 
        self.player = Player(ship_images, [self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT - 42])
        players.add(self.player)
        pygame.time.set_timer(pygame.USEREVENT+2, 100) # Timer for enemy shooting
        pygame.time.set_timer(pygame.USEREVENT+3, 80) # Timer for player animation
        pygame.time.set_timer(pygame.USEREVENT+4, 15) # Timer for explosion animation
        pygame.display.set_caption("Space Invaders")
    # Handle the events (players and enemies shooting, player movement)
    def next_turn(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.can_shoot:
                    Bullet("images/laser.png", [self.player.rect.left+28, self.player.rect.top-30], "player")
                    pygame.time.set_timer(pygame.USEREVENT+1, 1500, loops=1) # Timer to prevent constant player fire
                    self.can_shoot = False
            elif event.type == pygame.USEREVENT+1:
                self.can_shoot = True
            elif event.type == pygame.USEREVENT+2:
                idx = random.randint(0, len(enemies)-1)
                enemies.sprites()[idx].shoot()
            elif event.type == pygame.USEREVENT+3:
                self.player.image_swap()
                
            elif event.type == pygame.USEREVENT+4:
                explosions.update()
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]:
            self.player.rect.left -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player.rect.right += PLAYER_SPEED
        if keys[pygame.K_UP] and self.player.rect.top > BOUNDARY:
            self.player.rect.top -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.player.rect.top < self.SCREEN_HEIGHT - 40:
            self.player.rect.top += PLAYER_SPEED

# Draw everything on the screen and update the positions accordingly to intended behaviours
# Use flag to change directions of enemies if one of them touches the boundary
# Update score according to hits
    def update_ui(self):
        global FLAG
        global ENEMIES_SPEED_HORI
        self.display.blit(self.bg.image, self.bg.rect)
        players.draw(self.display)
        player_bullets.draw(self.display)
        enemy_bullets.draw(self.display)
        explosions.draw(self.display)
        enemies.draw(self.display)
        player_bullets.update()
        enemy_bullets.update()
        player_hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
        for enemy in player_hits:
            self.score += 1
            Explosion(self.explosion_images, (enemy.rect.left+(5*ENEMIES_SPEED_HORI), enemy.rect.top))
        death = pygame.sprite.groupcollide(enemy_bullets, players, True, True)
        if death:
            self.game_over = True
        enemies.update()
        display_text(self.display, "bottomleft", 0, self.SCREEN_HEIGHT, font, f"Score: {str(self.score)}", GREEN)
        if FLAG:
            ENEMIES_SPEED_HORI = -ENEMIES_SPEED_HORI
            FLAG = False
        pygame.display.flip()

game = Game()
# Populate the screen with diffrent enemies in each row
for i in range(ENEMIES_NUMBER):
    enemies.add(Enemy("images/ufolud3-1.png", "images/ufolud3-2.png", [i*50, 0]))
    enemies.add(Enemy("images/ufolud2-1.png", "images/ufolud2-2.png", [i*50, 40]))
    enemies.add(Enemy("images/ufolud1-1.png", "images/ufolud1-2.png", [i*50, 80]))

# Game loop
while not game.game_over:
    game.clock.tick(SPEED)
    game.next_turn()
    game.update_ui()

# Stop unused timers and initialize new ones to time the gameover animation
pygame.time.set_timer(pygame.USEREVENT+1, 0)
pygame.time.set_timer(pygame.USEREVENT+2, 0)
pygame.time.set_timer(pygame.USEREVENT+3, 0)
pygame.time.set_timer(pygame.USEREVENT+5, 5000)
pygame.time.set_timer(pygame.USEREVENT+4, 600, loops = 6)
# Change player images for the blinking effect
stay = game.player.images.pop()
game.player.frame = 1
game.player.images = [pygame.image.load("images/blank.png"), stay]
ENEMIES_SPEED_VERTI = 0.8
ENEMIES_SPEED_HORI = 0
over_screen = True
# Game over animation
while over_screen:
    game.display.blit(game.bg.image, game.bg.rect)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.USEREVENT+5:
                over_screen = False
            elif event.type == pygame.USEREVENT+4:
                game.player.image_swap()
    game.display.blit(game.player.image, game.player.rect)
    enemies.draw(game.display)
    enemies.update()
    pygame.display.flip()
game.display.blit(game.bg.image, game.bg.rect)
display_text(game.display, "center", game.SCREEN_WIDTH//2, game.SCREEN_HEIGHT//2, font2, "GAME OVER", GREEN)
display_text(game.display, "center", game.SCREEN_WIDTH//2, game.SCREEN_HEIGHT//2+64, font, f"SCORE: {game.score}", GREEN)
pygame.display.flip()
pygame.time.wait(3000)