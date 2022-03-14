import pygame
import os
import sys
sys.path.append("/Users/greninja028/Desktop/Tower_Defense")

from enemies.scorpion import Scorpion
from enemies.club import Club
from enemies.wizard import Wizard
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import DamageTower, RangeTower
import time
import random
pygame.font.init()

lifes_img = pygame.image.load(os.path.join("assets", "heart.png"))
star_imgs = pygame.image.load(os.path.join("assets", "star.png"))

class Game:
    def __init__(self):
        self.width = 1250
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = [Club()]
        self.attack_towers = [ArcherTowerLong(300,200),ArcherTowerLong(700,600), ArcherTowerShort(200,600),ArcherTowerShort(900,200)]
        self.support_towers = [RangeTower(100,600),DamageTower(400,200)]
        self.lifes = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("assets","bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width,self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 70)
        self.selected_tower = None

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            if time.time() - self.timer >= random.randrange(1,5)/2:
                self.timer = time.time()
                self.enemys.append(random.choice([Club(),Scorpion(),Wizard()]))
            # pygame.time.delay(500)
            clock.tick(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Look if you clicked on attack tower
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

            # Loop through enemies
            to_del = []
            for en in self.enemys:
                if en.x < -15:
                    to_del.append(en)

            # Delete all enemies off the screen
            for d in to_del:
                self.lifes -= 1
                self.enemys.remove(d)

            # Loop through attack towers
            for tw in self.attack_towers:
                tw.attack(self.enemys)

            # Loop through support towers
            for tw in self.support_towers:
                tw.support(self.attack_towers)

            if self.lifes <= 0:
                print("You  Lose")
                run = False

            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0,0))

        # Draw attack towers
        for tw in self.attack_towers:
            tw.draw(self.win)

        # Draw support towers
        for tw in self.support_towers:
            tw.draw(self.win)

        # Draw enemies
        for en in self.enemys:
            en.draw(self.win)

        # Draw lifes
        text = self.life_font.render(str(self.lifes), 1, (255,255,255))

        life = pygame.transform.scale(lifes_img,(50,50))
        start_x = self.width - life.get_width() - 10
        self.win.blit(text, (start_x - text.get_width() - 10, 13))
        self.win.blit(life, (start_x, 10))

        pygame.display.update()

    def draw_menu(self):
        pass

g = Game()
g.run()