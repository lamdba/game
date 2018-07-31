# -*- coding: utf-8 -*- 
import pygame
import sys
 
def run_game():
    pygame.init()   
    global screen
    screen = pygame.display.set_mode((1200,800))#定义screen对象
    pygame.display.set_caption("Freecell")#给框命名
    create()#初始化对象（新函数）（定义了）    
    
    while True:
        check_events()#检测输入（新函数）（定义了）
        var_update()#更新参数（新函数）
        screen_update()#更新显示（新函数）

def var_update():
    ship_update()#更新飞船的参数（新函数）
    bullet_update()#更新子弹参数（新函数）
    
def create():
    global var
    var={'ship':{'position':{'x':0,'y':400},
    'state':{'up':False,'down':False,'left':False,'right':False}},
    'bullet':{'rest':100,'num':0,'data':{},'data_carry':{},'count':0}}
    global constant
    constant={'ship_speed':3,'bullet_speed':5,'bg_color':(0,127,0),
    'ship_image':pygame.image.load('images/ship.bmp'),
    'bullet_image':pygame.image.load('images/bullet.bmp')}

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()          
        elif event.type  ==pygame.KEYDOWN:
            check_keydown_events(event)#（新函数）（已定义）      
        elif event.type  ==pygame.KEYUP:
            check_keyup_events(event)#（新函数）（已定义）
            
def check_keydown_events(event):
    if event.key == pygame.K_RIGHT:
        var['ship']['state']['right'] = True
    if event.key == pygame.K_LEFT:
        var['ship']['state']['left'] = True
    if event.key == pygame.K_UP:
        var['ship']['state']['up'] = True
    if event.key == pygame.K_DOWN:
        var['ship']['state']['down'] = True 
    if event.key == pygame.K_SPACE:
        fire_bullet()#（新函数）（已定义）
        print(var)
    elif event.key == pygame.K_q:
        sys.exit()  

def fire_bullet():#（卧槽。。。）（应该是修改data？）
    
    var['bullet']['data'][var['bullet']['count']]=\
    {'x':var['ship']['position']['x'],
    'y':var['ship']['position']['y']}
    var['bullet']['count'] += 1     
    
def check_keyup_events(event):
    if event.key == pygame.K_RIGHT:
        var['ship']['state']['right'] = False
    if event.key == pygame.K_LEFT:
        var['ship']['state']['left'] = False
    if event.key == pygame.K_UP:
        var['ship']['state']['up'] = False
    if event.key == pygame.K_DOWN:
        var['ship']['state']['down'] = False
                    
def var_update():
    ship_update()#（新函数）（已定义）
    bullet_update()#（新函数）（已定义）
    
def ship_update():
    if var['ship']['state']['right'] :
        var['ship']['position']['x'] += constant['ship_speed']
    if var['ship']['state']['left'] :
        var['ship']['position']['x'] -= constant['ship_speed']
    if var['ship']['state']['up'] :
        var['ship']['position']['y'] -= constant['ship_speed']
    if var['ship']['state']['down'] :
        var['ship']['position']['y'] += constant['ship_speed']
    
def bullet_update(): #示例=> 'data':{1:{x:10,y:20}}
    var['bullet']['data_carry']=var['bullet']['data'].copy()
    for k in var['bullet']['data'].keys():
        var['bullet']['data'][k]['x'] += constant['bullet_speed']
        if var['bullet']['data'][k]['x'] > (1200-10):
            del var['bullet']['data_carry'][k]
    var['bullet']['data']=var['bullet']['data_carry'].copy()    
                                    
    
def screen_update():
    screen.fill(constant['bg_color'])
    
    screen.blit(constant['ship_image'], 
    (var['ship']['position']['x'], var['ship']['position']['y']-32))
    
    for k in var['bullet']['data'].keys():
        screen.blit(constant['bullet_image'], 
    (var['bullet']['data'][k]['x'], var['bullet']['data'][k]['y']))
    
    pygame.display.flip()
    #print(var['bullet']['data'],var['bullet']['data_carry'])   

run_game()#唯一定义以外的操作
