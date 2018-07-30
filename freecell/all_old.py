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
		var_update()#���²���	--------|
		screen_update()#������ʾ 	    |
                         #          | 
def var_update():#------------------|
	ship_update()#1.���·ɴ��Ĳ���
	bullet_update()#1.�����ӵ�����
	
	
def create():
	global var,constant
	var={'ship':{'position':{'x':32,
	                         'y':-32-100},   #����*n
				 'state':{'left':False,
						  'right':False,
						  'in_air':True,						  
						  'canjump':3,						  
						  'up_speed':0,
						  'run_right':0,#˫����ʱ
						  'run_left':0}},
		 'bullet':{'rest':100,
				   'data':{},
				   'data_carry':{},
				   'count':1}#count�Ǳ�ţ���������+1
		 #~ 'alien':{'data':{},
		          #~ 'data_carry':{}
					#~ }		   
				   
				   
				   
				   }  
	      ###
	constant={'ship_speed':0.5,      #����*3
			  'bullet_speed':2,
			  'bg_color':(0,127,0),
			  'jump_speed':2,
			  'jump_times':5,
			  'ship_image':pygame.image.load('images/ship.png'),
			  'bullet_image':pygame.image.load('images/bullet.png'),
			  'g':0.01                                                 }


def check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()			
		elif event.type  ==pygame.KEYDOWN:
			check_keydown_events(event)#
		elif event.type  ==pygame.KEYUP:
			check_keyup_events(event)#
			
			
def check_keydown_events(event):
	if event.key == pygame.K_d:
		if var['ship']['state']['run_right'] != 0:
			constant['ship_speed'] = 1
		var['ship']['state']['right'] = True
		var['ship']['state']['left'] = False  #
		var['ship']['state']['run_right'] = 300
		
	if event.key == pygame.K_a:
		if var['ship']['state']['run_left'] != 0:
			constant['ship_speed'] = 1
		var['ship']['state']['left'] = True
		var['ship']['state']['right'] = False #��ֹ���Ҳ���
		var['ship']['state']['run_left'] = 300

	if event.key == pygame.K_j:
		fire_bullet()#���º��������Ѷ��壩
	if event.key == pygame.K_k and var['ship']['state']['canjump']!=0:
		#~ if var['ship']['state']['canjump'] == 3:
			#~ var['ship']['state']['h'] = var['ship']['position']['y']
		var['ship']['state']['in_air'] = True
		var['ship']['state']['canjump'] -= 1
		var['ship']['state']['up_speed'] = 2
	elif event.key == pygame.K_q:
		sys.exit()	
	
	
def check_keyup_events(event):
	if event.key == pygame.K_d:
		var['ship']['state']['right'] = False
		constant['ship_speed'] = 0.5
	if event.key == pygame.K_a:
		var['ship']['state']['left'] = False
		constant['ship_speed'] = 0.5


def fire_bullet():#���Բۡ���������Ӧ�����޸�data����
	var['bullet']['data'][var['bullet']['count']]=\
		{'x':var['ship']['position']['x'] + 32, #ͼƬ��С�������
		 'y':var['ship']['position']['y']}  ##��������Ϊ��ŵ��ӵ�
		 
	var['bullet']['count'] += 1
	if var['bullet']['count'] == 10000: #��ֹ��������������
		var['bullet']['count'] = 0		# 	
	
							
def var_update():
	ship_update()#���º��������Ѷ��壩
	bullet_update()#���º��������Ѷ��壩
	
	
def ship_update():
	if var['ship']['state']['right'] and \
			var['ship']['position']['x'] + 32 < 1200:
		var['ship']['position']['x'] += constant['ship_speed']
	if var['ship']['state']['left'] and \
			var['ship']['position']['x'] -32 > 0:
		var['ship']['position']['x'] -= constant['ship_speed']
	
	if var['ship']['state']['run_right'] != 0:
		var['ship']['state']['run_right'] -= 1
	if var['ship']['state']['run_left'] != 0:
		var['ship']['state']['run_left'] -= 1	#˫��˥��
			
	if var['ship']['state']['in_air'] :
		var['ship']['position']['y'] -= var['ship']['state']['up_speed']
		var['ship']['state']['up_speed'] -= constant['g']
		if var['ship']['position']['y'] + 32 > 800:#��ؼ��
			var['ship']['position']['y'] = 800 - 32
			var['ship']['state']['in_air'] = False
			var['ship']['state']['up_speed'] = constant['jump_speed']
			var['ship']['state']['canjump'] = constant['jump_times']
	
	
	#~ if var['ship']['state']['in_air']:
		#~ var['ship']['state']['up_speed'] -= constant['g']
	#~ elif var['ship']['position']['y'] +32 >= 1200:
		#~ var['ship']['position']['y'] +32 = 1200
		#~ var['ship']['state']['in_air']= False
				
			
	
	
def bullet_update(): #ʾ��=> 'data':{1:{x:10,y:20}}  #��Ч��
	#�����ֵ��ڱ��������в��ɽ���ɾ���������ʲ��÷�ģ��
	var['bullet']['data_carry']=var['bullet']['data'].copy()
	for k in var['bullet']['data'].keys():
		var['bullet']['data'][k]['x'] += constant['bullet_speed']
		if var['bullet']['data'][k]['x'] > (1200-10):
			del var['bullet']['data_carry'][k]
	var['bullet']['data']=var['bullet']['data_carry'].copy()
	
	
def screen_update():
	screen.fill(constant['bg_color']) #����
	
	screen.blit (constant['ship_image'], 
				(var['ship']['position']['x']-32, 
				 var['ship']['position']['y']-32)
		        )                                 #�ɴ�����
	
	for k in var['bullet']['data'].keys():
		screen.blit(constant['bullet_image'], 
				   (var['bullet']['data'][k]['x']-4, 
					var['bullet']['data'][k]['y']-4)
				   )                              #�ӵ�����
	
	pygame.display.flip()


run_game()#Ψһ��������Ĳ���
