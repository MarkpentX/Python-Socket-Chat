import socket
import threading
import pygame as pg

# pygame setup
user_name = "Mark"
pg.init()
screen = pg.display.set_mode((700, 700))
clock = pg.time.Clock()
running = True
font = pg.font.Font(None, 32)
input_box = pg.Rect(70, 625, 150, 40)
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False
all_messages = []
HOST_IP = "127.0.0.1"
PORT = 65266

text_surface = font.render("\n\n".join(all_messages), True, color_inactive)

def pagination():
    if len(all_messages) > 22:
        all_messages.pop(0)

def receiveResponses(socket):
    global text_surface
    while True:
        try:
            data = client_socket.recv(4096)
            if data:
                all_messages.append(data.decode("utf-8"))
                pagination()
                text_surface = font.render("\n".join(all_messages), True, color_inactive)
        except:
            socket.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP, PORT))

thread = threading.Thread(target=receiveResponses, args=(client_socket,), daemon=True)
thread.start()

while running:
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        if text.replace(" ", "") == "":
                            continue
                        text = f"{user_name}: " + text
                        client_socket.send(text.encode("utf-8"))
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(580, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)

        screen.blit(text_surface, (60, 46))

        pg.display.flip()
        clock.tick(60)



pg.quit()