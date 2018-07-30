# -*- coding: utf-8 -*- 
#���ñ���硰���º��������������Ѷ��壩��

import pygame
import sys
import time


def run_game(): #���ø�ʽ
	pygame.init()	                
	pygame.display.set_caption("Freecell")
	global screen                       
	screen = pygame.display.set_mode((1200,800))
	clock = pygame.time.Clock()
	
	create()
	while True:
		clock.tick(100)
		check_events()
		var_update()
		screen_update()
		
		
def var_update():        #�����·Ǿ�ֹ�Ķ���
	ship_update()        #���·ɴ��Ĳ���
	bullet_update()      #�����ӵ�����
		
		
def create():   #����-����-����
	global cst
	cst = Cst() 
	global bullets,count
	bullets = {}  #�ֵ䣨�����������ڶ�̬����
	count = 1 
	global shelfs
	shelfs = []
	global ship
	ship = Ship() 
	global window #�������
	window =Window()
	window.x = 0
	window.y = 0 
	
	def create_shelf(n,x,y): 
		exec("shelf{n} = Shelf({n},{x},{y})".format(n=n,x=x,y=y),
		globals())       #��Ȼ����
		exec("shelfs.append(shelf{n})".format(n=n),globals())
		
	create_shelf(1,400,250)     
	create_shelf(2,800,500)    
	create_shelf(3,400,750)
	create_shelf(4,800,1000)
	create_shelf(5,400,1250)
	create_shelf(6,800,1500)
	
	cst.ship_speed1 = 2      #���٣������º������ã�
	cst.ship_speed2 = cst.ship_speed1 * 2
	cst.bullet_speed = 8     #�ӵ��ٶ�
	cst.bg_color = (0,127,0) #����ɫ  
	cst.jump_speed = 10  #��Ծ���ٶ�
	cst.jump_times = 5  #��������
	cst.g = 0.3    #���ٶ�
	cst.bullet_image = pygame.image.load('images/bullet.png')
	cst.bullet_image2 = pygame.image.load('images/bullet2.png')
	cst.bullet_image3 = pygame.image.load('images/bullet3.png')
	cst.bullet_image4 = pygame.image.load('images/bullet4.png')
	cst.shelf_image = pygame.image.load('images/shelf2.png') 
	cst.delay = 30
		
		
class Ship(object):
	def __init__(self):
		self.x = 32+150
		self.y = 600-32
		                #��������5�������һ�����飩
		self.position = 0#0-���У�1-���棻11-shelf1��12-shelf2 #
		self.horizontal_move = 0 #�˱���Ϊ��/��/ˮƽ��ֹ
		self.direction = 1		
		
		self.speed = 2 ##���������
		
		self.can_jump = 0 #�޹ؽ�Ҫ����Ϊ��һ����غ󱻸���
		self.up_speed = 0 #�����ٶ�
		self.run_clock = 0
		self.attack_clock = 0
		                       
		self.key_s = False #s�Ƿ��£���÷����ģ���
		self.key_w = False #w�Ƿ��£���÷����ģ���
		self.d2 = self.direction
		self.quiet = False
		
		self.image = pygame.image.load('images/ship.png')
		self.image2 = pygame.image.load('images/ship2.png')


	def blit(self):  #����
		if self.direction == 1:
			the_image = self.image
		else:
			the_image = self.image2	
		screen.blit (the_image, 
					(self.x-32 - window.x, 
					 self.y-32 - window.y)
		            )    		


class Bullet(object):
	def __init__(self,x,y,d,a,k = 0): #�����룩���꣬���򣬷������
		self.x = x
		self.y = y
		self.d = d
		self.a = a
		self.k = k
		
	def blit(self):  #���ӵ�
		if self.k == 2:
			if self.d == 1:
				the_image = cst.bullet_image5
			elif self.d == -1:
				the_image = cst.bullet_image6
			elif self.d == 2:
				the_image = cst.bullet_image7
			elif self.d == -2:
				the_image = cst.bullet_image8	
		else:	
			if self.d == 1:
				the_image = cst.bullet_image
			elif self.d == -1:
				the_image = cst.bullet_image2
			elif self.d == 2:
				the_image = cst.bullet_image3
			elif self.d == -2:
				the_image = cst.bullet_image4	
			
		screen.blit(the_image, 
				   (self.x-4 - window.x, 
					self.y-4 - window.y)
				   )
				   
	def update(self):
		if self.k == 0:
			if self.d == 1:
				self.x += cst.bullet_speed
			elif self.d == -1:
				self.x -= cst.bullet_speed
			elif self.d == 2:
				self.y -= cst.bullet_speed
			elif self.d == -2:
				self.y += cst.bullet_speed
		elif self.k == 1:
			if self.d == 1:
				self.x += (self.x - self.a + 1)/10
			elif self.d == -1:
				self.x -= (self.a - self.x + 1)/10
			elif self.d == 2:
				self.y -= (self.a - self.y + 1)/10
			elif self.d == -2:
				self.y += (self.y - self.a + 1)/10	


