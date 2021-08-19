import pygame
#Use 2D vectors
vector = pygame.math.Vector2

#Initialize pygame
pygame.init()

#Set display surface (tile size is 32x32 so 960/32 = 30 tiles wide, 640/32 = 20 tiles high)
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Making a tile map!")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Define classes
class Tile(pygame.sprite.Sprite):
    """A class to read and create individual tiles and place them in the display"""

    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        #Load in the correct image and add it to the correct sub groups
        if image_int == 1:
            self.image = pygame.image.load("dirt.png")
        elif image_int == 2:
            self.image = pygame.image.load("grass.png")
            self.mask = pygame.mask.from_surface(self.image)
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load("water.png")
            sub_group.add(self)
        
        #Add every tile to the main tile group
        main_group.add(self)

        #Get the rect of the image and position within the grid
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pygame.draw.rect(display_surface, (0, 0, 255), self.rect, 1)


class Player(pygame.sprite.Sprite):
    """A player class the user can control"""

    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()

        #Animation Frames
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []

        #Moving Right
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (1).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (2).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (3).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (4).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (5).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (6).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (7).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (8).png"), (64,64)))

        #Moving Left
        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        #Idle Right
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (1).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (2).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (3).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (4).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (5).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (6).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (7).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Idle (8).png"), (64,64)))

        #Idle Left
        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.current_sprite = 0
        self.image = self.move_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.starting_x = x
        self.starting_y = y

        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        #Kinematics vectors (first value is the x, second value is the y)
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        #Kinematic constants
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCLERATION = .5 #Gravity
        self.VERTICAL_JUMP_SPEED = 15 #Detemerines how high we can jump
       


    def update(self):
        pygame.draw.rect(display_surface, (255, 255, 0), self.rect, 1)
        
        #Create a mask
        self.mask = pygame.mask.from_surface(self.image)
        #Draw the mask
        mask_outline = self.mask.outline()
        pygame.draw.lines(self.image, (255, 255, 0), True, mask_outline)

        self.move()
        self.check_collisions()


    def move(self):
        #Set the accleration vector to (0, 0) so there is initially no acceleration
        #If there is no force (no key presses) acting on the player then accerlation should be 0
        #Vertical accelration (gravity) is present always regardless of key-presses
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)

        #If the user is presseing a key, set the x-component of the accleration vector to a non zero value.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1*self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .2)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .2)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, .2)
            else:
                self.animate(self.idle_left_sprites, .2)

        #Calculate new kinematics values (2, 5) + (1, 6) = (3, 11)
        self.acceleration.x -= self.velocity.x*self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        #Update new rect based on kinematic calculations and add wrap around motion
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position


    def check_collisions(self):
        #Check for collisions with the grass tiles
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False, pygame.sprite.collide_mask)
        if collided_platforms:
            #Only move to the platform if the player is falling down
            if self.velocity.y > 0:
                self.position.y = collided_platforms[0].rect.top + 10
                self.velocity.y = 0

        #Check for collisions with the water tiles
        if pygame.sprite.spritecollide(self, self.water_tiles, False):
            print("YOU CANT SWIM!!!")
            self.position = vector(self.starting_x, self.starting_y)
            self.velocity = vector(0, 0)


    def jump(self):
        #Only jump if on a grass tile
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = -1*self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, speed):
        #Loop through the sprite list changing the current sprite
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


#Create sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()

#Create the tile map: 0 -> no tile, 1 -> dirt, 2 -> grass, 3 -> water, 4 -> player
#20 rows and 30 columns
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1]
]

#Create individual Tile objects from the tile map
#Loop through the 20 lists in tile_map (i moves us down the map)
for i in range(len(tile_map)):
    #Loop through the 30 elements in a given list (j moves us across the map)
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1:
            Tile(j*32, i*32, 1, main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j*32, i*32, 2, main_tile_group, grass_tile_group)
        elif tile_map[i][j] == 3:
            Tile(j*32, i*32, 3, main_tile_group, water_tile_group)
        elif tile_map[i][j] == 4:
            my_player = Player(j*32, i*32 + 32, grass_tile_group, water_tile_group)
            my_player_group.add(my_player)

#Load in a background image
background_image = pygame.image.load("background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

#The main game loop
running = True
while running:
    #Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Player wants to jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()

    #Blit the background
    display_surface.blit(background_image, background_rect)

    #Draw tiles
    main_tile_group.draw(display_surface)
    main_tile_group.update()

    #Update and draw sprites
    my_player_group.update()
    my_player_group.draw(display_surface)

    #Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()