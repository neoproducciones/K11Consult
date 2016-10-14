import RPi.GPIO as GPIO
from time import sleep

import liquidcrystal_i2c

cols = 20
rows = 4

lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)


#  Encoder pinout:
#  CLK - blue - pin #13
#  DT - brown - pin #11
#  SW - gray - pin #12
#  + - white - pin #1
#  GND - black - pin #9 (ground)

clk = 13
dt = 11
sw = 12

#  Usamos numeracion fisica de los pines
GPIO.setmode(GPIO.BOARD)
#  Configuramos cada uno de los pines
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clkLastState = GPIO.input(clk)
linea_actual = 0
lectura_falsa = False

while True:
    if not GPIO.input(sw):
        print("Pulsado")

    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if clkState != clkLastState:
        if dtState != clkState:
            lcd.printline(linea_actual, ' ')
            print "Izquierda"
            if linea_actual > 0:
                linea_actual -= 1
            else:
                linea_actual = 3
            lcd.printline(linea_actual, '>')
        else:
            print "Derecha"
            if linea_actual < 3:
                linea_actual += 1
            else:
                linea_actual = 0
        print (linea_actual)
    clkLastState = clkState
    #  sleep(0.01)
    sleep(0.005)
