import RPi.GPIO as GPIO
print ("Hola")

#  Encoder pinout:
#  CLK - blue
#  DT - brown
#  SW - gray - pin #11 (GPIO17 - GPIO_GEN0)
#  + - white - pin
#  GND - black - pin #9 (ground)

#  Utilizamos la numeración física de los pines
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    if GPIO.input(11):
        print("Pin 11 estado ALTO")
    else:
        print("Pin 11 estado BAJO")
