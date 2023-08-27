import numpy as np
import math
import scipy as sp
from scipy import special
import copy
import datetime
import matplotlib.pyplot as plt
from skimage.measure import shannon_entropy

#######################################################################################
######################################### I_org #######################################
#######################################################################################

def Iorg(pairs_of_objects, image_size = 1):
    """Iorg according to [Tompkins et al. 2017]"""

    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan



    #dist_min = np.nanmin(pairs_of_objects.distance_centroids, axis=1)
    dist_min = pairs_of_objects.dist_min


    # the theoretical Weibull-distribution for n particles
    u_dist_min, u_dist_min_counts = np.unique(dist_min, return_counts=True)
    lamda = pairs_of_objects.number_of_objects / image_size
    weib_cdf = 1 - np.exp(- lamda * math.pi * u_dist_min**2)


    # the CDF from the actual data
    data_cdf = np.cumsum(u_dist_min_counts / np.sum(u_dist_min_counts))

    # compute the integral between Weibull CDF and data CDF
    weib_cdf = np.append(0, weib_cdf   )
    weib_cdf = np.append(   weib_cdf, 1)
    data_cdf = np.append(0, data_cdf   )
    data_cdf = np.append(   data_cdf, 1)


    integral = np.sum ( data_cdf[:-1] * ( weib_cdf[1:] - weib_cdf[:-1] ) ) # DO NO USE trapz ! trapz return always >0.5 for N=2
    return integral



#######################################################################################
######################################### L_org #######################################
#######################################################################################

def Lorg(pairs_of_objects, l_max = 2, domain_length=1):
    """Lorg according to [Biagioli et al. 2023]
    A more general implementation at https://github.com/giobiagioli/organization_indices"""


    number_of_objects = pairs_of_objects.objects.number_of_objects
    if number_of_objects<2 :
        return np.nan

    #l_max = domain_length
    centroids_x          = pairs_of_objects.centroids_x
    centroids_y          = pairs_of_objects.centroids_y
    distance_centroids_x = np.abs(pairs_of_objects.distance_centroids_x)
    distance_centroids_y = np.abs(pairs_of_objects.distance_centroids_y)
    distance_centroids   = pairs_of_objects.distance_centroids

    size = 2*np.maximum(distance_centroids_x, distance_centroids_y)

    values = np.unique(size, return_counts=False)


    # 0 has to be there
    bins = values
    bins = np.linspace(0,l_max,100)  # 100 bins give results very close to Biagioli's code
    Nbins = bins.shape[0]


    size_tile  = np.tile(size, (Nbins,1,1))
    values_tile = np.rollaxis(np.tile(bins, (number_of_objects,number_of_objects,1)), 2)

    hist = np.where(size_tile<=values_tile,1,0)
    cum_hist = np.sum(hist, axis=2) - 1 # -1 to remove the auto-distance


    weights = np.ones(Nbins)
    centroids_x_tile = np.tile(centroids_x, (Nbins,1))
    centroids_y_tile = np.tile(centroids_y, (Nbins,1))



    xmax = np.minimum(centroids_x_tile + bins[:,None]/2., domain_length)
    xmin = np.maximum(centroids_x_tile - bins[:,None]/2., 0)
    ymax = np.minimum(centroids_y_tile + bins[:,None]/2., domain_length)
    ymin = np.maximum(centroids_y_tile - bins[:,None]/2., 0)

    weights = (ymax-ymin)*(xmax-xmin) / bins[:,None] / bins[:,None]
    weights = 1./weights
    weights = np.where(weights>1, weights, 1)




    cum_hist = weights*cum_hist

    Besag_obs = domain_length * np.sqrt(np.mean(cum_hist, axis=1) / (number_of_objects-1) )/ l_max


    Lorg =  np.sum ( Besag_obs[:-1] * ( bins[1:] - bins[:-1] ) / l_max  ) - 0.5
    Lorg = Lorg * ((number_of_objects-1)/number_of_objects)**0.5   # correction due to the low number of objects


    return Lorg






#######################################################################################
###############################  Radar Organization MEtric  ###########################
#######################################################################################


def ROME(pairs_of_objects):
    """ROME according to [Retsch et al. 2020]"""

    if   pairs_of_objects.objects.number_of_objects<1  :  return np.nan
    elif pairs_of_objects.objects.number_of_objects==1 :  return pairs_of_objects.objects.area_skm

    area_1 = pairs_of_objects.objects.areas
    area_2 = pairs_of_objects.objects.areas[:,None] #transpose the vector

    large_area = np.fmax(area_1, area_2).astype(float)
    small_area = np.fmin(area_1, area_2).astype(float)

    np.fill_diagonal(large_area, np.nan)
    np.fill_diagonal(small_area, np.nan)


    return np.nanmean(large_area + np.fmin(small_area, (small_area / pairs_of_objects.distance_edges)**2))



#######################################################################################
#################################  Information Entropy H  #############################
#######################################################################################


