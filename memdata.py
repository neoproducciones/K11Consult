from collections import OrderedDict

D = OrderedDict()
integrity = bool

loguear = bool
loguear_ms = int

vis = bool
vis_ms = int

usb = bool
db = bool
lcd = bool
encoder = bool


def init():
    global D
    global integrity
    global loguear
    global loguear_ms
    global vis
    global usb
    global db
    global lcd
    global encoder

    tupla = (('KMH', 0), ('ECO', 0), ('RPM', 0), ('TIM', 0), ('TMP', 0), ('OXY', 0), ('BAT', 0), ('INJ', 0),
             ('THL', 0), ('MAF', 0), ('IDL', 0), ('AFS', 0), ('AFL', 0), ('DR0', 0), ('DR1', 0), ('ERR', 0))
    D = OrderedDict(tupla)

    integrity = True

    loguear = False
    loguear_ms = 500
    vis = True

    usb = True
    db = False
    lcd = False
    encoder = False

    print("Variables inicializadas")
