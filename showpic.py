import socket
import os, sys, pygame

WIDTH=160
HEIGTH=120

pic_width=160
pic_height=120

def recvall(sock,count):
    buf=b''
    while count:
        newbuf=sock.recv(count)
        if not newbuf:
            return None
        buf +=newbuf
        count -= len(newbuf)
    return buf

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("web cam")
pygame.display.flip()
# svrsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #UDP传输
svrsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
svrsocket.bind(("", 1234))
svrsocket.listen(1)
client,addr=svrsocket.accept()
clock = pygame.time.Clock()  # 计算帧速
while 1:
    # data, address = svrsocket.recvfrom(80000)
    data=recvall(client,pic_width*pic_height*3)
    # print(len(data))
    camshot = pygame.image.frombuffer(data, (pic_width, pic_height), "RGB")
    img=pygame.transform.scale(camshot, (WIDTH, HEIGTH))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.blit(img , (0, 0))
    pygame.display.update()
    print(clock.get_fps())  # 在终端打印帧速
    clock.tick()