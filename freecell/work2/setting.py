import pygame

class Cst(object): #������ͳ���ʵ��������Ϊ�����õ�����
	pass
cst = Cst()

global s_a,s_b
s_a = 1024
s_b = 768 
global ship
 
global bullets,count
bullets = {}  #�ֵ䣨�����������ڶ�̬����
count = 1 
global shelfs
shelfs = []


cst.ship_speed1 = 2      
cst.ship_speed2 = cst.ship_speed1 * 2
cst.bullet_speed = 8    
cst.bg_color = (0,127,0) 
cst.jump_speed = 10  #��Ծ���ٶ�
cst.jump_times = 5  #��������
cst.g = 0.3    #���ٶ�
cst.bullet_image = pygame.image.load('images/bullet.png')
cst.bullet_image2 = pygame.image.load('images/bullet2.png')
cst.shelf_image = pygame.image.load('images/shelf2.png')
cst.run_delay = 100
