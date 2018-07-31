# -*- coding: utf-8 -*-
#采用标记如“（新函数）”，“（已定义）”

import pygame
import time


"""
哲学：数据结构为主，尽量不使用实例调用方法（用类调用）

"""

class Ship:
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
        self.tp = False
        self.tp_bullet = 0
        #self.wind = 0
        self.invincible_clock = 0

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
    
    
    def tp():
        ship.x = ship.tp_bullet.x
        ship.y = ship.tp_bullet.y
        ship.tp = False
        ship.position = 0
        ship.up_speed = 0
        del bullets[ship.tp_bullet.n]
    
    
    def tp_fire():
        if ship.key_w and ship.key_s:
            return 0
        elif ship.key_w:
            make_bullet(count,ship.x,ship.y -32-9,2,2)
        elif ship.key_s:
            make_bullet(count,ship.x,ship.y +32+9,-2,2)
        elif ship.direction == 1:
            make_bullet(count,ship.x +32+4,ship.y,1,2)
        else:
            make_bullet(count,ship.x -32-4,ship.y,-1,2)
        ship.tp_bullet = eval("b{count}".format(count=count-1))
    
    
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
    

class Bullet:
    def __init__(self,n,x,y,d,a,k = 0): #（中央）坐标，方向，发射记忆
        self.n = n
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
        if self.k == 1:
            if self.d == 1:
                self.x += (self.x - self.a + 2)/16
            elif self.d == -1:
                self.x -= (self.a - self.x + 2)/16
            elif self.d == 2:
                self.y -= (self.a - self.y + 2)/16
            elif self.d == -2:
                self.y += (self.y - self.a + 2)/16
        else:
            if self.d == 1:
                self.x += cst.bullet_speed
            elif self.d == -1:
                self.x -= cst.bullet_speed
            elif self.d == 2:
                self.y -= cst.bullet_speed
            elif self.d == -2:
                self.y += cst.bullet_speed







class Shelf:
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
            exit()
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
    elif event.key == pygame.K_e: #【E】
        ship.position = 1
        ship.can_jump = 5

    elif event.key == pygame.K_h: #【H】
        if ship.quiet:
            ship.quiet = False
        else:
            ship.quiet = True

    elif event.key == pygame.K_i: #【I】
        trident()
        ship.up_speed = 0
        ship.invincible_clock = 30

    elif event.key == pygame.K_l: #【L】
        if not (ship.key_w and ship.key_s):
            if ship.tp:
                ship.tp = False
                tp()
            else:
                ship.tp = True
                tp_fire()


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
    if d in [1,-1]:
        a = x
    else:
        a = y

    bullets.append(Bullet(n,x,y,d,a,k))




if "app":   # 伪类
    def run_game():
        pygame.init()
        pygame.display.set_caption("Freecell")
        screen = pygame.display.set_mode((1200,800))
        clock = pygame.time.Clock()

        cst,var = create()
        while True:
            check_events(cst,var)
            var_update(cst,var)
            screen_update(cst,var,screen)
            clock.tick(50)

    def create():   #常数-队列-对象
        cst={ship_speed1:2,
             ship_speed2:4,
             bullet_speed:8,
             bg_color:(0,127,0),
             jump_speed:8,
             jump_times:5,
             g = 0.2,
             bullet_image = pygame.image.load('images/bullet.png'),
             bullet_image2 = pygame.image.load('images/bullet2.png'),
             bullet_image3 = pygame.image.load('images/bullet3.png'),
             bullet_image4 = pygame.image.load('images/bullet4.png'),
             bullet_image5 = pygame.image.load('images/bullet5.png'),
             bullet_image6 = pygame.image.load('images/bullet6.png'),
             bullet_image7 = pygame.image.load('images/bullet7.png'),
             bullet_image8 = pygame.image.load('images/bullet8.png'),
             shelf_image = pygame.image.load('images/shelf2.png'),
             
             delay = 30,
        }

        var={ship:Ship(),
             bullets:{},
             shelfs:[Shelf(1,400,250),
                     Shelf(2,800,500),
                     Shelf(3,400,750),
                     Shelf(4,800,1000),
                     Shelf(5,400,1250),
                     Shelf(6,800,1500),
                    ],
             
             window:{x:0,y:0},
            }
        return (cst,var)



    def var_update(cst,var):        #（更新非静止的对象）
        ship_update(cst,var)        #更新飞船的参数
        bullet_update(cst,var)      #更新子弹参数
    


    def ship_update(cst,var):
    
        if ship.run_clock != 0:
            ship.run_clock -= 1#衰变钟
    
        if ship.attack_clock != 0:
            ship.attack_clock -= 1
    
        if ship.invincible_clock != 0: #【I】
            ship.invincible_clock -= 1
        else:
            if ship.horizontal_move == 1 : #右移
                ship.x += ship.speed
            elif ship.horizontal_move == -1 :
                ship.x -= ship.speed
            if ship.x + 32 - window.x >= 1200 - 100 :
                window.x = ship.x + 32+100-1200    #“如果屏幕不需特别变化”
            elif ship.x - 32 -window.x <= 0 + 100:
                window.x = ship.x - 32-100
    
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
    
    
    def bullet_update(cst,var):
        global bullets,count
        if not var['ship'].quiet:      #【H】
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
                    if bullets_carry[k].k == 2:
                        ship.tp = False
                    del bullets_carry[k]
            bullets = bullets_carry.copy()


    def screen_update(cst,var):
        screen.fill(cst.bg_color) #清屏
    
        for shelf in shelfs:
            shelf.blit()
    
        ship.blit()                             #飞船上屏
    
        for k in bullets.keys():
            bullets[k].blit()                        #子弹上屏
    
        pygame.display.flip()
    
    

if __name__ == "__main__":
    run_game()


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
