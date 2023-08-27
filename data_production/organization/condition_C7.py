import numpy as np



label      = 'C7'

cases = dict()
cases[f'base'] = 0
for n in range(1,21) :
    cases[f'shift{n}'] = n


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]


    image_to_return = image[10:110, 0+n:100+n]
    return image_to_return
