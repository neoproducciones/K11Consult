#!/usr/bin/python
# importSingleDial.py

#Copyright (C) 2014 Eilidh Fridlington http://eilidh.fridlington.com

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>



import os
import sys
import time
#import dials as dd
import pygame
from pygame.locals import *
pygame.init()
#dd.Dials(positionX=150)

os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

size = width, height = 1320, 740

pygame.display.set_caption('K11Consult: %s' % __file__)

monitorX = pygame.display.Info().current_w
monitorY = pygame.display.Info().current_h

backgroundFullscreenX = (monitorX / 2) - 340
backgroundFullscreenY = (monitorY / 2) - 340

backgroundWindowedX = (width / 2) - 340
backgroundWindowedY = (height / 2) -340

needleFullscreenX = monitorX / 2
needleFullscreenY = monitorY / 2

needleWindowedX = width / 2
needleWindowedY = height / 2

dial1FullscreenX = monitorX / 2
dial1FullscreenY = backgroundFullscreenY + 535

dial1WindowedX = width / 2
dial1WindowedY = backgroundWindowedY + 535

backgroundX = backgroundWindowedX
backgroundY = backgroundWindowedY

needleX = needleWindowedX
needleY = needleWindowedY

dial1X = dial1WindowedX
dial1Y = dial1WindowedY



screen = pygame.display.set_mode(size)

needle = pygame.image.load("needle.png").convert_alpha()
background = pygame.image.load("dial.png").convert_alpha()

fontFifty = pygame.font.SysFont("Digital-7 Mono", 87)

#surface1 = pygame.Surface((300,300))



#surface1.set_colorkey(0x0000FF)


#screen.fill(0x000000)


RPM_Value = 0


while True:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            sys.exit()
            pygame.quit()

        if event.type is KEYDOWN and event.key == K_q:
            sys.exit()
            pygame.quit()

        if event.type is KEYDOWN and event.key == K_w:
            pygame.display.set_mode(size)

            backgroundX = backgroundWindowedX
            backgroundY = backgroundWindowedY
            needleX = needleWindowedX
            needleY = needleWindowedY
            dial1X = dial1WindowedX
            dial1Y = dial1WindowedY
            screen.fill(0x000000)

        if event.type is KEYDOWN and event.key == K_f:
            pygame.display.set_mode((monitorX,monitorY), FULLSCREEN)

            backgroundX = backgroundFullscreenX
            backgroundY = backgroundFullscreenY
            needleX = needleFullscreenX
            needleY = needleFullscreenY
            dial1X = dial1FullscreenX
            dial1Y = dial1FullscreenY
            screen.fill(0x000000)

    #surface1.fill(0x000000)
    screen.fill(0x000000)


    #dd.Dials(maximumValue=(TEMP_Max_Value/10),endPosition=45,startPosition=-45,dialLabel='Temperature',displayCircle=True,dialType=dd.degree,needleDestination=surface1,needleValue=TEMP_Value,foregroundColour=(255,255,255),backgroundColour=(0,0,81))

    needleNew = pygame.transform.rotozoom(needle, (120 - (RPM_Value  / 33.33)),1)
    #needleNew2 = pygame.transform.rotozoom(needle, (120 - (RPM_Value  / 66.66)),1)
    displayValue = fontFifty.render(("%s" % RPM_Value), 1, (255,0,255))
    labelRect = displayValue.get_rect()
    labelRect.centerx = dial1X
    labelRect.centery = dial1Y

    needle_rect = needleNew.get_rect()
    #screen.blit(background, (surface1X,surface1Y))
    #screen.blit(needleNew, needle_rect)
    #surface1.blit(displayValue, (labelRect))

    screen.blit(background, (backgroundX,backgroundY))
    needle_rect.center = (needleX,needleY)
    #screen.blit(surface1,(surface1X,surface1Y))
    screen.blit(needleNew, needle_rect)
    screen.blit(displayValue, (labelRect))
    #screen.blit(background, (surface1X,surface1Y))

    #time.sleep(0.08)


    if RPM_Value >= 8000:
        counter = 120
        RPM_Value = 0
    else:
        #counter -=3
        RPM_Value += 50

    pygame.display.update()
