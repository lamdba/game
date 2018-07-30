# -*- coding: utf-8 -*- 
#采用标记如“（新函数）”，“（已定义）”

import pygame
import sys
import time


def run_game(): #套用格式
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
		
		
def var_update():        #（更新非静止的对象）
	ship_update()        #更新飞船的参数
	bullet_update()      #更新子弹参数
		
		
def create():   #常数-队列-对象
	global cst
	cst = Cst() 
	global bullets,count
	bullets = {}  #字典（看起来）便于动态操纵
	count = 1 
	global shelfs
	shelfs = []
	global ship
	ship = Ship() 
	global window #特殊对象
	window =Window()
	window.x = 0
	window.y = 0 
	
	def create_shelf(n,x,y): 
		exec("shelf{n} = Shelf({n},{x},{y})".format(n=n,x=x,y=y),
		globals())       #自然坐标
		exec("shelfs.append(shelf{n})".format(n=n),globals())
		
	create_shelf(1,400,250)     
	create_shelf(2,800,500)    
	create_shelf(3,400,750)
	create_shelf(4,800,1000)
	create_shelf(5,400,1250)
	create_shelf(6,800,1500)
	
	cst.ship_speed1 = 2      #船速（被更新函数引用）
	cst.ship_speed2 = cst.ship_speed1 * 2
	cst.bullet_speed = 8     #子弹速度
	cst.bg_color = (0,127,0) #背景色  
	cst.jump_speed = 10  #跳跃初速度
	cst.jump_times = 5  #连跳次数
	cst.g = 0.3    #加速度
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
		                #（以下是5个正交且互斥的组）
		self.position = 0#0-空中；1-地面；11-shelf1；12-shelf2 #
		self.horizontal_move = 0 #此变量为左/右/水平静止
		self.direction = 1		
		
		self.speed = 2 ##这里很尴尬
		
		self.can_jump = 0 #无关紧要，因为第一次落地后被更新
		self.up_speed = 0 #上升速度
		self.run_clock = 0
		self.attack_clock = 0
		                       
		self.key_s = False #s是否按下（这该放在哪？）
		self.key_w = False #w是否按下（这该放在哪？）
		self.d2 = self.direction
		self.quiet = False
		
		self.image = pygame.image.load('images/ship.png')
		self.image2 = pygame.image.load('images/ship2.png')


	def blit(self):  #画船
		if self.direction == 1:
			the_image = self.image
		else:
			the_image = self.image2	
		screen.blit (the_image, 
					(self.x-32 - window.x, 
					 self.y-32 - window.y)
		            )    		


class Bullet(object):
	def __init__(self,x,y,d,a,k = 0): #（中央）坐标，方向，发射记忆
		self.x = x
		self.y = y
		self.d = d
		self.a = a
		self.k = k
		
	def blit(self):  #画子弹
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
	def __init__(self,n,x,y): #顶部中央坐标，自然表示
		self.x = x
		self.y = 800 - y
		self.n = n
				
	def blit(self):  #画平台（所有的blit都依赖window）
		screen.blit(cst.shelf_image,
				   (self.x - 64 - window.x,
					self.y - window.y)
					)
			
	
def check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:#点【关闭】
			sys.exit()					
		elif event.type  ==pygame.KEYDOWN:#动作：【按】
			check_keydown_events(event)
		elif event.type  ==pygame.KEYUP:#动作：【松】
			check_keyup_events(event)
	
	
