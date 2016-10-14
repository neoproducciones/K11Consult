import liquidcrystal_i2c

cols = 20
rows = 4

lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)

i = 0

while True:
    lcd.printline(i, '>>')
    i = i + 1
