# -*- coding: utf-8 -*- 
#采用标记如“（新函数）”，“（已定义）”

import pygame
import sys

def run_game():
	pygame.init()	                #初始化pygame
	global screen                        #（和下一行）定义screen（窗口）对象
	screen = pygame.display.set_mode((1200,800))
	pygame.display.set_caption("Freecell")       #给框命名
	
	create()#初始化对象（仅参数）	
	while True:
		check_events()#检测输入
		var_update()#更新参数	
		screen_update()#更新显示 
		      
		
		
def var_update():        #（更新非静止的对象）
	ship_update()        #更新飞船的参数
	bullet_update()      #更新子弹参数
		
		
class Ship(object):
	def __init__(self):
		self.x = 32+150
		self.y = 600-32
		                #（以下是5个正交且互斥的组）
		self.position = 0#0-空中；1-地面；11-shelf1；12-shelf2 #
		self.horizontal_move = 0 #此变量为左/右/水平静止
		self.direction = 1		
		self.view = 0 #0-平地模式；1-空中模式
		
		self.can_jump = 0 #无关紧要，因为第一次落地后被更新
		self.up_speed = 0 #上升速度
		self.run_clock = 0
		                       
		self.key_s = False #k是否按下（这该放在哪？）
		
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
	def __init__(self,x,y,d): #子弹：（中央）坐标，方向
		self.x = x
		self.y = y
		self.direction = d
		
	def blit(self):  #画子弹
		if self.direction == 1:
			the_image = constant.bullet_image
		else:
			the_image = constant.bullet_image2
		screen.blit(the_image, 
				   (self.x-4 - window.x, 
					self.y-4 - window.y)
				   )			


class Constant(object): #常数类和常数实例，仅仅为了能用点连接
	pass
constant = Constant() 


class Window(object):#屏幕左上角
	pass
window =Window()
window.x = 0
window.y = 0 

def create_shelf(n,x,y): #（可以考虑单独出一个create类）（形如shelf1）
	exec("shelf"+str(n)+" = Shelf("+str(n)+","+str(x)+","+str(y)+")",
	globals())       #注意，这里为了方便，用了左下基准的坐标（因为是手动设置位置）
		
class Shelf(object):
	def __init__(self,n,x,y): #接收顶部中央坐标，采用【数学表示】（？）
		self.x = x
		self.y = 800 - y
		self.n = n
				
	def blit(self):  #画平台（所有的blit都依赖window）
		screen.blit(constant.shelf_image,
				   (self.x - 64 - window.x,
					self.y - window.y)
					)
			
	def on_detect(self):                                                ##考虑这样一个函数：接收对象和shelf列表，做出判定（设置y，position，u_s和c_j）（需要作为方法吗？）
		if  ship.y + 32 > self.y -5 and \
			ship.y + 32 < self.y  and \
			ship.x > self.x - 96 and\
			ship.x < self.x + 96:
				
				ship.y = self.y - 32 #落地
				
				ship.position = 10 + self.n	
				ship.up_speed = constant.jump_speed
				ship.can_jump = constant.jump_times	
				return True
		else:
			return False			
				
	def out_detect(self):                 #这个也似乎不应该属于shelf类。。。
		if ship.position == 10 + self.n :
			if (ship.x < self.x - 96 or\
					ship.x > self.x + 96):
				ship.up_speed = 0
				ship.position = 0			
		
					
def create():   #创建各种对象（constant是特例）
	global ship
	global bullets,bullets_carry,count
	global shelf1,shelf2,shelf3,shelf4,shelf5,shelf6
	global s_center #屏幕中央
	ship = Ship()                #船
	bullets = {}                        #子弹表（字典）
	count = 1                        #子弹计数
	create_shelf(1,400,250)     #第一个台阶
	create_shelf(2,800,500)    #第二个台阶
	create_shelf(3,400,750)
	create_shelf(4,800,1000)
	create_shelf(5,400,1250)
	create_shelf(6,800,1500)
	
	
	constant.ship_speed = 0.5      #船速（被更新函数引用）
	constant.bullet_speed = 2     #子弹速度
	constant.bg_color = (0,127,0) #背景色  
	constant.jump_speed = 2  #跳跃初速度
	constant.jump_times = 5  #连跳次数
	constant.g = 0.01    #加速度
	constant.bullet_image = pygame.image.load('images/bullet.png')
	constant.bullet_image2 = pygame.image.load('images/bullet2.png')
	constant.shelf_image = pygame.image.load('images/shelf2.png') 
	
	
	
def check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:#点【关闭】
			sys.exit()
					
		elif event.type  ==pygame.KEYDOWN:#动作：【按】
			check_keydown_events(event)
		elif event.type  ==pygame.KEYUP:#动作：【松】
			check_keyup_events(event)
	
