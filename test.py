import RPi.GPIO as GPIO
from time import sleep

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
counter = 0

while True:
    if not GPIO.input(sw):
        print("Pulsado")
    else:
        print("")

    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if clkState != clkLastState:
        if dtState != clkState:
            counter -= 1
            print("Izquierda")
        else:
            counter += 1
            print("Derecha")
        print counter
    clkLastState = clkState
    sleep(0.01)