def check_keydown_events(event):
	if event.key == pygame.K_d:   #【D】
		if ship.run_clock != 0 or ship.speed == cst.ship_speed2:            
			ship.speed = cst.ship_speed2
		else:
			ship.speed = cst.ship_speed1
		ship.direction = 1
		ship.d2 = 1
		ship.horizontal_move = 1
		ship.run_clock = cst.delay
		
	elif event.key == pygame.K_a: #【A】
		if ship.run_clock != 0 or ship.speed == cst.ship_speed2:            
			ship.speed = cst.ship_speed2
		else:
			ship.speed = cst.ship_speed1
		ship.direction = -1
		ship.d2 = -1
		ship.horizontal_move = -1
		ship.run_clock = cst.delay

	elif event.key == pygame.K_j: #【J】
		if ship.attack_clock == 0:
			fire()
			ship.attack_clock = 30
	elif event.key == pygame.K_k: #【k】
		if ship.key_s and ship.position != 0:  #如果不悬空且S被按下			
			ship.position = 0   #失重
			ship.up_speed = 0  
		elif ship.can_jump !=0 :  #空中s/空中非S/着陆非S ：
			ship.position = 0 #悬空
			ship.up_speed = cst.jump_speed #给出向上初速度
			ship.can_jump -= 1 #跳跃次数-1
						
	elif event.key == pygame.K_s: #【S】
		ship.key_s = True
	elif event.key == pygame.K_w: #【W】
		ship.key_w = True
	elif event.key == pygame.K_q: #【Q】
		ship.position = 0
		ship.up_speed = cst.jump_speed * 2 
		ship.can_jump = cst.jump_times
		#~ sys.exit()
	elif event.key == pygame.K_e: #【E】
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
	if event.key == pygame.K_d: #【D】
		if ship.horizontal_move == 1: #如果在往右     #【矛盾状态】的按键交错分析
			ship.horizontal_move = 0
		
	elif event.key == pygame.K_a: #【A】
		if ship.horizontal_move == -1: 
			ship.horizontal_move = 0
				
	elif event.key == pygame.K_s: #【S】被
		ship.key_s = False	
	elif event.key == pygame.K_w: #【W】
		ship.key_w = False	


def make_bullet(n,x,y,d,k = 0):                     #这个版本还没放进去
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
	
	if count == 10000: #防止无限增长。。。
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
				ship.y = shelf.y - 32 #落地
				ship.position = 10 + shelf.n	
				ship.up_speed = cst.jump_speed
				ship.can_jump = cst.jump_times
		else:
			continue
	if ship.y + 32 > 800:#落地检测				
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
	if ship.horizontal_move == 1 : #右移
		ship.x += ship.speed
		if ship.x + 32 - window.x >= 1200 - 100 :
			window.x = ship.x + 32+100-1200    #“如果屏幕不需特别变化”
	elif ship.horizontal_move == -1 :
		ship.x -= ship.speed
		if ship.x - 32 -window.x <= 0 + 100:
			window.x = ship.x - 32-100
		
	if ship.run_clock != 0:
		ship.run_clock -= 1#衰变钟
		
	if ship.attack_clock != 0:
		ship.attack_clock -= 1	
		
	if ship.position == 0 : 
		if ship.up_speed > -50:         #最大坠速
			ship.up_speed -= cst.g
		ship.y -= ship.up_speed
		if ship.position != 16:     #不知有何用
			if ship.y < 400: #跟随视线
				window.y = ship.y - 400
			else:	
				window.y = 0  
		
		is_on(ship,shelfs)		
	
	is_out(ship)	
		
	if ship.position == 16 and window.y > -1500:       #####这非常尴尬，但是我也想不出有何用处
		window.y -= 2
		
						
def bullet_update():   
	global bullets,count
	if not ship.quiet:		#【H】
		bullets_carry = bullets.copy()#翻模法，用原字典的键遍历新字典
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
	screen.fill(cst.bg_color) #清屏
		
	for shelf in shelfs:
		shelf.blit()
		
	ship.blit()                             #飞船上屏
	
	for k in bullets.keys():
		bullets[k].blit()                        #子弹上屏
	
	pygame.display.flip()


run_game()#唯一定义以外的操作	


#    点评：非个性化部分，放在常量中引用。子弹的位置是变量，图像是常量，故bullet类只创建
# 坐标属性（并在创建时要求给出此属性），子弹上屏时引用常量中的图像；飞船只有一艘，无所谓
# 把常量放在何处；shelf（初级）的参数仅包括位置

#理论上多用elif可以减少检测 ，但也不总是。。。（尤其是特殊情况报警）

#情况分析维度：某个键是否按下（每个键都是独立的维度）；某一状态的值（每一状态都是一个维度）
#  技巧：分离出相互独立的维度


#当shelf不断增多，一个一个检测显然不显示，如何把检测限定在少量之内？（试设计算法）

#虽然仅x和y就能决定状态，但这里根据事件来改变状态以减少工作。但是并非所有检测都能避开——
#  譬如落地检测。

#对ship进行跃迁赋值的时候，应如何处理屏幕？（不看改变看关系）

#类不得引用别人的常数
