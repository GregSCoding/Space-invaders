import pygame
import random
from helpers_pygame import get_image, display_text
BOUNDARY = 500
SPEED = 65
BULLET_SPEED = 5
ENEMIES_SPEED = 2
ENEMIES_NUMBER = 15
PLAYER_SPEED = 3
FLAG = False
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)
player_bullets = pygame.sprite.RenderPlain()
enemy_bullets = pygame.sprite.RenderPlain()
enemies = pygame.sprite.RenderPlain()


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
    def __init__(self, image_file, location, side):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
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
    def __init__(self, image_file1, image_file2, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.current_image = random.randint(0, 1)
        self.frame_timer = 80
        self.images = (pygame.image.load(image_file1), pygame.image.load(image_file2))
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        enemies.add(self)

    def update(self):
        global ENEMIES_SPEED
        global FLAG
        self.rect.left += ENEMIES_SPEED
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
              
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 700
        self.display = pygame.display.set_mode(size=(self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.can_shoot = True
        self.score = 0
        self.game_over = False
        pygame.time.set_timer(pygame.USEREVENT+2, 100) # Timer for enemy shooting
        pygame.time.set_timer(pygame.USEREVENT+3, 80) # Timer for player animation
        pygame.display.set_caption("Space Invaders")
        pygame.init()
    
    def next_turn(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.can_shoot:
                    Bullet("images/laser.png", [player.rect.left+28, player.rect.top-30], "player")
                    pygame.time.set_timer(pygame.USEREVENT+1, 1500, loops=1) # Timer to prevent cosntant player fire
                    self.can_shoot = False
            elif event.type == pygame.USEREVENT+1:
                self.can_shoot = True
            elif event.type == pygame.USEREVENT+2:
                idx = random.randint(0, len(enemies)-1)
                enemies.sprites()[idx].shoot()
            elif event.type == pygame.USEREVENT+3:
                player.image_swap()

        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]:
            player.rect.left -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.rect.right += PLAYER_SPEED
        if keys[pygame.K_UP] and player.rect.top > BOUNDARY:
            player.rect.top -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player.rect.top < game.SCREEN_HEIGHT - 40:
            player.rect.top += PLAYER_SPEED

    def update_ui(self):
        global FLAG
        global ENEMIES_SPEED
        game.display.blit(bg.image, bg.rect)
        players.draw(game.display)
        player_bullets.draw(game.display)
        enemy_bullets.draw(game.display)
        player_bullets.update()
        enemy_bullets.update()
        player_hits = pygame.sprite.groupcollide(player_bullets, enemies, True, True)
        for hit in player_hits:
            self.score += 1
        death = pygame.sprite.groupcollide(enemy_bullets, players, True, True)
        if death:
            self.game_over = True
        enemies.draw(game.display)
        enemies.update()
        display_text(self.display, "bottomleft", 0, self.SCREEN_HEIGHT, font, f"Score: {str(self.score)}", GREEN)
        if FLAG:
            ENEMIES_SPEED = -ENEMIES_SPEED
            FLAG = False
        pygame.display.flip()



game = Game()
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 64)
bg = Background("images/bg.png",[0,0])
player_sheet = pygame.image.load("images/statek.png")
images = [get_image(player_sheet, 1.5, x, 39, 39) for x in range(8)]
player = Player(images, [game.SCREEN_WIDTH//2, game.SCREEN_HEIGHT - 42])
players = pygame.sprite.RenderPlain()
players.add(player)

for i in range(ENEMIES_NUMBER):
    enemies.add(Enemy("images/ufolud3-1.png", "images/ufolud3-2.png", [i*50, 0]))
    enemies.add(Enemy("images/ufolud2-1.png", "images/ufolud2-2.png", [i*50, 40]))
    enemies.add(Enemy("images/ufolud1-1.png", "images/ufolud1-2.png", [i*50, 80]))

while not game.game_over:
    game.clock.tick(SPEED)
    game.next_turn()
    game.update_ui()

pygame.time.set_timer(pygame.USEREVENT+2, 0)
pygame.time.set_timer(pygame.USEREVENT+3, 5000)
pygame.time.set_timer(pygame.USEREVENT+4, 600, loops = 8)
stay = player.images.pop()
player.frame = 1
player.images = [pygame.image.load("images/blank.png"), stay]
over_screen = True
while over_screen:
    game.display.blit(bg.image, bg.rect)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.USEREVENT+3:
                over_screen = False
            elif event.type == pygame.USEREVENT+4:
                player.image_swap()
    game.display.blit(player.image, player.rect)
    pygame.display.flip()

display_text(game.display, "center", game.SCREEN_WIDTH//2, game.SCREEN_HEIGHT//2, font2, "GAME OVER", GREEN)
display_text(game.display, "center", game.SCREEN_WIDTH//2, game.SCREEN_HEIGHT//2+64, font, f"SCORE: {game.score}", GREEN)
pygame.display.flip()
pygame.time.wait(5000)