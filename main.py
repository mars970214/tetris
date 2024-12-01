# tetris
# T轉向問題
import pygame
import os
import random
import time
import math

game = {
    "title" : "Tetris",
    "FPS"   : 60,
    "WIDTH" : 500,
    "HEIGHT": 642,
    "block_name": "I J L O S T Z",
    "direction" : 0,
    "score" : 0,
    "start_time": time.time()
}
die_blocks = pygame.sprite.Group()
die_blocks_list = []
store_block =[]

# 遊戲初始化 and 創建視窗
pygame.init()
screen = pygame.display.set_mode((game["WIDTH"], game["HEIGHT"]))
pygame.display.set_caption(game["title"])
clock = pygame.time.Clock()
icon_img = pygame.image.load(os.path.join("img", "icon.png")).convert_alpha()
icon_mini_img = pygame.transform.scale(icon_img, (32, 32))
icon_mini_img.set_colorkey((0, 0, 0))
pygame.display.set_icon(icon_mini_img)

pygame.mixer.music.load(os.path.join("sound", "bgm.mp3"))
pygame.mixer.music.set_volume(0.1)

# 載入圖片
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
bottom_img = pygame.image.load(os.path.join("img/block", "bottom.png")).convert()

block_imgs = []
for i in game["block_name"].split(" "):
    block_imgs.append(pygame.image.load(os.path.join("img/block", f"{i}.png")).convert_alpha()) # convert_alpha 可以使圖片有透明度
show_block_imgs = []
for i in game["block_name"].split(" "):
    show_block_imgs.append(pygame.image.load(os.path.join("img", f"{i}.png")).convert_alpha())

font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

class Block(pygame.sprite.Sprite):
    #需改成位置公式 方便套入
    def __set_locate(self, number, type):
        x = 0
        y = 0
        if type == "I":
            if game["direction"] == 0 or game["direction"] == 2:
                x = number
                y = 2 - game["direction"]/2
            else:
                x = 1 + (game["direction"]-1)/2
                y = number
        elif type == "O":
            if number > 1:
                x -= 2
                y = 1
            x += number +1
        elif type == "J" or type == "L":
            if number == 0:
                if (type == "J" and game["direction"] == 0) or (type == "L" and game["direction"] == 2):
                    y = 1
                elif (type == "J" and game["direction"] == 1) or (type == "L" and game["direction"] == 3):
                    x = 1
                elif (type == "J" and game["direction"] == 2) or (type == "L" and game["direction"] == 0):
                    x = 2
                    y = 1
                elif (type == "J" and game["direction"] == 3) or (type == "L" and game["direction"] == 1):
                    x = 1
                    y = 2
            else:
                if game["direction"] == 0 or game["direction"] == 2:
                    x = number -1
                    y = (game["direction"] -2)*(-1)
                else:
                    x = game["direction"] -1
                    y = number -1
        elif type == "T":
            if number == 0:
                x = 1
                y = 1
            else:
                if game["direction"] == 0 or game["direction"] == 2:
                    x = number -1
                    if number %2 != 0:
                        y = 1
                    else:
                        y = game["direction"]
                else:
                    y = number -1
                    if number %2 != 0:
                        x = 1
                    else:
                        x = (game["direction"] -3)*(-1)
        else:
            if number == 0:
                x = 1
                y = 1
            elif number == 3:
                if game["direction"] == 0:
                    x = 1
                    y = 2
                elif game["direction"] == 1:
                    y = 1
                elif game["direction"] == 2:
                    x = 1
                else:
                    x = 2
                    y = 1
            elif type == "S":
                if game["direction"] == 0:
                    if number == 1:
                        x = 2
                        y = 1
                    elif number == 2:
                        y = 2
                elif game["direction"] == 1:
                    if number == 1:
                        x = 1
                        y = 2
                elif game["direction"] == 2:
                    if number == 1:
                        y = 1
                    elif number == 2:
                        x = 2
                else:
                    if number == 1:
                        x = 1
                    elif number == 2:
                        x = 2
                        y = 2
            elif type == "Z":
                if game["direction"] == 0:
                    if number == 1:
                        y = 1
                    elif number == 2:
                        x = 2
                        y = 2
                elif game["direction"] == 1:
                    if number == 1:
                        x = 1
                    elif number == 2:
                        y = 2
                elif game["direction"] == 2:
                    if number == 1:
                        x = 2
                        y = 1
                else:
                    if number == 1:
                        x = 1
                        y = 2
                    elif number == 2:
                        x = 2


        return (x*32, y*32)
    
    def __init__(self, type, number):
        pygame.sprite.Sprite.__init__(self)
        self.number = number
        self.type = type
        self.image = block_imgs[game["block_name"].split(" ").index(type)]
        self.rect = self.image.get_rect()
        self.movex = self.__set_locate(number, type)[0]
        self.movey = self.__set_locate(number, type)[1]
        self.rect.centerx = (32*3 + 16) + self.movex + 2
        self.rect.bottom = self.movey - 64
    
    def turn(self):
        # self.image = pygame.transform.rotate(self.image, 270)
        self.rect.centerx += self.__set_locate(self.number, self.type)[0] - self.movex
        self.rect.bottom += self.__set_locate(self.number, self.type)[1] - self.movey

        self.movex = self.__set_locate(self.number, self.type)[0]
        self.movey = self.__set_locate(self.number, self.type)[1]

        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def drop(self, d):
        if d == 0:#down
            self.rect.bottom += 32
        elif d == 1:#up
            self.rect.bottom -= 32
        elif d == 2:#left
            self.rect.centerx -= 32
        elif d == 3:#right
            self.rect.centerx += 32

    # 未刪除乾淨 可能導致卡頓
    def delete(self, y):
        if self.rect.bottom == y:
            self.rect.centerx = -99
            self.rect.bottom = -9
        if self.rect.bottom < y:
            self.rect.bottom += 32

