# -*- coding: utf-8 -*- 
#采用标记如“（新函数）”，“（已定义）”

import pygame
import sys
 
def run_game():
	pygame.init()	
	global screen
	screen = pygame.display.set_mode((1200,800))#定义screen（窗口）对象
	pygame.display.set_caption("Freecell")#给框命名
	
	create()#初始化对象（仅参数）	
	while True:
		check_events()#检测输入
		var_update()#更新参数	--------|
		screen_update()#更新显示 	    |
                         #          | 
def var_update():#------------------|
	ship_update()#1.更新飞船的参数
	bullet_update()#1.更新子弹参数
	
	
def create():
	global var,constant
	var={'ship':{'position':{'x':32,
	                         'y':-32-100},   #变量*n
				 'state':{'left':False,
						  'right':False,
						  'in_air':True,						  
						  'canjump':3,						  
						  'up_speed':0,
						  'run_right':0,#双击计时
						  'run_left':0}},
		 'bullet':{'rest':100,
				   'data':{},
				   'data_carry':{},
				   'count':1}#count是编号，等于总数+1
		 #~ 'alien':{'data':{},
		          #~ 'data_carry':{}
					#~ }		   
				   
				   
				   
				   }  
	      ###
	constant={'ship_speed':0.5,      #常量*3
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
		var['ship']['state']['right'] = False #防止左右不能
		var['ship']['state']['run_left'] = 300

	if event.key == pygame.K_j:
		fire_bullet()#（新函数）（已定义）
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


def fire_bullet():#（卧槽。。。）（应该是修改data？）
	var['bullet']['data'][var['bullet']['count']]=\
		{'x':var['ship']['position']['x'] + 32, #图片大小相关数字
		 'y':var['ship']['position']['y']}  ##增加索引为编号的子弹
		 
	var['bullet']['count'] += 1
	if var['bullet']['count'] == 10000: #防止无限增长。。。
		var['bullet']['count'] = 0		# 	
	
							
def var_update():
	ship_update()#（新函数）（已定义）
	bullet_update()#（新函数）（已定义）
	
	
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
		var['ship']['state']['run_left'] -= 1	#双击衰变
			
	if var['ship']['state']['in_air'] :
		var['ship']['position']['y'] -= var['ship']['state']['up_speed']
		var['ship']['state']['up_speed'] -= constant['g']
		if var['ship']['position']['y'] + 32 > 800:#落地检测
			var['ship']['position']['y'] = 800 - 32
			var['ship']['state']['in_air'] = False
			var['ship']['state']['up_speed'] = constant['jump_speed']
			var['ship']['state']['canjump'] = constant['jump_times']
	
	
	#~ if var['ship']['state']['in_air']:
		#~ var['ship']['state']['up_speed'] -= constant['g']
	#~ elif var['ship']['position']['y'] +32 >= 1200:
		#~ var['ship']['position']['y'] +32 = 1200
		#~ var['ship']['state']['in_air']= False
				
			
	
	
def bullet_update(): #示例=> 'data':{1:{x:10,y:20}}  #有效！
	#由于字典在遍历过程中不可进行删除操作，故采用翻模法
	var['bullet']['data_carry']=var['bullet']['data'].copy()
	for k in var['bullet']['data'].keys():
		var['bullet']['data'][k]['x'] += constant['bullet_speed']
		if var['bullet']['data'][k]['x'] > (1200-10):
			del var['bullet']['data_carry'][k]
	var['bullet']['data']=var['bullet']['data_carry'].copy()
	
	
def screen_update():
	screen.fill(constant['bg_color']) #清屏
	
	screen.blit (constant['ship_image'], 
				(var['ship']['position']['x']-32, 
				 var['ship']['position']['y']-32)
		        )                                 #飞船上屏
	
	for k in var['bullet']['data'].keys():
		screen.blit(constant['bullet_image'], 
				   (var['bullet']['data'][k]['x']-4, 
					var['bullet']['data'][k]['y']-4)
				   )                              #子弹上屏
	
	pygame.display.flip()


run_game()#唯一定义以外的操作
