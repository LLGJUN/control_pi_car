#!/usr/bin/python
# -*-coding: utf-8 -*-

from socket import *
from datetime import *
import time
import binascii
import threading
import pygame

WIDTH=160
HEIGTH=120

pic_width=160
pic_height=120

# 线程1:用来接收客户端发送过来的数据
class myThread_receive_data_from_client(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, clientsocket):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientsocket = clientsocket

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.threadID)
        receive_data(self.clientsocket)
        print("Exiting " + self.threadID)

def recvall(sock,count):
    buf=b''
    while count:
        newbuf=sock.recv(count)
        if not newbuf:
            return None
        buf +=newbuf
        count -= len(newbuf)
    return buf

def receive_data(client_socket):  # 接收到五条数据后推出
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGTH))
    pygame.display.set_caption("web cam")
    pygame.display.flip()
    clock = pygame.time.Clock()  # 计算帧速
    while 1:
        data = recvall(client_socket, pic_width * pic_height * 3)
        # print(len(data))
        camshot = pygame.image.frombuffer(data, (pic_width, pic_height), "RGB")
        img = pygame.transform.scale(camshot, (WIDTH, HEIGTH))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        screen.blit(img, (0, 0))
        pygame.display.update()
        print(clock.get_fps())  # 在终端打印帧速
        clock.tick()


# 线程2：用来发送数据到客户端
class myThread_send_data_from_client(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, clientsocket, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientsocket = clientsocket
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.threadID)
        send_data(self.clientsocket, self.counter)
        print("Exiting " + self.threadID)


def send_data(mysocket, counter):  # 接收到五条数据后推出
    while counter > 0:
        delta = input('请输入舵机角度')
        # mysocket.send('+++message:from server+++')
        mysocket.send(str(delta))
        print('send ok')
        counter -= 1
    mysocket.close()


if __name__ == '__main__':
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(('', 2222))
    server.listen(5)
    print("Waiting for connection...")
    client_socket, client = server.accept()

    myThread_receive = myThread_receive_data_from_client('receive_thread', client_socket)
    myThread_send = myThread_send_data_from_client('send_thread', client_socket, 20)
    myThread_receive.setDaemon(True)
    myThread_receive.start()
    myThread_send.setDaemon(True)
    myThread_send.start()

    threads = []
    # 添加线程到线程列表
    threads.append(myThread_receive)
    threads.append(myThread_send)

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting Main Thread")
    server.close()
