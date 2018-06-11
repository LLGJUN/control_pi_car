import socket
import pygame
from pygame.locals import *
import time


WIDTH=640
HEIGTH=480
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("web cam")
pygame.display.flip()
svrsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
svrsocket.bind(('', 2222))
svrsocket.listen(1)
print('正在侦听客户端连接')
client,addr=svrsocket.accept()
print('接收到一个新连接')
clock = pygame.time.Clock()  # 计算帧速
while 1:
    clock.tick()
    pygame.display.update()
    # 绘制按键执行代码
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_w] or key_pressed[K_UP]:
        time.sleep(0.2)
        if key_pressed[K_w] or key_pressed[K_UP]:
            print('you press up ')
            client.send(b'up')

    if key_pressed[K_s] or key_pressed[K_DOWN]:
        time.sleep(0.2)
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            print('you press down ')
            client.send(b'down')

    if key_pressed[K_a] or key_pressed[K_LEFT]:
        time.sleep(0.2)
        if key_pressed[K_s] or key_pressed[K_LEFT]:
            print('you press left ')
            client.send(b'left')

    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        time.sleep(0.2)
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            print('you press right ')
            client.send(b'right')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()