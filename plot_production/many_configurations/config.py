

class config  :

    def __init__ (self,
                  property_label,
                  cases,
                  xlabel = 'base',
                  fname_original = 'base',
                  var_to_exclude = ['number', 'area_original', 'number_original', 'mean_area'],
                  ) :

        self.cases   = cases
        self.labels  = [cases[x]['label']  for x in cases]
        self.fname_original = fname_original
        self.var_to_exclude = var_to_exclude
        self.xlabel         = xlabel






cases_C3 = {f'shift{n}':        {'label': f'+{n}'}          for n in range(1,39,2) }
cases_C4 = {f'increased{n}':    {'label': f'+{n}'}          for n in range(1,20,1) }
cases_C5 = {f'reso{n}':         {'label': f'x{n}'}          for n in range(2,7)    }
cases_C6 = {f'{30*n}min_later': {'label': f'+{int(n/2)} h'} for n in range(1,25)   }
cases_C7 = {f'shift{n}':        {'label': f'+{n}'}          for n in range(1,20,1) }







configs = dict()
configs['C3'] = config( 'C3', cases = cases_C3, xlabel='shift of the test object'        )
configs['C4'] = config( 'C4', cases = cases_C4, xlabel='increase of the test object'     )
configs['C5'] = config( 'C5', cases = cases_C5, xlabel='scale factor of the grid boxes'  )
configs['C6'] = config( 'C6', cases = cases_C6, xlabel='time delay'                      )
configs['C7'] = config( 'C7', cases = cases_C7, xlabel='shift of region considered'      )
