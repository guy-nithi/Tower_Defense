import pygame
import os
import math
import sys
sys.path.append("/Users/greninja028/Desktop/Tower_Defense")

from enemies.scorpion import Scorpion
from enemies.club import Club
from enemies.wizard import Wizard
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import DamageTower, RangeTower
from menu.menu import VerticalMenu, PlayPauseButton
import time
import random
pygame.font.init()

path = [(-10, 226),(46, 225),(164, 222),(263, 273),(639, 265),(681, 222),(697, 147),(744, 76),(834, 55),(925, 118),(958, 217),(1042, 279),(1148, 317),(1168, 412),(1120, 480),(997, 490),(887, 496),(797, 528),(732, 560),(147, 545),(103, 460),(72, 359),(7, 341),(0, 341),(-40,334)]

lifes_img = pygame.image.load(os.path.join("assets", "heart.png"))
star_imgs = pygame.image.load(os.path.join("assets", "star.png"))
side_imgs = pygame.transform.scale(pygame.image.load(os.path.join("assets", "side.png")),(120,500))

buy_archer = pygame.transform.scale(pygame.image.load(os.path.join("assets", "buy_archer.png")),(75,75))
buy_archer2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "buy_archer_2.png")),(75,75))
buy_damage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "buy_damage.png")),(75,75))
buy_range = pygame.transform.scale(pygame.image.load(os.path.join("assets", "buy_range.png")),(75,75))

play_btn = pygame.transform.scale(pygame.image.load(os.path.join("assets", "button_start.png")),(75,75))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("assets", "button_pause.png")),(75,75))

wave_bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "wave.png")),(225,75))

attack_tower_names = ["archer","archer2"]
support_tower_names = ["range","damage"]

# Waves are in form
# Frequency of enemies
# (# of scorpion, # of wizards, # of clubs)
waves = [
    [20,0,0],
    [50,0,0],
    [100,0,0],
    [0,20,0],
    [0,50,0],
    [0,100,0],
    [20,100,0],
    [50,100,0],
    [100,100,0],
    [20,0,50],
    [20,0,100],
    [20,0,150],
    [0,0,200],
    [150,150,0],
    [0,1,0],
    [0,1,1],
    [1,1,1],
    [10,10,10],
    [100,100,100],
    [500,500,500]
]

class Game:
    def __init__(self):
        self.width = 1350
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.attack_towers = []
        self.support_towers = []
        self.lifes = 10
        self.money = 2000
        self.bg = pygame.image.load(os.path.join("assets","bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width,self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 65)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_imgs.get_width() + 70,250, side_imgs)
        self.menu.add_btn(buy_archer, "buy_archer",500)
        self.menu.add_btn(buy_archer2, "buy_archer_2",750)
        self.menu.add_btn(buy_damage, "buy_damage",1000)
        self.menu.add_btn(buy_range, "buy_range",1000)
        self.moving_object = False
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = True
        self.PlayPauseButton = PlayPauseButton(play_btn, pause_btn, 10, self.height - 85)

    def gen_enemies(self):
        """
        :Return
            enemy:
        """
        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.PlayPauseButton.paused = self.pause
        else:
            wave_enemies = [Scorpion(),Wizard(),Club()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def point_to_line(self,tower):
        """
        Returns if you can place tower based on distance from path

        Args:
            tower (Bool): 
        """
        # Find two closest points
        return True

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(100)

            if self.pause == False:
                # Gen Monsters
                if time.time() - self.timer >= random.randrange(1,6)/3:
                    self.timer = time.time()
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()
 
            # Check for moving object
            if self.moving_object:
                self.moving_object.move(pos[0],pos[1])
                tower_list = self.attack_towers[:] + self.support_towers[:]
                collide = False
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (255,0,0,100)
                        self.moving_object.place_color = (255,0,0,100)
                    else:
                        tower.place_color = (0,0,255,100)
                        if not collide:
                            self.moving_object.place_color = (0,0,255,100)

            # Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # If you're moving an object and click
                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.attack_towers[:] + self.support_towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object):
                                not_allowed = True

                        if not not_allowed and self.point_to_line(self.moving_object):
                            if self.moving_object.name in attack_tower_names:
                                self.attack_towers.append(self.moving_object)
                            elif self.moving_object.name in support_tower_names:
                                self.support_towers.append(self.moving_object)
                            self.moving_object.moving = False
                            self.moving_object = None
                    else:
                        # Check for play or pause
                        if self.PlayPauseButton.click(pos[0],pos[1]):
                            self.pause = not(self.pause)
                            self.PlayPauseButton.paused = self.pause

                        # Look if you click on side menu
                        side_menu_button = self.menu.get_clicked(pos[0],pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)

                        # Look if you clicked on attack tower or support tower
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0],pos[1])
                            if btn_clicked:
                                if btn_clicked == 'Upgrade':
                                    cost = self.selected_tower.menu.get_item_cost()
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.selected_tower.upgrade()

                        if not(btn_clicked):
                            for tw in self.attack_towers:
                                if tw.click(pos[0],pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

                                # Look if you clicked on support tower
                                for tw in self.support_towers:
                                    if tw.click(pos[0],pos[1]):
                                        tw.selected = True
                                        self.selected_tower = tw
                                    else:
                                        tw.selected = False

            if not self.pause:     
                # Loop through enemies
                to_del = []
                for en in self.enemys:
                    en.move()
                    if en.x < -15:
                        to_del.append(en)

                # Delete all enemies off the screen
                for d in to_del:
                    self.lifes -= 1
                    self.enemys.remove(d)

                # Loop through attack towers
                for tw in self.attack_towers:
                    self.money += tw.attack(self.enemys)

                # Loop through support towers
                for tw in self.support_towers:
                    tw.support(self.attack_towers)

                if self.lifes <= 0:
                    print("You Lose")
                    run = False

            self.draw()

        pygame.quit()

    def draw(self):

        self.win.blit(self.bg, (0,0))

        if self.moving_object:
            # Draw placement rings
            for tower in self.attack_towers:
                tower.draw_placement(self.win)

            for tower in self.support_towers:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)

        # Draw attack towers
        for tw in self.attack_towers:
            tw.draw(self.win)

        # Draw support towers
        for tw in self.support_towers:
            tw.draw(self.win)

        # Draw enemies
        for en in self.enemys:
            en.draw(self.win)

        # Redraw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)

        # Draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)

        # Draw menu
        self.menu.draw(self.win)

        # Draw play pause button
        self.PlayPauseButton.draw(self.win)

        # Draw lifes
        text = self.life_font.render(str(self.lifes), 1, (255,255,255))

        life = pygame.transform.scale(lifes_img,(50,50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 13))
        self.win.blit(life, (start_x, 10))

        # Draw money
        text = self.life_font.render(str(self.money), 1, (255,255,255))

        money = pygame.transform.scale(star_imgs,(50,50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 75))
        self.win.blit(money, (start_x, 65))

        # Draw wave
        self.win.blit(wave_bg, (10,10))
        text = self.life_font.render("Wave #" + str(self.wave),1,(255,255,255))
        self.win.blit(text, (10 + wave_bg.get_width()/2 - text.get_width()/2,25))

        pygame.display.update()

    def add_tower(self,name):
        x,y = pygame.mouse.get_pos()
        name_list = ["buy_archer", "buy_archer_2", "buy_damage", "buy_range"]
        object_list = [ArcherTowerLong(x,y),ArcherTowerShort(x,y),DamageTower(x,y), RangeTower(x,y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")


g = Game()
g.run()