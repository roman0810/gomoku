import glfw
from OpenGL.GL import *
from math import *  
from enum import Enum

window = None

#размер экрана в пикселях
size = 640

#отступ фигур от клеток
marge = 0.01
#доля поля от половины экрана
scale = 1.5
#координаты курсора
step = [-scale/16,-scale/16]

#точки определяющие место фигур
circ = []
cros = []

class tit(Enum):
    EMPT = 0
    CIRC    = 1
    CROS    = 2
  

table = []
for i in range(15):
    table.append([])
    for j in range(15):
        table[i].append(tit.EMPT)


def main():
    global window

    if not glfw.init():
        return
    window = glfw.create_window(size, size, "Lab1", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    while not glfw.window_should_close(window):
        display()
    glfw.destroy_window(window)
    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            step[0] += scale/16
        if key == 263:
            step[0] -= scale/16
        if key == 265: #up
        	step[1] += scale/16
        if key == 264: #down
        	step[1] -= scale/16
        if key == glfw.KEY_SPACE:
            circ.append([step[0]+scale/32,step[1]+scale/32])
            set_circ(step[0], step[1])
            # ai_move()
        if key == 257:  #enter (проверка отрисоки крестиков)
            cros.append([step[0] , step[1]])



def display():
    global size , step

    glClear(GL_COLOR_BUFFER_BIT) #очистка буффера цвета
    glLoadIdentity()

    x = step[0]
    y = step[1]

    glBegin(GL_LINES) #начало постройки полигона по точкам
    for i in range(-8,8):
        glColor3f(1, 1, 1)
        glVertex2f(i/16*scale,-0.5*scale)
        glVertex2f(i/16*scale,0.5*scale-scale/16)

        glVertex2f(-0.5*scale, i/16*scale)
        glVertex2f(0.5*scale-scale/16, i/16*scale)

    glColor3f(1, 0, 0)
    glVertex2f(x,y)
    glVertex2f(scale/16+x,y)

    glVertex2f(scale/16+x,y)
    glVertex2f(scale/16+x,scale/16+y)

    glVertex2f(scale/16+x,scale/16+y)
    glVertex2f(x,scale/16+y)

    glVertex2f(x,scale/16+y)
    glVertex2f(x,y)

    glEnd()

    #отрисовка ноликов
    for point in circ:
        posx, posy = point[0],point[1]   
        sides = 32    
        radius = scale/32 - marge/2
        glBegin(GL_LINE_STRIP)
        glColor3f(0,1,0)
        for i in range(70):    
            cosine= radius * cos(i*pi/sides) + posx    
            sine  = radius * sin(i*pi/sides) + posy    
            glVertex2f(cosine,sine)

        glEnd()

    #отрисовка крестиков
    for point in cros:
        glBegin(GL_LINES)
        glColor3f(1,1,0)

        glVertex2f(point[0] + marge,point[1] + marge)
        glVertex2f(point[0]+scale/16 - marge,point[1]+scale/16 -marge)

        glVertex2f(point[0]+marge,point[1]+scale/16-marge)
        glVertex2f(point[0]+scale/16-marge,point[1]+marge)


        glEnd()


    glfw.swap_buffers(window)
    glfw.poll_events()




# def ai_move():


def set_circ(x , y):
    x += 8*scale/16
    y += 8*scale/16

    x = x//(scale/16)
    y = y//(scale/16)
    
    table[int(x)][int(y)] = tit.CIRC

def set_cros(x , y):
    x += 8*scale/16
    y += 8*scale/16

    x = x//(scale/16)
    y = y//(scale/16)
    
    table[int(x)][int(y)] = tit.CROS

main()
















