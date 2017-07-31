#!/usr/bin/env python

import pygrib
import numpy as np
import pandas as pd
import datetime

def grib_to_df():
    #grib = pygrib.open("/home/iic/Escritorio/TLsTxcTOsoSYmtRzKDl0e75I4HAjqDApvbc.grb")
    #grib = pygrib.open('/media/sf_Compartida/test_20170301.grib')
    grib = pygrib.open('/media/sf_Compartida/Historicoprueba2.grib')

    variables = []
    dates = []
    for grb in grib:
        print(grb)
        if not grb.name in variables:
            variables.append(grb.name)
        if not grb.analDate in dates:
            dates.append(grb.analDate)
    print(variables)
    print(dates)
    print(variables[0]+ str(grib[1].values.shape))
    dicc = {}

    for date in dates:

        dicc[date] = {}
        data = grib.select(analDate=date)
        for grb in data:
            values = grb.values
            lat, lon = grb.latlons()
            time = date + datetime.timedelta(hours=grb['endStep'])
            variable = grb['name']
            if not time in dicc[date]:
                dicc[date][time] = {}
            for i in range(lat.shape[0]):
                for j in range(lat.shape[1]):
                    coords = lat[i][j], lon[i][j]
                    key = variable + str(coords)
                    dicc[date][time][key] = values[i][j]


    for k in dicc:
        file = open('dataframe_'+str(k)+'.txt', 'w')
        df = pd.DataFrame.from_dict(dicc[k],orient='index')
        file.write(str(df))
        file.close()

    #df = pd.DataFrame(dicc[0][0],dicc[0].keys(),variables)
    #print(df)

if __name__ == '__main__':
    grib_to_df()