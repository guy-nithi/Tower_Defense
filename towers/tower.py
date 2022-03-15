import pygame
from menu.menu import Menu
import os

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("assets","menu.png")), (120,70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("assets","upgrade.png")), (50,50))

class Tower:
    """
    Abstract class for towers
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0,0,0]
        self.price = [0,0,0]
        self.level = 1
        self.selected = False
        self.tower_imgs = []
        self.damage = 1
        # Define Menu and buttons
        self.menu = Menu(self.x,self.y,menu_bg,[2000,5000,12000])
        self.menu.add_btn(upgrade_btn,"Upgrade")

    def draw(self, win):
        """draws the tower

        Args:
            win (_type_): surface
        """
        img = self.tower_imgs[self.level-1]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))
        
        # Draw menu
        if self.selected:
            self.menu.draw(win)

    def draw_radius(self,win):
        if self.selected:
            # Draw range circle
            surface = pygame.Surface((self.range*4, self.range*4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (128,128,128, 100), (self.range, self.range), self.range, 0)

            win.blit(surface, (self.x-self.range, self.y-self.range))

    def click(self,x,y):
        """
        returns if tower has been clicked on
        and selects tower if it was clicked

        :param x: int
        :param y: int

        Returns:
            bool
        """
        img = self.tower_imgs[self.level-1]
        if x <= self.x - img.get_width()//2 + self.width and x >= self.x - img.get_width()//2:
            if y <= self.y + self.height - img.get_height()//2 and y >= self.y - img.get_height()//2:
                return True
        
        return False

    def sell(self):
        """
        call to sell the tower, returns sell price
        """
        return self.sell_price[self.level-1]

    def upgrade(self):
        """
        upgrades the tower for a give cost

        Returns:
            None:
        """
        self.level += 1
        self.damage += 1

    def get_upgrade_cost(self):
        """
        returns the upgrade cost, if 0 then can't upgrade anymore

        Returns:
            int:
        """
        return self.price[self.level-1]

    def move(self,x,y):
        self.x = x
        self.y = y
