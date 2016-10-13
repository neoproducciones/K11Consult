import RPi.GPIO as GPIO
print ("Hola")

#  Encoder pinout:
#  CLK - blue - pin #13
#  DT - brown - pin #11
#  SW - gray - pin #12
#  + - white - pin #1
#  GND - black - pin #9 (ground)

#  Usamos numeracion fisica de los pines
GPIO.setmode(GPIO.BOARD)
#  Configuramos cada uno de los pines
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(12):
        print("")
    else:
        print("Pulsado boton")
