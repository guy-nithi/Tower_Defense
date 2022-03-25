import pygame
import math

class Enemy:

    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(-10, 226),(46, 225),(164, 222),(263, 273),(639, 265),(681, 222),(697, 147),(744, 76),(834, 55),(925, 118),(958, 217),(1042, 279),(1148, 317),(1168, 412),(1120, 480),(997, 490),(887, 496),(797, 528),(732, 560),(147, 545),(103, 460),(72, 359),(7, 341),(0, 341),(-40,334)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dist = 0
        self.imgs = []
        self.flipped = False
        self.max_health = 0

    def draw(self,win):
        """

        Draws the enemy with the given images
        :param win: surface
        :return: None
        """
        self.img = self.imgs[self.animation_count]

        win.blit(self.img,(self.x-self.img.get_height()/2,self.y-self.img.get_height()/2 - 35))
        self.draw_health_bar(win)

    def draw_health_bar(self,win):
        """
        draw health bar above enemy

        Args:
            win (_type_): surface
        """
        length = 50
        move_by = round(length / self.max_health)
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255,0,0),(self.x-30, self.y-75, length, 10), 0)
        pygame.draw.rect(win, (0,255,0),(self.x-30, self.y-75, health_bar, 10), 0)

    def collide(self,X,Y):
        """
        Returns if position has hit enemy
        :param X: int
        :param Y: int
        :return: Bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        
        return False

    def move(self):
        """
        Move enemy
        :return: None
        """
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2,y2 = (-10, 355)
        else:
            x2, y2 = self.path[self.path_pos+1]

        dirn = ((x2-x1)*2,(y2-y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length, dirn[1]/length)

        if dirn[0] < 0 and not(self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

        self.x = move_x
        self.y = move_y

        # Go to the next point
        if dirn[0] >= 0: # Moving right
            if dirn[1] >= 0: # Moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos +=1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else: # Moving left
            if dirn[1] >= 0: # Moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos +=1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
        

    def hit(self,damage):
        """
        Returns if an enemy has died removes one health
        each call
        :return: Bool
        """

        self.health -= damage
        if self.health <= 0:
            return True
        return False