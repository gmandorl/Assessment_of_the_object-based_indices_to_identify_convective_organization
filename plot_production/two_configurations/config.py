

class config  :

    def __init__ (self,
                  property_label,
                  fname_original = 'base',
                  fname_modified = '',
                  axis_label_modified = 'with one additional object',
                  var_to_exclude = [],
                  scale_factor=1,
                  ) :

        self.property_label   = property_label
        self.fname_original   = fname_original
        self.fname_modified   = fname_modified
        self.var_to_exclude = var_to_exclude + ['area_skm', 'area_spg', 'number_original', 'area_original'] + ['mean_area', 'NN_edge', 'NN_center', 'ROME_norm', 'ROME_norm2', 'Iorg_all_events', 'new_index_auto', 'new_index_mutual', 'SCAI2', 'MCAI2', 'D0', 'D2', 'Iorg_recommended', 'Lorg2', 'ROME_delta', 'H', 'Ishape'] # + ['number', 'area']

        self.axis_label_modified         = axis_label_modified
        self.scale_factor = scale_factor








configs = dict()
configs['C1'] = config('C1', fname_modified = 'plusObj',       axis_label_modified = 'with one additional object')
configs['C2'] = config('C2', fname_modified = 'mergedObj',     axis_label_modified = 'when two objects are merged')
configs['C3'] = config('C3', fname_modified = 'shift20',       axis_label_modified = 'test object shifted by 20 pixels')
configs['C4'] = config('C4', fname_modified = 'increased20',   axis_label_modified = 'test object side increased by 20 pixels')


configs['C5'] = config('C7', fname_modified = 'reso3',         axis_label_modified = 'with 3 times reduced resolution')
#configs['C6'] = config('C6', fname_modified = '30min_later',   axis_label_modified = '30 minutes later')
#configs['C6'] = config('C6', fname_modified = '60min_later',   axis_label_modified = '60 minutes later')
#configs['C6'] = config('C6', fname_modified = '90min_later',   axis_label_modified = '90 minutes later')
#configs['C6'] = config('C6', fname_modified = '720min_later',  axis_label_modified = '12 hours later')
configs['C6'] = config('C6', fname_modified ='131400min_later',axis_label_modified = '6 months later')
configs['C7'] = config('C7', fname_modified = 'shift10',       axis_label_modified = 'region shifted by 10 pixels')



