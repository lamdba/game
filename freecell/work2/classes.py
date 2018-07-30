# -*- coding: utf-8 -*- 
import pygame
from setting import *

class Ship(object):
	def __init__(self):
		self.x = 32+150
		self.y = 600-32
		                #��������5�������һ�����飩
		self.position = 0#0-���У�1-���棻11-shelf1��12-shelf2 #
		self.horizontal_move = 0 #�˱���Ϊ��/��/ˮƽ��ֹ
		self.direction = 1		
		self.view = 0 #0-ƽ��ģʽ��1-����ģʽ
		self.speed = 0.5 ##���������,������취�ڴ���ʱ�ų�ʼ��
		
		self.can_jump = 0 #�޹ؽ�Ҫ����Ϊ��һ����غ󱻸���
		self.up_speed = 0 #�����ٶ�
		self.run_clock = 0
		                       
		self.key_s = False #k�Ƿ��£���÷����ģ���
		
		self.image = pygame.image.load('images/ship.png')
		self.image2 = pygame.image.load('images/ship2.png')
			
	
	def blit(self,screen,window):  #����
		if self.direction == 1:
			the_image = self.image
		else:
			the_image = self.image2	
		screen.blit (the_image, 
					(self.x-32 - window.x, 
					 self.y-32 - window.y)
		            ) 

class Bullet(object):
	def __init__(self,x,y,d): #�ӵ��������룩���꣬����
		self.x = x
		self.y = y
		self.direction = d
		
	def blit(self,screen,window):  #���ӵ�
		if self.direction == 1:
			the_image = cst.bullet_image
		else:
			the_image = cst.bullet_image2
		screen.blit(the_image, 
				   (self.x-4 - window.x, 
					self.y-4 - window.y)
				   )			

class Shelf(object):
	def __init__(self,n,x,y): #���ն����������꣬���á���ѧ��ʾ��������
		self.x = x
		self.y = 800 - y
		self.n = n
				
	def blit(self):  #��ƽ̨�����е�blit������window��
		screen.blit(cst.shelf_image,
				   (self.x - 64 - window.x,
					self.y - window.y)
					)
			
	def on_detect(self,ship):                                                ##��������һ�����������ն����shelf�б������ж�������y��position��u_s��c_j������Ҫ��Ϊ�����𣿣�
		if  ship.y + 32 > self.y + ship.up_speed -5 and \
			ship.y + 32 < self.y  and \
			ship.x > self.x - 96 and\
			ship.x < self.x + 96:
				
				ship.y = self.y - 32 #���
				
				ship.position = 10 + self.n	
				ship.up_speed = cst.jump_speed
				ship.can_jump = cst.jump_times	
				return True
		else:
			return False			
				
	def out_detect(self):                 #���Ҳ�ƺ���Ӧ������shelf�ࡣ����
		if ship.position == 10 + self.n :
			if (ship.x < self.x - 96 or\
					ship.x > self.x + 96):
				ship.up_speed = 0
				ship.position = 0	