def check_keydown_events(event):
	if event.key == pygame.K_d: #【D】被按下时
		ship.direction = 1
		if ship.run_clock != 0:            #右跑衰变钟还在
			constant.ship_speed = 1 #船速：1
		ship.horizontal_move = 1
		ship.run_clock = 300 #右跑衰变钟：300
		
	elif event.key == pygame.K_a: #【A】被按下时
		ship.direction = -1
		if ship.run_clock != 0:	 #左跑衰变钟还在    
			constant.ship_speed = 1 #船速：1
		ship.horizontal_move = -1
		
		ship.run_clock = 300  #左跑衰变钟：300

	elif event.key == pygame.K_j: #【J】被按下时
		fire_bullet()          #开火
	elif event.key == pygame.K_k :	#【k】被按下时
		if ship.key_s and ship.position != 0:  #如果不悬空且S被按下			
			ship.position = 0   #悬空
			ship.up_speed = 0  #向上速度：0
		elif ship.can_jump !=0 :  #空中s/空中非S/着陆非S ：
			ship.position = 0 #悬空
			ship.can_jump -= 1 #跳跃次数-1
			ship.up_speed = constant.jump_speed #给出向上初速度
						
	elif event.key == pygame.K_s: #【S】被按下时
		ship.key_s = True	#开启S状态
	elif event.key == pygame.K_q: #【Q】被按下时
		ship.position = 0
		ship.up_speed = 5	
		#~ sys.exit()
	elif event.key == pygame.K_e: #【E】被按下时
		ship.position = 1
		ship.can_jump = 5#测试用外挂					
		
def check_keyup_events(event):
	if event.key == pygame.K_d: #【D】被松开时
		if not ship.horizontal_move == -1: #如果左跑模式也为关       #【矛盾状态】的按键交错分析
			constant.ship_speed = 0.5 #船速：0.5
			ship.horizontal_move = 0 #右跑模式：关（水平静止模式）
		
	elif event.key == pygame.K_a: #【A】被松开时
		if not ship.horizontal_move == 1: #如果右跑模式也为关 
			ship.horizontal_move = 0  #左跑模式：关
			constant.ship_speed = 0.5	#船速：0.5
	
	elif event.key == pygame.K_s: #【S】被松开时
		ship.key_s = False	#S状态：关
	
def make_bullet(n,x,y,d):
	exec('b'+str(n)+' = Bullet('+str(x)+','+str(y)+','+str(d)+')',
	globals())
	
def add_bullet(n):
	exec("bullets[b"+str(n)+"]=b"+str(n),globals())

def del_bullet(n):
	exec('del(b'+str(n)+')',globals())	
	
def fire_bullet():
	global count
	if ship.direction == 1:
		make_bullet(count,ship.x +32+4,ship.y,1)
	else:
		make_bullet(count,ship.x -32-4,ship.y,-1)
	
	add_bullet(count)
			 
	count += 1
	if count == 10000: #防止无限增长。。。
		count = 0		# 	
	
def var_update():
	ship_update()
	bullet_update()




def ship_update():
	if ship.horizontal_move == 1 :
		ship.x += constant.ship_speed
		if ship.x + 32 - window.x >= 1200 - 100 :
			ship.x  = 1200 - 100 -32 + window.x
			window.x += constant.ship_speed
		
	elif ship.horizontal_move == -1 :
		ship.x -= constant.ship_speed
		if ship.x - 32 -window.x <= 0 + 100:
			ship.x  = 0 + 100 + 32 + window.x
			window.x -= constant.ship_speed
		
			
		
	
	if ship.run_clock != 0:
		ship.run_clock -= 1
	elif ship.run_clock != 0:
		ship.run_clock -= 1	#双击衰变
		
		
	
			
	if ship.position == 0 : #当在空中
		ship.up_speed -= constant.g
		ship.y -= ship.up_speed
		if ship.y < 400:
			window.y = ship.y - 400
		#~ elif ship.y < 800-1500-400 :
			#~ ship.view = 2
		else:	
			window.y = 0  #......
		
		if ship.up_speed <= 0:             #鬼畜互斥做法
			if shelf1.on_detect():
				pass
			elif shelf2.on_detect():
				pass
			elif shelf3.on_detect():
				pass
			elif shelf4.on_detect():
				pass
			elif shelf5.on_detect():
				pass
			elif shelf6.on_detect():
				pass
						
			if ship.y + 32 > 800:#落地检测
				
				ship.y = 800 - 32
				
				ship.position = 1	
				ship.up_speed = constant.jump_speed
				ship.can_jump = constant.jump_times	
		
							
	shelf1.out_detect()
	shelf2.out_detect()
	shelf3.out_detect()
	shelf4.out_detect()
	shelf5.out_detect()
	shelf6.out_detect()
	
	#~ print(ship.y + 32 < 800- 1500,window.y > 800 - 1500 -400)
	#~ if ship.y + 32 < 800- 1500 and window.y >  - 1500 -400:
		#~ print(window.y > - 1500 -400)
	#~ if ship.view == 2:
		#~ window.y -= 1 #;print('here')
		
						
def bullet_update():
	#由于字典在遍历过程中不可进行删除操作，故采用翻模法
	global bullets,bullets_carry,count
	bullets_carry = bullets.copy()
	for k in bullets.keys():
		if bullets_carry[k].direction == 1:
			bullets_carry[k].x += constant.bullet_speed
		else:
			bullets_carry[k].x -= constant.bullet_speed
		if bullets[k].x > (1200-4+window.x) or bullets[k].x < (4+window.x):
			del bullets_carry[k]
	bullets = bullets_carry.copy()
		
def screen_update():
	screen.fill(constant.bg_color) #清屏
	
	shelf1.blit()                 #平台上屏
	shelf2.blit()
	shelf3.blit()
	shelf4.blit()
	shelf5.blit()
	shelf6.blit()
		
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
