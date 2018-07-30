# -*- coding: utf-8 -*- 
#���ñ���硰���º��������������Ѷ��壩��

import pygame
import sys
import time

clock = pygame.time.Clock()

class Cst(object): #������ͳ���ʵ��������Ϊ�����õ�����
	pass

def run_game():
	pygame.init()	                #��ʼ��pygame
	global screen                        #������һ�У�����screen�����ڣ�����
	screen = pygame.display.set_mode((1200,800))
	pygame.display.set_caption("Freecell")       #��������
	f = 100
	create()#��ʼ�����󣨽�������	
	while True:
		clock.tick(f)
		check_events()#�������
		var_update()#���²���	
		screen_update()#������ʾ 
		#~ print(ship.run_clock,ship.speed)  
		
		
def var_update():        #�����·Ǿ�ֹ�Ķ���
	ship_update()        #���·ɴ��Ĳ���
	bullet_update()      #�����ӵ�����
		
def create():   #�������ֶ���k��������
	global s_a,s_b
	s_a = 1024
	s_b = 768 
	global ship
	ship = Ship() 
	global bullets,count
	bullets = {}  #�ֵ䣨�����������ڶ�̬����
	count = 1 
	global shelfs
	shelfs = []
	global cst
	cst = Cst() 
   
	create_shelf(1,400,250)     #��һ��̨��
	create_shelf(2,800,500)    #�ڶ���̨��
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
		
class Ship(object):
	def __init__(self):
		self.x = 32+150
		self.y = 600-32
		                #��������5�������һ�����飩
		self.position = 0#0-���У�1-���棻11-shelf1��12-shelf2 #
		self.horizontal_move = 0 #�˱���Ϊ��/��/ˮƽ��ֹ
		self.direction = 1		
		self.view = 0 #0-ƽ��ģʽ��1-����ģʽ
		self.speed = 2 ##���������
		
		self.can_jump = 0 #�޹ؽ�Ҫ����Ϊ��һ����غ󱻸���
		self.up_speed = 0 #�����ٶ�
		self.run_clock = 0
		                       
		self.key_s = False #s�Ƿ��£���÷����ģ���
		self.key_w = False #w�Ƿ��£���÷����ģ���
		
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
	def __init__(self,x,y,d): #�ӵ��������룩���꣬����
		self.x = x
		self.y = y
		self.direction = d
		
	def blit(self):  #���ӵ�
		if self.direction == 1:
			the_image = cst.bullet_image
		elif self.direction == -1:
			the_image = cst.bullet_image2
		elif self.direction == 2:
			the_image = cst.bullet_image3
		elif self.direction == -2:
			the_image = cst.bullet_image4	
			
		screen.blit(the_image, 
				   (self.x-4 - window.x, 
					self.y-4 - window.y)
				   )			






class Window(object):#��Ļ���Ͻ�
	pass
window =Window()
window.x = 0
window.y = 0 

def create_shelf(n,x,y): #�����Կ��ǵ�����һ��create�ࣩ������shelf1��
	exec("shelf"+str(n)+" = Shelf("+str(n)+","+str(x)+","+str(y)+")",
	globals())       #ע�⣬����Ϊ�˷��㣬�������»�׼�����꣨��Ϊ���ֶ�����λ�ã�
		
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
			
	def on_detect(self):                                                ##��������һ�����������ն����shelf�б������ж�������y��position��u_s��c_j������Ҫ��Ϊ�����𣿣�
		if  ship.y + 32 > self.y -5 and \
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
		
					

	
	
	
def check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:#�㡾�رա�
			a = clock.get_fps()
			print(a)
			sys.exit()
					
		elif event.type  ==pygame.KEYDOWN:#������������
			check_keydown_events(event)
		elif event.type  ==pygame.KEYUP:#���������ɡ�
			check_keyup_events(event)
	
def check_keydown_events(event):
	if event.key == pygame.K_d: #��D��������ʱ
		ship.direction = 1
		if ship.run_clock != 0:            #����˥���ӻ���
			ship.speed = cst.ship_speed2 #���٣�1
		ship.horizontal_move = 1
		ship.run_clock = 300 #����˥���ӣ�300
		
	elif event.key == pygame.K_a: #��A��������ʱ
		ship.direction = -1
		if ship.run_clock != 0:	 #����˥���ӻ���    
			ship.speed = cst.ship_speed2 #���٣�1
		ship.horizontal_move = -1
		
		ship.run_clock = 300  #����˥���ӣ�300

	elif event.key == pygame.K_j: #��J��������ʱ
		fire_bullet()          #����
	elif event.key == pygame.K_k :	#��k��������ʱ
		if ship.key_s and ship.position != 0:  #�����������S������			
			ship.position = 0   #����
			ship.up_speed = 0  #�����ٶȣ�0
		elif ship.can_jump !=0 :  #����s/���з�S/��½��S ��
			ship.position = 0 #����
			ship.can_jump -= 1 #��Ծ����-1
			ship.up_speed = cst.jump_speed #�������ϳ��ٶ�
						
	elif event.key == pygame.K_s: #��S��������ʱ
		ship.key_s = True	#����S״̬
	elif event.key == pygame.K_w: #��W��������ʱ
		ship.key_w = True	#����w״̬	
	elif event.key == pygame.K_q: #��Q��������ʱ
		ship.position = 0
		ship.up_speed = 5	
		#~ sys.exit()
	elif event.key == pygame.K_e: #��E��������ʱ
		ship.position = 1
		ship.can_jump = 5#���������	
	elif event.key == pygame.K_UP: #���ϡ�������ʱ
		cst.g += 0.01
		print(cst.g)
		
	elif event.key == pygame.K_DOWN: #���¡�������ʱ
		cst.g -= 0.01
		print(cst.g)
							
		
