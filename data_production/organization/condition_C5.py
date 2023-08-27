import numpy as np



label      = 'C5'

cases = dict()
cases[f'base'] = 0
for n in range(1,7) :
    cases[f'reso{n}'] = n


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]

    image_to_return = image
    if n>1 :
        # reduce the resolution
        sh = image.shape
        image_to_return = image.reshape(int(sh[0]/n), n, int(sh[1]/n), n)
        image_to_return = np.nanmean(image_to_return, axis=(1,3))

        # define what values have to be considered systems
        image_to_return = np.where(image_to_return>0.5, 1, 0)


    return image_to_return