class Window(object):
	pass


class Cst(object):
	pass


class Shelf(object):
	def __init__(self,n,x,y): #�����������꣬��Ȼ��ʾ
		self.x = x
		self.y = 800 - y
		self.n = n
				
	def blit(self):  #��ƽ̨�����е�blit������window��
		screen.blit(cst.shelf_image,
				   (self.x - 64 - window.x,
					self.y - window.y)
					)
			
	
def check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:#�㡾�رա�
			sys.exit()					
		elif event.type  ==pygame.KEYDOWN:#������������
			check_keydown_events(event)
		elif event.type  ==pygame.KEYUP:#���������ɡ�
			check_keyup_events(event)
	
	
def check_keydown_events(event):
	if event.key == pygame.K_d:   #��D��
		if ship.run_clock != 0 or ship.speed == cst.ship_speed2:            
			ship.speed = cst.ship_speed2
		else:
			ship.speed = cst.ship_speed1
		ship.direction = 1
		ship.d2 = 1
		ship.horizontal_move = 1
		ship.run_clock = cst.delay
		
	elif event.key == pygame.K_a: #��A��
		if ship.run_clock != 0 or ship.speed == cst.ship_speed2:            
			ship.speed = cst.ship_speed2
		else:
			ship.speed = cst.ship_speed1
		ship.direction = -1
		ship.d2 = -1
		ship.horizontal_move = -1
		ship.run_clock = cst.delay

	elif event.key == pygame.K_j: #��J��
		if ship.attack_clock == 0:
			fire()
			ship.attack_clock = 30
	elif event.key == pygame.K_k: #��k��
		if ship.key_s and ship.position != 0:  #�����������S������			
			ship.position = 0   #ʧ��
			ship.up_speed = 0  
		elif ship.can_jump !=0 :  #����s/���з�S/��½��S ��
			ship.position = 0 #����
			ship.up_speed = cst.jump_speed #�������ϳ��ٶ�
			ship.can_jump -= 1 #��Ծ����-1
						
	elif event.key == pygame.K_s: #��S��
		ship.key_s = True
	elif event.key == pygame.K_w: #��W��
		ship.key_w = True
	elif event.key == pygame.K_q: #��Q��
		ship.position = 0
		ship.up_speed = cst.jump_speed * 2 
		ship.can_jump = cst.jump_times
		#~ sys.exit()
	elif event.key == pygame.K_e: #��E��
		ship.position = 1
		ship.can_jump = 5
	elif event.key == pygame.K_h:
		if ship.quiet:
			ship.quiet = False
		else:
			ship.quiet = True
	elif event.key == pygame.K_i: 
		trident()
							
		
def check_keyup_events(event):
	if event.key == pygame.K_d: #��D��
		if ship.horizontal_move == 1: #���������     #��ì��״̬���İ����������
			ship.horizontal_move = 0
		
	elif event.key == pygame.K_a: #��A��
		if ship.horizontal_move == -1: 
			ship.horizontal_move = 0
				
	elif event.key == pygame.K_s: #��S����
		ship.key_s = False	
	elif event.key == pygame.K_w: #��W��
		ship.key_w = False	


def make_bullet(n,x,y,d,k = 0):                     #����汾��û�Ž�ȥ
	global count	
	if d in [1,-1]:
		a = x
	else:
		a = y
	exec("b{n} = Bullet({x},{y},"
	"{d},{a},{k})".format(n=n,x=x,y=y,d=d,a=a,k=k),
	globals())
	
	def add_bullet(n):
		exec("bullets[b{n}]=b{n}".format(n=n),globals())
	add_bullet(count)
	
	count += 1
	
	if count == 10000: #��ֹ��������������
		count = 0		# 	


def trident():
	if ship.key_w and ship.key_s:
		return 0
	elif ship.key_w:
		make_bullet(count,ship.x,ship.y +32+30,2,1)
		make_bullet(count,ship.x +32-9,ship.y +32+30,2,1)
		make_bullet(count,ship.x -32+9,ship.y +32+30,2,1)
	elif ship.key_s:
		make_bullet(count,ship.x,ship.y -32-30,-2,1)
		make_bullet(count,ship.x +32-9,ship.y -32-30,-2,1)
		make_bullet(count,ship.x -32+9,ship.y -32-30,-2,1)	
	elif ship.direction == 1:
		make_bullet(count,ship.x -32-30,ship.y,1,1)
		make_bullet(count,ship.x -32-30,ship.y +32-9,1,1)
		make_bullet(count,ship.x -32-30,ship.y -32+9,1,1)
	else:
		make_bullet(count,ship.x +32+30,ship.y,-1,1)
		make_bullet(count,ship.x +32+30,ship.y+32-9,-1,1)
		make_bullet(count,ship.x +32+30,ship.y-32+9,-1,1)	
	

