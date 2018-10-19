import atexit
import io
import os
import os.path
import fnmatch
import picamera
import pygame
import RPi.GPIO as GPIO

#buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Key A
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Key B
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Key C
GPIO.setup( 6, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Up
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Down
GPIO.setup( 5, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Right
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Press

#load icons
class Icon:
	def __init__(self, name):
	  self.name = name
	  try:
	    self.bitmap = pygame.image.load(iconPath + '/' + name + '.png')
	  except:
	    pass

class Button:

	def __init__(self, rect, **kwargs):
	  self.rect     = rect # Bounds
	  self.color    = None # Background fill color, if any
	  self.iconBg   = None # Background Icon (atop color fill)
	  self.iconFg   = None # Foreground Icon (atop background)
	  self.bg       = None # Background Icon name
	  self.fg       = None # Foreground Icon name
	  self.callback = None # Callback function
	  self.value    = None # Value passed to callback
	  for key, value in kwargs.iteritems():
	    if   key == 'color': self.color    = value
	    elif key == 'bg'   : self.bg       = value
	    elif key == 'fg'   : self.fg       = value
	    elif key == 'cb'   : self.callback = value
	    elif key == 'value': self.value    = value

	def selected(self, pos):
	  x1 = self.rect[0]
	  y1 = self.rect[1]
	  x2 = x1 + self.rect[2] - 1
	  y2 = y1 + self.rect[3] - 1
	  if ((pos[0] >= x1) and (pos[0] <= x2) and
	      (pos[1] >= y1) and (pos[1] <= y2)):
	    if self.callback:
	      if self.value is None: self.callback()
	      else:                  self.callback(self.value)
	    return True
	  return False

	def draw(self, screen):
	  if self.color:
	    screen.fill(self.color, self.rect)
	  if self.iconBg:
	    screen.blit(self.iconBg.bitmap,
	      (self.rect[0]+(self.rect[2]-self.iconBg.bitmap.get_width())/2,
	       self.rect[1]+(self.rect[3]-self.iconBg.bitmap.get_height())/2))
	  if self.iconFg:
	    screen.blit(self.iconFg.bitmap,
	      (self.rect[0]+(self.rect[2]-self.iconFg.bitmap.get_width())/2,
	       self.rect[1]+(self.rect[3]-self.iconFg.bitmap.get_height())/2))

	def setBg(self, name):
	  if name is None:
	    self.iconBg = None
	  else:
	    for i in icons:
	      if name == i.name:
	        self.iconBg = i
	        break

path = '/boot/DCIM/PI'
iconPath = 'icons'
icons = []
buttons = [
    [Button((0, 0, 128, 128), bg='test')]
]

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode([128,128], pygame.FULLSCREEN)

font = pygame.font.Font(None, 45)

camera = picamera.PiCamera()
camera.rotation = 90
camera.resolution = (128, 128)
camera.crop = (0.0, 0.0, 1.0, 1.0)
atexit.register(camera.close)

rgb = bytearray(49152)

for file in os.listdir(iconPath):
  if fnmatch.fnmatch(file, '*.png'):
    icons.append(Icon(file.split('.')[0]))

for s in buttons:        # For each screenful of buttons...
  for b in s:            #  For each button on screen...
    for i in icons:      #   For each icon...
      if b.bg == i.name: #    Compare names; match?
        b.iconBg = i     #     Assign Icon to Button
        b.bg     = None  #     Name no longer used; allow garbage collection
      if b.fg == i.name:
        b.iconFg = i
        b.fg     = None



# Main loop
while(True):

  try:
    Key_A = GPIO.input(21)
    Key_B = GPIO.input(20)
    Key_C = GPIO.input(16)
    Key_U = GPIO.input( 6)
    Key_D = GPIO.input(19)
    Key_L = GPIO.input( 5)
    Key_R = GPIO.input(26)
    Key_P = GPIO.input(13)

  except:
    GPIO.cleanup()

  stream = io.BytesIO()
  camera.capture(stream, use_video_port=True, format='rgb')
  
  stream.seek(0)
  stream.readinto(rgb)
  stream.close()

  img = pygame.image.frombuffer(rgb[0:(49152)], (128, 128), 'RGB')
  if img:
    screen.blit(img, (0, 0))
    screen.blit(font.render('Hello World', True, (255,255,255)), (0, 0))

  for i,b in enumerate(buttons[0]):
    b.draw(screen)

  pygame.display.update()