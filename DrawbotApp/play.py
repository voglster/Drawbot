import pygame, thorpy
import serial.tools.list_ports


def clearScreen(screen):
    screen.fill((255,255,255))

def getComPorts():
    for name,_,_ in serial.tools.list_ports.comports():
        yield name

def getFirstComPort():
    return next(getComPorts())

def assertComPorts():
    if not getFirstComPort():
        thorpy.launch_blocking_alert("No comport found please restart after connecting machine\n")
        pygame.quit()


pygame.init()

screen = pygame.display.set_mode((1024,768))
clearScreen()
assertComPorts()

#draw ui

#dropdown with comports
#connected button/disconnectect button
#status label (connected?)
#jog buttons
#reset home buttons



rect = pygame.Rect((0, 0, 50, 50))
rect.center = screen.get_rect().center
clock = pygame.time.Clock()

pygame.draw.rect(screen, (255,0,0), rect)
pygame.display.flip()

#declaration of some ThorPy elements ...
slider = thorpy.SliderX.make(100, (12, 35), "My Slider")
button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
box = thorpy.Box.make(elements=[slider,button])
#we regroup all elements on a menu, even if we do not launch the menu
menu = thorpy.Menu(box)
#important : set the screen as surface for all elements
for element in menu.get_population():
    element.surface = screen
#use the elements normally...
box.set_topleft((100,100))
box.blit()
box.update()

playing_game = True
while playing_game:
    clock.tick(60)
    pygame.draw.rect(screen, (255,255,255), rect) #delete old
    pygame.display.update(rect)
    rect.move_ip((1,0))
    pygame.draw.rect(screen, (255,0,0), rect) #drat new
    pygame.display.update(rect)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing_game = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pygame.draw.rect(screen, (255,255,255), rect) #delete old
                pygame.display.update(rect)
                rect.move_ip((-5,0))
                pygame.draw.rect(screen, (255,0,0), rect) #drat new
                pygame.display.update(rect)
        menu.react(event) #the menu automatically integrate your elements

pygame.quit()