def fire(k = 0):           
	
	if ship.key_w and ship.key_s:
		return 0
	elif ship.key_w:
		make_bullet(count,ship.x,ship.y -32-9,2)
	elif ship.key_s:
		make_bullet(count,ship.x,ship.y +32+9,-2)	
	elif ship.direction == 1:
		make_bullet(count,ship.x +32+4,ship.y,1)
	else:
		make_bullet(count,ship.x -32-4,ship.y,-1)
	

def is_on(ship,shelf_list):
	for shelf in shelf_list:
		if shelf.x -96 < ship.x < shelf.x +96:
			if shelf.y + ship.up_speed  < ship.y+32 < shelf.y:
				ship.y = shelf.y - 32 #���
				ship.position = 10 + shelf.n	
				ship.up_speed = cst.jump_speed
				ship.can_jump = cst.jump_times
		else:
			continue
	if ship.y + 32 > 800:#��ؼ��				
		ship.y = 800 - 32
		ship.position = 1	
		ship.up_speed = cst.jump_speed
		ship.can_jump = cst.jump_times	


def is_out(ship):
	if ship.position > 10:
		shelf = eval("shelf"+str(ship.position - 10))
		if (ship.x < shelf.x - 96 or\
			ship.x > shelf.x + 96):
				ship.up_speed = 0
				ship.position = 0	
		

def ship_update():
	if ship.horizontal_move == 1 : #����
		ship.x += ship.speed
		if ship.x + 32 - window.x >= 1200 - 100 :
			window.x = ship.x + 32+100-1200    #�������Ļ�����ر�仯��
	elif ship.horizontal_move == -1 :
		ship.x -= ship.speed
		if ship.x - 32 -window.x <= 0 + 100:
			window.x = ship.x - 32-100
		
	if ship.run_clock != 0:
		ship.run_clock -= 1#˥����
		
	if ship.attack_clock != 0:
		ship.attack_clock -= 1	
		
	if ship.position == 0 : 
		if ship.up_speed > -50:         #���׹��
			ship.up_speed -= cst.g
		ship.y -= ship.up_speed
		if ship.position != 16:     #��֪�к���
			if ship.y < 400: #��������
				window.y = ship.y - 400
			else:	
				window.y = 0  
		
		is_on(ship,shelfs)		
	
	is_out(ship)	
		
	if ship.position == 16 and window.y > -1500:       #####��ǳ����Σ�������Ҳ�벻���к��ô�
		window.y -= 2
		
						
def bullet_update():   
	global bullets,count
	if not ship.quiet:		#��H��
		bullets_carry = bullets.copy()#��ģ������ԭ�ֵ�ļ��������ֵ�
		for k in bullets.keys():        
			bullets_carry[k].update()
			if bullets_carry[k].d == 1:
				r = bullets_carry[k].x - bullets_carry[k].a
			elif bullets_carry[k].d == -1:
				r = bullets_carry[k].a - bullets_carry[k].x
			elif bullets_carry[k].d == 2:
				r = bullets_carry[k].a - bullets_carry[k].y
			elif bullets_carry[k].d == -2:
				r = bullets_carry[k].y - bullets_carry[k].a
			if r > 1200:
				del bullets_carry[k]
		bullets = bullets_carry.copy()
		
		
def screen_update():
	screen.fill(cst.bg_color) #����
		
	for shelf in shelfs:
		shelf.blit()
		
	ship.blit()                             #�ɴ�����
	
	for k in bullets.keys():
		bullets[k].blit()                        #�ӵ�����
	
	pygame.display.flip()


run_game()#Ψһ��������Ĳ���	


#    �������Ǹ��Ի����֣����ڳ��������á��ӵ���λ���Ǳ�����ͼ���ǳ�������bullet��ֻ����
# �������ԣ����ڴ���ʱҪ����������ԣ����ӵ�����ʱ���ó����е�ͼ�񣻷ɴ�ֻ��һ�ң�����ν
# �ѳ������ںδ���shelf���������Ĳ���������λ��

#�����϶���elif���Լ��ټ�� ����Ҳ�����ǡ��������������������������

#�������ά�ȣ�ĳ�����Ƿ��£�ÿ�������Ƕ�����ά�ȣ���ĳһ״̬��ֵ��ÿһ״̬����һ��ά�ȣ�
#  ���ɣ�������໥������ά��


#��shelf�������࣬һ��һ�������Ȼ����ʾ����ΰѼ���޶�������֮�ڣ���������㷨��

#��Ȼ��x��y���ܾ���״̬������������¼����ı�״̬�Լ��ٹ��������ǲ������м�ⶼ�ܱܿ�����
#  Ʃ����ؼ�⡣

#��ship����ԾǨ��ֵ��ʱ��Ӧ��δ�����Ļ���������ı俴��ϵ��

#�಻�����ñ��˵ĳ���
