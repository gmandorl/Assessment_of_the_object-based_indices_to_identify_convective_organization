import numpy as np
from objects import *
import copy
from scipy import ndimage

label      = 'C1'

cases = dict()
cases['base']    = 0
cases['plusObj'] = 1


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]


    if n!=0 :
        filled_im         = ndimage.binary_fill_holes(image).astype(int)  # fill holes


        # find an empty position where to add the additional convective pixel
        numb_in_3x3 = filled_im[0:-2, :-2] + filled_im[2:, :-2] + filled_im[1:-1, :-2] + \
                      filled_im[0:-2,1:-1] + filled_im[2:,1:-1] + filled_im[1:-1,1:-1] + \
                      filled_im[0:-2,2:  ] + filled_im[2:,2:  ] + filled_im[1:-1,2:  ]

        idx_edges = np.argwhere(numb_in_3x3 == 0)
        N = idx_edges.shape[0]

        if idx_edges.shape[0]==0 : return image
        else :
            nth_candidate = np.random.randint(N)
            idx1 = idx_edges[nth_candidate][0]+1
            idx2 = idx_edges[nth_candidate][1]+1

            image[idx1,idx2]=1




    return image