def H(image, pairs_of_objects):
    """Information Entropy according to [Sullivan et al. 2019]"""

    if   pairs_of_objects.objects.number_of_objects<2  :  return np.nan

    domain_length = max(image.shape[0], image.shape[1])
    return shannon_entropy(image) / domain_length




#######################################################################################
########################## Convective Organization Potential ##########################
#######################################################################################

def COP(pairs_of_objects):
    """The Convective Organization Potential according to [White et al. 2018]"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    diameter_1 = pairs_of_objects.objects.diameters
    diameter_2 = pairs_of_objects.objects.diameters[:,None] #transpose the vector
    v = np.array(0.5 * (diameter_1 + diameter_2) / pairs_of_objects.distance_centroids)
    return np.nansum(v) / pairs_of_objects.number_of_combinations




#######################################################################################
#################### Area Based Convective Organization Potential #####################
#######################################################################################

def ABCOP(pairs_of_objects, image_size=1):
    """The Area Based Convective Organization Potential according to [ Jin et al. 2022]"""
    if pairs_of_objects.objects.number_of_objects<1 :
        return np.nan
    if pairs_of_objects.objects.number_of_objects==1 :
        density = pairs_of_objects.objects.areas[0] / image_size
        return math.pi**0.5 / 2 * density / (2-density**0.5)

    areas_1 = pairs_of_objects.objects.areas
    areas_2 = pairs_of_objects.objects.areas[:,None]


    diameter_1 = pairs_of_objects.objects.diameters
    diameter_2 = pairs_of_objects.objects.diameters[:,None] #transpose the vector
    distances = np.maximum(1, pairs_of_objects.distance_centroids - 0.5 * (diameter_1 + diameter_2) )
    np.fill_diagonal(distances, np.nan)

    V_area = 0.5 * (areas_1 + areas_2) / distances / image_size**0.5
    ABCOP = np.sum(np.nanmax(V_area, axis=0))

    return ABCOP




#######################################################################################
######################  Simple Convective Aggregation Metric  #########################
#######################################################################################

def SCAI(pairs_of_objects, image_size = 1):
    """SCAI according to [Tobin et al. 2013]"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan


    d_0  = np.exp( 0.5 * np.nansum( np.log(pairs_of_objects.distance_centroids)) / pairs_of_objects.number_of_combinations )
    SCAI = pairs_of_objects.number_of_objects / (image_size**1.5) * d_0 * 1000 * 2 # *2 comes from Nmax

    return SCAI



#######################################################################################
######################  Modified Convective Aggregation Metric  #######################
#######################################################################################

def MCAI(pairs_of_objects, image_size = 1):
    """MCAI according to [Xu et al. 2018]"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    diameter_1 = pairs_of_objects.objects.diameters
    diameter_2 = pairs_of_objects.objects.diameters[:,None] #transpose the vector

    d2 = np.maximum(0, pairs_of_objects.distance_centroids - 0.5 * (diameter_1 + diameter_2) )
    d2 = np.nanmean(d2)
    L = math.sqrt(image_size)


    MCAI = pairs_of_objects.objects.number_of_objects * d2 * 1000 * 2 / L**3
    return MCAI



#######################################################################################
##################  Morphological Index of Convective Aggregation  ####################
#######################################################################################

def MICA(pairs_of_objects, image_size = 1):
    """MICA according to [Kadoya et Masunaga 2018]"""


    if pairs_of_objects.objects.number_of_objects==0 :
        return np.nan

    objects = pairs_of_objects.objects
    regions = objects.regions

    min_row = np.min([r.bbox[0]     for r in regions])
    min_col = np.min([r.bbox[1]     for r in regions])
    max_row = np.max([r.bbox[2]     for r in regions])
    max_col = np.max([r.bbox[3]     for r in regions])

    Acls = (max_row - min_row) * (max_col - min_col)
    MICA = 1.* ( objects.area_skm / Acls ) * ( image_size - Acls ) / image_size

    return MICA



#######################################################################################
######################################## I_shape ######################################
#######################################################################################

def Ishape(pairs_of_objects, image_size = 1):
    """Ishape according to [Pscheidt et al. 2019]"""

    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    areas       = pairs_of_objects.objects.areas
    perimeters  = pairs_of_objects.objects.perimeter

    Ishape =  np.sum (areas**0.5 / perimeters) /  pairs_of_objects.objects.number_of_objects


    return Ishape


#######################################################################################
######################################### EXTRA #######################################
#######################################################################################


def OIDRA (pairs_of_objects, image_size = 1):

    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    objects   = pairs_of_objects.objects
    areas     = pairs_of_objects.objects.areas
    distances = pairs_of_objects.distance_edges


    L       = math.sqrt(image_size)
    weights = 1 - np.sqrt( 1.4142135623730951 * distances / L )
    areas   = areas / np.sum(areas)


    # compute A_i * A*j * weight_ij
    coefficients = weights
    coefficients = coefficients * areas
    coefficients = (coefficients.T*areas.T).T


    new_index  = np.nansum(coefficients) + np.sum(areas*areas)


    return  new_index


