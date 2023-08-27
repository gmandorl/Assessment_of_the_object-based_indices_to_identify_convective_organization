import numpy as np

from objects import *
import metrics
import matplotlib.pyplot as plt





def run_metrics (image) :

    objects          = make_objects(image)   # class containing regions and polynoms
    pairs_of_objects = make_pairs(objects)   # class containing all pairs of objects


    #plt.imshow(image)
    #plt.imshow(objects.labeled)
    #plt.show()

    image_size = image.size
    domain_length = image.shape[0]
    #print(image.shape)

    dict_org = dict()
    dict_org['area']      = objects.area_skm
    dict_org['number']    = objects.number_of_objects

    dict_org['Iorg']      = metrics.Iorg(pairs_of_objects, image_size=image_size)
    dict_org['Lorg']      = metrics.Lorg(pairs_of_objects,  l_max=2.*image.shape[0],  domain_length=domain_length)


    dict_org['SCAI']      = - metrics.SCAI(pairs_of_objects, image_size=image_size)
    dict_org['MCAI']      = - metrics.MCAI(pairs_of_objects, image_size=image_size)

    dict_org['COP']       = metrics.COP(pairs_of_objects)
    dict_org['ABCOP']     = metrics.ABCOP(pairs_of_objects, image_size=image_size)
    dict_org['ROME']      = metrics.ROME(pairs_of_objects)
    dict_org['MICA']      = metrics.MICA(pairs_of_objects, image_size=image_size)

    dict_org['OIDRA'] = metrics.OIDRA(pairs_of_objects, image_size=image_size)


    # derived variables
    dict_org['mean_area']  = dict_org['area'] / dict_org['number']


    # set to NAN all the metrics when N=1 (23% of the events, 1.5% of the events for C2)
    if dict_org['number'] <= 1 :
        dict_org['Iorg']      = np.nan
        dict_org['Lorg']      = np.nan
        dict_org['SCAI']      = np.nan
        dict_org['MCAI']      = np.nan
        dict_org['COP']       = np.nan
        dict_org['ABCOP']     = np.nan
        dict_org['ROME']      = np.nan
        dict_org['MICA']      = np.nan
        dict_org['OIDRA'] = np.nan






    # store to compare with anomalies and percentiles
    dict_org['area_original']      = dict_org['area']
    dict_org['number_original']    = dict_org['number']

    return dict_org