class Test_Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = block_imgs[game["block_name"].find("I")]
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.bottom = 0

class Bottom_Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bottom_img
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.bottom = 0

class Show_Block(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = show_block_imgs[game["block_name"].split(" ").index(type)]
        self.rect = self.image.get_rect()
        self.rect.centerx = -99
        self.rect.bottom = -99

all_block = pygame.sprite.Group()
all_blocks = []
show_next_blocks = pygame.sprite.Group()
show_next_blocks_list = []
store_blocks = pygame.sprite.Group()
store_blocks_list = []
bottom_blocks = pygame.sprite.Group()
bottom_blocks_list = []
for i in game["block_name"].split(" "):
    Bb = Show_Block(i)
    show_next_blocks_list.append(Bb)
    show_next_blocks.add(Bb)
for i in game["block_name"].split(" "):
    Bb = Show_Block(i)
    store_blocks_list.append(Bb)
    store_blocks.add(Bb)
for i in range(4):
    Bb = Bottom_Block()
    bottom_blocks_list.append(Bb)
    bottom_blocks.add(Bb)

next_block = game["block_name"].split(" ")
def summon_block(c=0):
    global all_block
    global all_blocks
    # 消除檢查
    locy = []
    for i in die_blocks_list:
        locy.append(i.rect.bottom)
    for i in range(21):
        if locy.count(i*32) >= 10:
            game["score"] += 50
            for j in die_blocks_list:
                j.delete(i*32)



    global next_block # 將next_block變為全局變數(避免區域錯誤)
    game["direction"] = 0
    if c:
        if len(store_block) == 1:
            btype = store_block.pop()
        else:
            btype = next_block.pop()
        for i in store_blocks_list:
            i.rect.centerx = -90
            i.rect.bottom = -90
            if i.type == all_blocks[0].type:
                i.rect.centerx = 420
                i.rect.bottom = 555
        store_block.append(all_blocks[0].type)
        for i in all_blocks:
            i.rect.bottom = 999
        all_block.empty()
        all_blocks = []
    else:
        btype = next_block.pop()

    for i in die_blocks_list:
        if i.rect.bottom < 0:
            global running
            running = False

    if len(next_block) == 1:
        a = game["block_name"].split(" ")
        random.shuffle(a)
        for i in a:
            next_block.append(i)
        
    for i in range(4):
        block = Block(btype, i)
        all_block.add(block)
        all_blocks.append(block)

        die_blocks.add(block)
        die_blocks_list.append(block)
    show_bottom()

    for i in show_next_blocks_list:
        i.rect.centerx = -90
        i.rect.bottom = -90
        if i.type == next_block[-1]:
            i.rect.centerx = 420
            i.rect.bottom = 384
     

tb = pygame.sprite.Group()
test_block = Test_Block()
tb.add(test_block)

timed = time.time()
end_time = 0

# 遊戲迴圈
running = True

def test(d):
    hit = False
    xL = 900
    xR = 0
    yu = 900
    yd = 0
    
    for j in all_blocks:
        if d == 0:
            test_block.rect.centerx = j.rect.centerx
            test_block.rect.bottom = j.rect.bottom +32

        elif d == 1:
            test_block.rect.centerx = j.rect.centerx
            test_block.rect.bottom = j.rect.bottom -32

        elif d == 2:
            test_block.rect.centerx = j.rect.centerx -32
            test_block.rect.bottom = j.rect.bottom

        elif d == 3:
            test_block.rect.centerx = j.rect.centerx +32
            test_block.rect.bottom = j.rect.bottom
            
        if j.rect.bottom +32 > yd:
            yd = j.rect.bottom +32
        if j.rect.bottom -32 < yu:
            yu = j.rect.bottom -32
        if j.rect.centerx -32 < xL:
            xL = j.rect.centerx -32
        if j.rect.centerx +32 > xR:
            xR = j.rect.centerx +32

        unhit = pygame.sprite.spritecollideany(test_block, all_block)
        hits = pygame.sprite.spritecollideany(test_block, die_blocks)
        if hits != None and unhit == None:
            hit = True
        # 當 兩方塊重疊會 hits != None and unhit == None 解決方法參照轉向x z

    if d == 0 and not(hit) and yd <= 640:
        return True
    elif d == 1 and not(hit) and yu <= 640 and xL >= 0 and xR < 320:
        return True
    elif d == 2 and not(hit) and xL >= 0:
        return True
    elif d == 3 and not(hit) and xR < 320:
        return True
    else:
        return False

def show_bottom():
    drop = 900
    y = 0
    i = 0
    while i < 4:
        bottom_blocks_list[i].rect.centerx = all_blocks[i].rect.centerx
        bottom_blocks_list[i].rect.bottom = all_blocks[i].rect.bottom
        y = 0
        for j in range(20):
            bottom_blocks_list[i].rect.bottom += 32
            unhit = pygame.sprite.spritecollideany(bottom_blocks_list[i], all_block)
            hit = pygame.sprite.spritecollideany(bottom_blocks_list[i], die_blocks)
            if (hit != None and unhit == None) or bottom_blocks_list[i].rect.bottom > 640:
                break
            else:
                y += 32
        if y < drop:
            drop = y
        i += 1
    i = 0
    while i < 4:
        bottom_blocks_list[i].rect.bottom = all_blocks[i].rect.bottom + drop
        i += 1

summon_block()
pygame.mixer.music.play(-1)
while running:
    clock.tick(game["FPS"])
    
    if end_time == 0 and not(test(0)):
        end_time = time.time()

    if end_time != 0 and time.time() > end_time + 1.5:
        end_time = 0
        all_block.empty()
        all_blocks = []
        summon_block()
    drop_speed = 1.5-0.01*(time.time() - game["start_time"])
    if end_time == 0 and time.time() > timed + drop_speed:
        if test(0):
            game["score"] += 1
            for i in all_blocks:
                i.drop(0)
        timed = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        elif event.type == pygame.KEYDOWN:
            end_time = 0
            if event.key == pygame.K_x:
                hit = False
                for i in all_blocks:
                    game["direction"] += 1
                    if game["direction"] == 4:
                        game["direction"] = 0
                    for j in all_blocks:
                        j.turn()

                    test_block.rect.centerx = i.rect.centerx
                    test_block.rect.bottom = i.rect.bottom

                    game["direction"] -= 1
                    if game["direction"] == -1:
                        game["direction"] = 3
                    for j in all_blocks:
                        j.turn()
                    
                    unhits = pygame.sprite.spritecollideany(test_block, all_blocks)
                    hits = pygame.sprite.spritecollideany(test_block, die_blocks)
                    
                    if (hits != None and unhits == None) or test_block.rect.centerx < 0 or test_block.rect.centerx >= 320 or test_block.rect.bottom >= 640:
                        hit = True
                        break

                game["direction"] += 1
                if game["direction"] == 4:
                    game["direction"] = 0
                for j in all_blocks:
                    j.turn()
                if hit:
                    if test(1):
                        for i in all_blocks:
                            i.drop(1)
                    else:
                        game["direction"] -= 1
                        if game["direction"] == -1:
                            game["direction"] = 3
                        for i in all_blocks:
                            i.turn()
            elif event.key == pygame.K_z:
                hit = False
                for i in all_blocks:
                    game["direction"] -= 1
                    if game["direction"] == -1:
                        game["direction"] = 3
                    for j in all_blocks:
                        j.turn()

                    test_block.rect.centerx = i.rect.centerx
                    test_block.rect.bottom = i.rect.bottom
                    
                    game["direction"] += 1
                    if game["direction"] == 4:
                        game["direction"] = 0
                    for j in all_blocks:
                        j.turn()
                    
                    unhits = pygame.sprite.spritecollideany(test_block, all_blocks)
                    hits = pygame.sprite.spritecollideany(test_block, die_blocks)
                    
                    if (hits != None and unhits == None) or test_block.rect.centerx < 0 or test_block.rect.centerx >= 320 or test_block.rect.bottom >= 640:
                        hit = True
                        break

                game["direction"] -= 1
                if game["direction"] == -1:
                    game["direction"] = 3
                for j in all_blocks:
                    j.turn()
                if hit:
                    if test(1):
                        for i in all_blocks:
                            i.drop(1)
                    else:
                        game["direction"] += 1
                        if game["direction"] == 4:
                            game["direction"] = 0
                        for i in all_blocks:
                            i.turn()
            elif event.key == pygame.K_a:
                hit = False
                for i in all_blocks:
                    game["direction"] += 2
                    if game["direction"] > 3:
                        game["direction"] -= 4
                    for j in all_blocks:
                        j.turn()

                    test_block.rect.centerx = i.rect.centerx
                    test_block.rect.bottom = i.rect.bottom
                    
                    game["direction"] += 2
                    if game["direction"] > 3:
                        game["direction"] -= 4
                    for j in all_blocks:
                        j.turn()
                    
                    unhits = pygame.sprite.spritecollideany(test_block, all_blocks)
                    hits = pygame.sprite.spritecollideany(test_block, die_blocks)
                    
                    if (hits != None and unhits == None) or test_block.rect.centerx < 0 or test_block.rect.centerx >= 320 or test_block.rect.bottom >= 640:
                        hit = True
                        break

                game["direction"] += 2
                if game["direction"] > 3:
                    game["direction"] -= 4
                for j in all_blocks:
                    j.turn()
                if hit:
                    if test(1):
                        for i in all_blocks:
                            i.drop(1)
                    else:
                        game["direction"] += 2
                        if game["direction"] > 3:
                            game["direction"] -= 4
                        for i in all_blocks:
                            i.turn()
            elif event.key == pygame.K_c:
                end_time = 0
                summon_block(1)
                
            elif event.key == pygame.K_LEFT:
                if test(2):
                    for i in all_blocks:
                        i.drop(2)
            elif event.key == pygame.K_RIGHT:
                if test(3):
                    for i in all_blocks:
                        i.drop(3)
            elif event.key == pygame.K_DOWN:
                if test(0):
                    game["score"] += 3
                    for i in all_blocks:
                        i.drop(0)
            elif event.key == pygame.K_SPACE:
                game["score"] += 2
                for k in range(20):
                    if test(0):
                        for i in all_blocks:
                            i.drop(0)
                    else:
                        break
                end_time = 0
                all_block.empty()
                all_blocks = []
                summon_block()
        show_bottom()

    # 物體更新
    all_block.update()

    # 畫面顯示
    screen.fill((0,0,0))
    screen.blit(background_img, (0,0))
    draw_text(screen, str(f"分數:{game['score']}"), 32, 416, 32)
    with open("log/score.log", "r") as file:
        fi = int(file.read())
    if game["score"] > fi:
        fi = game["score"]
        with open("log/score.log", "w") as file:
            file.write(str(fi))
    draw_text(screen, str("最高分數:"), 32, 416, 116)
    draw_text(screen, str(f"{fi}"), 32, 416, 166)
    draw_text(screen, str("下一個方塊"), 32, 416, 260)
    draw_text(screen, str("儲存的方塊"), 32, 416, 416)
    bottom_blocks.draw(screen)
    die_blocks.draw(screen)
    show_next_blocks.draw(screen)
    store_blocks.draw(screen)
    pygame.display.update()

screen.fill((0,0,0))
draw_text(screen, "Game Over", 90, game["WIDTH"]/2, 0)
draw_text(screen, str(f"分數:{game['score']}"), 90, game["WIDTH"]/2, 110)
with open("log/score.log", "r") as file:
    fi = file.read()
draw_text(screen, str("最高分數:"), 90, game["WIDTH"]/2, 200)
draw_text(screen, str(f"{fi}"), 90, game["WIDTH"]/2, 290)
pygame.display.update()
time.sleep(3)

pygame.quit()