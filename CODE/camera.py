import atexit
import io
import os
import picamera
import pygame

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode([128,128], pygame.FULLSCREEN)

camera = picamera.PiCamera()
camera.rotation = 90
camera.resolution = (128, 128)
camera.crop = (0.0, 0.0, 1.0, 1.0)
atexit.register(camera.close)

rgb = bytearray(49152)

# Main loop
while(True):
  stream = io.BytesIO()
  camera.capture(stream, use_video_port=True, format='rgb')

  stream.seek(0)
  stream.readinto(rgb)
  stream.close()

  img = pygame.image.frombuffer(rgb[0:(49152)], (128, 128), 'RGB')
  if img:
      screen.blit(img, (0, 0))

  pygame.display.update()