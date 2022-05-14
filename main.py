import random
import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Psycho Runner')

game_over = 0
tile_dim = 50
score = 0

font = pygame.font.Font(None, 32)
end_text = font.render('GAME OVER', True, (235, 0, 0), 0)
end_rect = end_text.get_rect()
end_rect.center = (width // 2, height // 3)
background = pygame.image.load('background.png')


class Psycho:
    def __init__(self, x, y):
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img, (30, 50))
        self.dead_img = pygame.image.load('dead.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self, game):
        dx = 0
        dy = 0
        if game == 0:
            key = pygame.key.get_pressed()
            if (key[pygame.K_UP]) and self.jumped == False:
                self.vel_y = -18
                self.jumped = True
            if not key[pygame.K_UP]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 4
            if key[pygame.K_RIGHT]:
                dx += 4
            # gravity
            self.vel_y += 2
            if self.vel_y > 3.5:
                self.vel_y = 3.5
            dy += self.vel_y
            # Checks for collisions with other rects
            for tile in env.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
            self.rect.x += dx
            self.rect.y += dy
            if self.rect.bottom > height:
                self.rect.bottom = height
            if pygame.sprite.spritecollide(self, obstacle_group, False):
                game = -1
        elif game == -1:
            self.image = self.dead_img
            if self.rect.y > 200:
                self.rect.y -= 5

        window.blit(self.image, self.rect)
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)
        return game


# Used for creating the map and visualisation
def create_grid():
    for line in range(0, 10):
        pygame.draw.line(window, (255, 255, 255), (0, line * tile_dim), (width, line * tile_dim))
        pygame.draw.line(window, (255, 255, 255), (line * tile_dim, 0), (line * tile_dim, height))


class Map:
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('dirt.png')
        sand_img = pygame.image.load('sand.png')
        row_val = 0
        for row in data:
            col_val = 0
            for tile in row:
                if tile == 1:
                    block = pygame.transform.scale(dirt_img, (tile_dim, tile_dim))
                    block_rect = block.get_rect()
                    block_rect.x = col_val * tile_dim
                    block_rect.y = row_val * tile_dim
                    tile = (block, block_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    block = pygame.transform.scale(sand_img, (tile_dim, tile_dim))
                    block_rect = block.get_rect()
                    block_rect.x = col_val * tile_dim
                    block_rect.y = row_val * tile_dim
                    tile = (block, block_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    obstacle = Obstacle(col_val * tile_dim, row_val * tile_dim + 15)
                    obstacle_group.add(obstacle)
                if tile == 4:
                    gem = Gem(col_val * tile_dim + (tile_dim // 2), row_val * tile_dim + (tile_dim // 2))
                    gem_group.add(gem)
                col_val += 1
            row_val += 1

    def create(self):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('obstacle.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 12
        if abs(self.move_counter) > 25:
            self.move_direction *= -1
            self.move_counter *= -12
        pygame.draw.rect(window, (255, 255, 255), self.rect)


class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        gem = pygame.image.load('gem.png')
        self.image = pygame.transform.scale(gem, (tile_dim // 2, tile_dim // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


def generate_map():
    cols = 10
    rows = 10
    empty_map = [[0 for y in range(cols)] for x in range(rows)]

    # create floor
    for i in range(cols):
        empty_map[rows - 1][i] = 2

    start_map = empty_map

    return start_map


def update_map(current, total_time, prev_update):
    new_val = current
    gem_group.empty()
    obstacle_group.empty()
    if total_time - 1000 > prev_update:
        for i in range(0, 9):
            for j in range(0, 9):
                new_val[i][j] = new_val[i][j + 1]
        ran_col = random.randint(1, 8)
        ran_row = random.randint(6, 9)
        obs_prob = random.randint(0, 99)
        if new_val[ran_col][ran_row] == 0:
            new_val[ran_col][ran_row] = 2
            if obs_prob > 80:
                new_val[ran_col][8] = 3
            elif 80 > obs_prob > 60:
                new_val[ran_col][ran_row] = 4
        prev_update = total_time

    return new_val, prev_update


psycho = Psycho(100, height - 130)

obstacle_group = pygame.sprite.Group()
gem_group = pygame.sprite.Group()

score_gem = Gem(tile_dim // 2, tile_dim // 2)
gem_group.add(score_gem)


def draw_score(text, font, text_col, x, y):
    score_text = font.render(text, True, text_col)
    window.blit(score_text, (x, y))


run = True
total_time = 0
prev_update = 0
map_val = generate_map()
env = Map(map_val)

while run:
    total_time += clock.get_time()
    clock.tick(60)
    window.blit(background, (0, 0))
    if game_over == 0:
        map_val_new = update_map(map_val, total_time, prev_update)
        prev_update = map_val_new[1]
        env = Map(map_val_new[0])
        env.create()
        if pygame.sprite.spritecollide(psycho, gem_group, True):
            score += 1
    obstacle_group.update()
    gem_group.draw(window)
    draw_score('X ' + str(score), pygame.font.SysFont('Bauhaus 93', 28), (255, 255, 255), tile_dim - 10, 10)
    obstacle_group.draw(window)
    game_over = psycho.update(game_over)
    if game_over == -1:
        window.blit(end_text, end_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
