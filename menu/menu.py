from logging import exception
import pygame
import os
pygame.font.init()

star = pygame.transform.scale(pygame.image.load(os.path.join("assets","star.png")), (50,50))
star2 = pygame.transform.scale(pygame.image.load(os.path.join("assets","star.png")), (20,20))

class Button:
    """
    Button class for menu object
    """
    def __init__(self,menu,img,name):
        self.name = name
        self.img = img
        self.x = menu.x - 50
        self.y = menu.y - 110
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.imgs = []
        self.items = 0

    def click(self,X,Y):
        """
        Returns if the position has collided with the menu

        Args:
            X (int):
            Y (int):

        Returns:
            bool:
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
            return False

    def draw(self,win):
        win.blit(self.img,(self.x,self.y))

    def update(self):
        self.x = self.menu.x - 50
        self.y = self.menu.y - 110

class VerticalButton(Button):
    """
    Button class for menu object
    """
    def __init__(self,x,y,img,name,cost):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost

class PlayPauseButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = True

    def draw(self, win):
        if self.paused:
            win.blit(self.play,(self.x,self.y))
        else:
            win.blit(self.pause, (self.x,self.y))

class Menu:
    """
    Menu for holding items
    """
    def __init__(self,tower,x,y,img,item_cost):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.item_cost = item_cost
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("comicsans",20)
        self.tower = tower

    def add_btn(self,img,name):
        """
        Adds buttons to menu

        Args:
            img (surface):
            name (str):
        """
        self.items += 1
        self.buttons.append(Button(self,img,name))

    def get_item_cost(self):
        return self.item_cost[self.tower.level - 1]

    def draw(self,win):
        """
        Draws btn and menu bg

        Args:
            win (surface):
        """
        win.blit(self.bg,(self.x - self.bg.get_width()/2,self.y-120))
        for item in self.buttons:
            item.draw(win)
            win.blit(star, (item.x + item.width + 5,item.y-9))
            text = self.font.render(str(self.item_cost[self.tower.level-1]),1,(255,255,255))
            win.blit(text,(item.x + item.width + 30 - text.get_width()/2, item.y + star.get_height() - 8))


    def get_clicked(self,X,Y):
        """
        Returns the clicked item from the menu

        Args:
            X (int):
            Y (int):
        
        Returns:
            str:
        """
        for btn in self.buttons:
            if btn.click(X,Y):
                return btn.name
        
        return None

    def update(self):
        """
        update menu and button location

        Returns:
            None:
        """
        for btn in self.buttons:
            btn.update()

class VerticalMenu(Menu):
    """
    Vertical Menu For Side Bar of Game
    """
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("comicsans", 25)

    def add_btn(self, img, name, cost):
        """
        Adds buttons to menu

        Args:
            img (surface):
            name (str):
        """
        self.items += 1
        btn_x = self.x - 40
        btn_y = self.y-100 + (self.items-1)*120
        self.buttons.append(VerticalButton(btn_x,btn_y,img,name,cost))


    def get_item_cost(self,name):
        for btn in self.buttons:
            if btn.name == name:
                return btn.cost

        return -1

    def draw(self,win):
        """
        Draws btn and menu bg

        Args:
            win (surface):
        """
        win.blit(self.bg,(self.x - self.bg.get_width()/2,self.y-120))
        for item in self.buttons:
            item.draw(win)
            win.blit(star2, (item.x+2,item.y + item.height))
            text = self.font.render(str(item.cost),1,(255,255,255))
            win.blit(text,(item.x + item.width/2 - text.get_width()/2 + 7, item.y + item.height + 5))