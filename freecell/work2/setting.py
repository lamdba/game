import pygame

class Cst(object): #常数类和常数实例，仅仅为了能用点连接
	pass
cst = Cst()

global s_a,s_b
s_a = 1024
s_b = 768 
global ship
 
global bullets,count
bullets = {}  #字典（看起来）便于动态操纵
count = 1 
global shelfs
shelfs = []


cst.ship_speed1 = 2      
cst.ship_speed2 = cst.ship_speed1 * 2
cst.bullet_speed = 8    
cst.bg_color = (0,127,0) 
cst.jump_speed = 10  #跳跃初速度
cst.jump_times = 5  #连跳次数
cst.g = 0.3    #加速度
cst.bullet_image = pygame.image.load('images/bullet.png')
cst.bullet_image2 = pygame.image.load('images/bullet2.png')
cst.shelf_image = pygame.image.load('images/shelf2.png')
cst.run_delay = 100
