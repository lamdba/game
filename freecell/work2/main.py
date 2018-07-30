# -*- coding: utf-8 -*- 
#���ñ���硰���º��������������Ѷ��壩��

import pygame
import sys
import time

#~ from classes import *
from create import *
from classes import *

clock = pygame.time.Clock()


ship = Ship()
def run_game():
	pygame.init()	                #��ʼ��pygame
	pygame.display.set_caption("Freecell")       #��������
	global screen                        #������һ�У�����screen�����ڣ�����
	screen = pygame.display.set_mode((1200,800))
	
	#;print('here')#��ʼ�����󣨽�������
	
	create()
	
	while True:
		clock.tick(100)
		check_events()#�������
		var_update()#���²���	
		screen_update()#������ʾ 
		  
		
		
def var_update():        #�����·Ǿ�ֹ�Ķ���
	ship_update()        #���·ɴ��Ĳ���
	bullet_update()      #�����ӵ�����
		
#~ def create():   #�������ֶ���k��������
	
	 
   
def create_shelf(n,x,y): #�����Կ��ǵ�����һ��create�ࣩ������shelf1��
	exec("shelf"+str(n)+" = Shelf("+str(n)+","+str(x)+","+str(y)+")",
	globals())       #ע�⣬����Ϊ�˷��㣬�������»�׼�����꣨��Ϊ���ֶ�����λ�ã�	 
		
   		

def create():
	create_shelf(1,400,250)     #��һ��̨��
	create_shelf(2,800,500)    #�ڶ���̨��
	create_shelf(3,400,750)
	create_shelf(4,800,1000)
	create_shelf(5,400,1250)
	create_shelf(6,800,1500)
	global ship
	ship = Ship();print('here')







class Window(object):#��Ļ���Ͻ�
	pass
window =Window()
window.x = 0
window.y = 0 


		
		
		
					

	
	
	
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
		ship.run_clock = cst.run_delay #����˥���ӣ�300
		
	elif event.key == pygame.K_a: #��A��������ʱ
		ship.direction = -1
		if ship.run_clock != 0:	 #����˥���ӻ���    
			ship.speed = cst.ship_speed2 #���٣�1
		ship.horizontal_move = -1
		
		ship.run_clock = cst.run_delay  #����˥���ӣ�300

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
	elif event.key == pygame.K_q: #��Q��������ʱ
		ship.position = 0
		ship.up_speed = cst.jump_speed * 2	
		#~ sys.exit()
	elif event.key == pygame.K_e: #��E��������ʱ
		ship.position = 1
		ship.can_jump = 5#���������					
		
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
		
						
def bullet_update():
	#�����ֵ��ڱ��������в��ɽ���ɾ���������ʲ��÷�ģ��
	global bullets,bullets_carry,count
	bullets_carry = bullets.copy()
	for k in bullets.keys():
		if bullets_carry[k].direction == 1:
			bullets_carry[k].x += cst.bullet_speed
		else:
			bullets_carry[k].x -= cst.bullet_speed
		if bullets[k].x > (1200-4+window.x) or bullets[k].x < (4+window.x):
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
		
	ship.blit(screen,window)                             #�ɴ�����
	
	for k in bullets.keys():
		bullets[k].blit(screen,window)                        #�ӵ�����
	
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
