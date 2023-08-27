import numpy as np
from objects import *
import copy
import matplotlib.pyplot as plt
from scipy import ndimage


label      = 'C2'

cases = dict()
cases['base']    = 0
cases['mergedObj'] = 1


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]

    if n==0 : return image

    extended_im                = np.zeros((image.shape[0]+2, image.shape[1]+2))
    extended_im[1:-1,1:-1]     = image
    extended_im                = ndimage.binary_fill_holes(extended_im).astype(int)  # fill holes
    objects_original           = make_objects(extended_im)   # class containing regions and polynoms
    pairs_of_objects_original  = make_pairs(objects_original)   # class containing all pairs of objects

    numb_original       = objects_original.number_of_objects

    distances = copy.deepcopy(pairs_of_objects_original.distance_edges)
    np.fill_diagonal(distances, np.nan)

    #### condition to add a point ####
    if numb_original<2 or np.nanmin(distances)!= 1 :
        return image

    labeled = objects_original.labeled


    # find an empty position where to add the additional convective pixel
    empty_close_to_two_objects_1 = extended_im[0:-2,1:-1] + extended_im[2:,1:-1] - extended_im[1:-1,1:-1]
    empty_close_to_two_objects_2 = extended_im[1:-1,0:-2] + extended_im[1:-1,2:] - extended_im[1:-1,1:-1]
    empty_weighted_1 = labeled[0:-2,1:-1] - labeled[2:,1:-1]
    empty_weighted_2 = labeled[1:-1,0:-2] - labeled[1:-1,2:]
    candidates = np.where((empty_close_to_two_objects_1 == 2) & (empty_weighted_1!=0), 1, 0) +                 np.where((empty_close_to_two_objects_2 == 2) & (empty_weighted_2!=0), 1, 0)


    #add the new convective pixel
    candidate_indices = np.where(candidates>0)
    image_to_return = image
    image_to_return[candidate_indices[0][0],candidate_indices[1][0]] =1


    return image_to_return
