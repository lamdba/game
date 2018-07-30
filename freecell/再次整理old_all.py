# -*- coding: utf-8 -*- 
#���ñ���硰���º��������������Ѷ��壩��

import pygame
import sys

def run_game():
	pygame.init()	
	global screen
	screen = pygame.display.set_mode((1200,800))#����screen�����ڣ�����
	pygame.display.set_caption("Freecell")#��������
	
	create()#��ʼ�����󣨽�������	
	while True:
		check_events()#�������
		var_update()#���²���	
		screen_update()#������ʾ 
		
def var_update():
	ship_update()#1.���·ɴ��Ĳ���
	bullet_update()#1.�����ӵ�����
		
class Ship(object):
	def __init__(self):
		self.x = 32
		self.y = -32-100
		self.left = False
		self.right = False
		self.in_air = True
		self.can_jump = 0 #�޹ؽ�Ҫ����Ϊ��һ����غ󱻸���
		self.up_speed = 0
		self.run_right = 0 #���Բ��һ����ʱ������һ���жϱ���
		self.run_left = 0
		self.image = pygame.image.load('images/ship.png')

class Bullet(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Constant(object):
	def __init__(self):
		self.ship_speed = 0.5      #����*n
		self.bullet_speed = 2
		self.bg_color = (0,127,0)
		self.jump_speed = 2
		self.jump_times = 5
		self.bullet_image = pygame.image.load('images/bullet.png')
		self.g = 0.01      
constant = Constant() 		           
		
def create():
	global ship
	global bullets,bullets_carry,count
	ship = Ship()
	bullets = {}
	bullets_carry = {}
	count = 1
	
def check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#~ ship.in_air = True
			#~ ship.can_jump -= 1
			#~ ship.up_speed = 2
			
			sys.exit()			
		elif event.type  ==pygame.KEYDOWN:
			check_keydown_events(event)#
		elif event.type  ==pygame.KEYUP:
			check_keyup_events(event)#
	
def check_keydown_events(event):
	if event.key == pygame.K_d:
		if ship.run_right != 0:#���ܼ��
			constant.ship_speed = 1
		ship.right = True
		ship.left = False  #
		ship.run_right = 300
		
	if event.key == pygame.K_a:
		if ship.run_left != 0:
			constant.ship_speed = 1
		ship.left = True
		ship.right = False #��ֹ���Ҳ���
		ship.run_left = 300

	if event.key == pygame.K_j:
		fire_bullet()#���º��������Ѷ��壩
	if event.key == pygame.K_k and ship.can_jump !=0:		
		ship.in_air = True
		ship.can_jump -= 1
		ship.up_speed = 2
	if event.key == pygame.K_q:
		sys.exit()			#��Щ����elif��Σ�		
		
def check_keyup_events(event):
	if event.key == pygame.K_d:
		ship.right = False
		constant.ship_speed = 0.5
	if event.key == pygame.K_a:
		ship.left = False
		constant.ship_speed = 0.5		
	
def make_bullet(n,x,y):
	exec('b'+str(n)+' = Bullet('+str(x)+','+str(y)+')',globals())
	
def add_bullet(n):
	exec("bullets[b"+str(n)+"]=b"+str(n),globals())

def del_bullet(n):
	exec('del(b'+str(n)+')',globals())	
	
def fire_bullet():
	global count
	make_bullet(count,ship.x +32+4,ship.y)
	add_bullet(count)
			 
	count += 1
	if count == 10000: #��ֹ��������������
		count = 0		# 	
	
def var_update():
	ship_update()
	bullet_update()
	
def ship_update():
	if ship.right and ship.x + 32 < 1200:
		ship.x += constant.ship_speed
	if ship.left and ship.x -32 > 0:
		ship.x -= constant.ship_speed
	if ship.run_right != 0:
		ship.run_right -= 1
	if ship.run_left != 0:
		ship.run_left -= 1	#˫��˥��
			
	if ship.in_air :
		ship.y -= ship.up_speed
		ship.up_speed -= constant.g
		if ship.y + 32 > 800:#��ؼ��
			ship.y = 800 - 32
			ship.in_air = False
			ship.up_speed = constant.jump_speed
			ship.can_jump = constant.jump_times				

def bullet_update():
	#�����ֵ��ڱ��������в��ɽ���ɾ���������ʲ��÷�ģ��
	global bullets,bullets_carry,count
	bullets_carry = bullets.copy()
	for k in bullets.keys():
		bullets_carry[k].x += constant.bullet_speed
		if bullets[k].x > (1200-4):
			del bullets_carry[k]
	bullets = bullets_carry.copy()
	
def screen_update():
	screen.fill(constant.bg_color) #����
	
	screen.blit (ship.image, 
				(ship.x-32, 
				 ship.y-32)
		        )                                 #�ɴ�����
	
	for k in bullets.keys():
		screen.blit(constant.bullet_image, 
				   (bullets[k].x-4, 
					bullets[k].y-4)
				   )                              #�ӵ�����
	
	pygame.display.flip()


run_game()#Ψһ��������Ĳ���	
