


label='TOOCAN'

path = '/bdd/MEGHA_TROPIQUES/MCS/EXPORT/TOOCAN/TOOCAN_v2.06/WESTERNPACIFIC/'
var_name = 'MCS_label'
cut = 0.1 # any system has value greater than 0
cut_reversed = False



# shape (240, 240) if 9.6 x 9.6
lat_min = 9.6
lat_max = 0
lon_min = 140.4
lon_max = 150


import numpy as np

# resolution is reduced to have an image of 120x120
def preprocessing(image) :
    sh = image.shape
    image_to_return = image.reshape(int(sh[0]/2), 2, int(sh[1]/2), 2)
    image_to_return = np.nanmean(image_to_return, axis=(1,3))
    return image_to_return


