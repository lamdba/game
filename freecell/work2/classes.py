# -*- coding: utf-8 -*- 
import pygame
from setting import *

class Ship(object):
	def __init__(self):
		self.x = 32+150
		self.y = 600-32
		                #（以下是5个正交且互斥的组）
		self.position = 0#0-空中；1-地面；11-shelf1；12-shelf2 #
		self.horizontal_move = 0 #此变量为左/右/水平静止
		self.direction = 1		
		self.view = 0 #0-平地模式；1-空中模式
		self.speed = 0.5 ##这里很尴尬,必须想办法在创建时才初始化
		
		self.can_jump = 0 #无关紧要，因为第一次落地后被更新
		self.up_speed = 0 #上升速度
		self.run_clock = 0
		                       
		self.key_s = False #k是否按下（这该放在哪？）
		
		self.image = pygame.image.load('images/ship.png')
		self.image2 = pygame.image.load('images/ship2.png')
			
	
	def blit(self,screen,window):  #画船
		if self.direction == 1:
			the_image = self.image
		else:
			the_image = self.image2	
		screen.blit (the_image, 
					(self.x-32 - window.x, 
					 self.y-32 - window.y)
		            ) 

class Bullet(object):
	def __init__(self,x,y,d): #子弹：（中央）坐标，方向
		self.x = x
		self.y = y
		self.direction = d
		
	def blit(self,screen,window):  #画子弹
		if self.direction == 1:
			the_image = cst.bullet_image
		else:
			the_image = cst.bullet_image2
		screen.blit(the_image, 
				   (self.x-4 - window.x, 
					self.y-4 - window.y)
				   )			

class Shelf(object):
	def __init__(self,n,x,y): #接收顶部中央坐标，采用【数学表示】（？）
		self.x = x
		self.y = 800 - y
		self.n = n
				
	def blit(self):  #画平台（所有的blit都依赖window）
		screen.blit(cst.shelf_image,
				   (self.x - 64 - window.x,
					self.y - window.y)
					)
			
	def on_detect(self,ship):                                                ##考虑这样一个函数：接收对象和shelf列表，做出判定（设置y，position，u_s和c_j）（需要作为方法吗？）
		if  ship.y + 32 > self.y + ship.up_speed -5 and \
			ship.y + 32 < self.y  and \
			ship.x > self.x - 96 and\
			ship.x < self.x + 96:
				
				ship.y = self.y - 32 #落地
				
				ship.position = 10 + self.n	
				ship.up_speed = cst.jump_speed
				ship.can_jump = cst.jump_times	
				return True
		else:
			return False			
				
	def out_detect(self):                 #这个也似乎不应该属于shelf类。。。
		if ship.position == 10 + self.n :
			if (ship.x < self.x - 96 or\
					ship.x > self.x + 96):
				ship.up_speed = 0
				ship.position = 0	
