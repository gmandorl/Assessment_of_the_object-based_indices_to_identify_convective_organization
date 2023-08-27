import numpy as np



label      = 'C4'

cases = dict()
cases[f'base'] = 0
for n in range(1,21) :
    cases[f'increased{n}'] = n


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]

    sh    = image.shape
    to_add = np.zeros((sh[0],50))

    # add a (n+2)x(n+2) box in an additional space on the right of the image
    to_add[int((sh[0])/2-1)-n:int((sh[0])/2+1)+n, 24-n:26+n] = 1

    image_to_return = np.concatenate((image, to_add), axis=1)
    return image_to_return