def check_keyup_events(event):
	if event.key == pygame.K_d: #��D�����ɿ�ʱ
		if not ship.horizontal_move == -1: #�������ģʽҲΪ��       #��ì��״̬���İ����������
			ship.speed = cst.ship_speed1 #���٣�0.5
			ship.horizontal_move = 0 #����ģʽ���أ�ˮƽ��ֹģʽ��
		
	elif event.key == pygame.K_a: #��A�����ɿ�ʱ
		if not ship.horizontal_move == 1: #�������ģʽҲΪ�� 
			ship.horizontal_move = 0  #����ģʽ����
			ship.speed = cst.ship_speed1	#���٣�0.5
	
	elif event.key == pygame.K_s: #��S�����ɿ�ʱ
		ship.key_s = False	#S״̬����
	elif event.key == pygame.K_w: #��W�����ɿ�ʱ
		ship.key_w = False	#w״̬����	
	
def make_bullet(n,x,y,d):                     #����汾��û�Ž�ȥ
	exec('b'+str(n)+' = Bullet('+str(x)+','+str(y)+','+str(d)+')',
	globals())
	
def add_bullet(n):
	exec("bullets[b"+str(n)+"]=b"+str(n),globals())

def del_bullet(n):
	exec('del(b'+str(n)+')',globals())	
	
def fire_bullet():           #��һ�ν���������ӷ���Σ�
	global count
	if ship.key_w and ship.key_s:
		return 0
	elif ship.key_w:
		make_bullet(count,ship.x,ship.y -32-4,2)
	elif ship.key_s:
		make_bullet(count,ship.x,ship.y +32+4,-2)	
	elif ship.direction == 1:
		make_bullet(count,ship.x +32+4,ship.y,1)
	else:
		make_bullet(count,ship.x -32-4,ship.y,-1)
	
	add_bullet(count)
			 
	count += 1
	if count == 10000: #��ֹ��������������
		count = 0		# 	
	
def var_update():
	ship_update()
	bullet_update()




def ship_update():
	if ship.horizontal_move == 1 :
		ship.x += ship.speed
		if ship.x + 32 - window.x >= 1200 - 100 :
			ship.x  = 1200 - 100 -32 + window.x
			window.x += ship.speed
		
	elif ship.horizontal_move == -1 :
		ship.x -= ship.speed
		if ship.x - 32 -window.x <= 0 + 100:
			ship.x  = 0 + 100 + 32 + window.x
			window.x -= ship.speed
		
			
		
	
	if ship.run_clock != 0:
		ship.run_clock -= 1
	elif ship.run_clock != 0:
		ship.run_clock -= 1	#˫��˥��
		
		
	
			
	if ship.position == 0 : #���ڿ���
		if ship.up_speed > -10:
			ship.up_speed -= cst.g
		ship.y -= ship.up_speed
		if ship.position != 16:
			if ship.y < 400:
				window.y = ship.y - 400
		#~ elif ship.y < 800-1500-400 :
			#~ ship.view = 2
			else:	
				window.y = 0  #......
		
		if ship.up_speed <= 0:             #���󻥳�����
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
						
			if ship.y + 32 > 800:#��ؼ��
				
				ship.y = 800 - 32
				
				ship.position = 1	
				ship.up_speed = cst.jump_speed
				ship.can_jump = cst.jump_times	
		
							
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
		
	if ship.position == 16 and window.y > -1500:       #####��ǳ����Σ�������Ҳ�벻���к��ô�
		window.y -= 1
		
						
def bullet_update():                              #�ƺ������÷�����
	#�����ֵ��ڱ��������в��ɽ���ɾ���������ʲ��÷�ģ��
	global bullets,bullets_carry,count
	bullets_carry = bullets.copy()
	for k in bullets.keys():        #��ԭ�ֵ�ļ�����
		if bullets_carry[k].direction == 1:
			bullets_carry[k].x += cst.bullet_speed
		elif bullets_carry[k].direction == -1:
			bullets_carry[k].x -= cst.bullet_speed
		elif bullets_carry[k].direction == 2:
			bullets_carry[k].y -= cst.bullet_speed
		elif bullets_carry[k].direction == -2:
			bullets_carry[k].y += cst.bullet_speed
				                                      #�ƺ����Է���#������ȷ
		if bullets[k].x > (1200-4+window.x) or \
		bullets[k].x < (4+window.x) or \
		bullets[k].y > 800 or\
		bullets[k].y < -1000:
			del bullets_carry[k]
	bullets = bullets_carry.copy()
		
def screen_update():
	screen.fill(cst.bg_color) #����
	
	shelf1.blit()                 #ƽ̨����
	shelf2.blit()
	shelf3.blit()
	shelf4.blit()
	shelf5.blit()
	shelf6.blit()
		
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
