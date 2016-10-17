D = dict()
integrity = bool

loguear = bool
loguear_ms = int

vis = bool
vis_ms = int

def init():
    global D
    global integrity
    global loguear
    global loguear_ms
    global vis
    global vis_ms

    D = {'KMH': 0, 'ECO': 0, 'RPM': 0, 'TIM': 0, 'TMP': 0, 'OXY': 0, 'BAT': 0, 'INJ': 0,
         'THL': 0, 'MAF': 0, 'IDL': 0, 'AFS': 0, 'AFL': 0, 'DR0': 0, 'DR1': 0, 'ERR': 0}

    integrity = True

    loguear = False
    loguear_ms = 500
    vis = True
    vis_ms = 500

    print("Variables inicializadas")


