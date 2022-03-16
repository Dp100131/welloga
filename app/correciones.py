# Imports

import lasio

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

#Volumen de arcilla

def Vshh(df, GR, n, columns):
    
    if (n==1):

        df['Vsh'] = 5

    elif (n==2):

        df['Vsh_GRcorr'] = 5

    vsh = []

    GRmin = df[GR].min()
    GRmax = df[GR].max()
    GRindex = columns.index(GR)

    for i in range(0, df.shape[0], 1):

        GRsand = df.iloc[i, GRindex]
        vshcal = ((GRsand - GRmin)/(GRmax - GRmin))

        if vshcal < 0:

            vshcal = 0

        elif vshcal > 1:

            vshcal = 1
    
        vsh.append(vshcal.round(4))

    if (n==1):

        df['Vsh'] = vsh

    elif (n==2):
        
        df['Vsh_GRcorr'] = vsh

# Correción GR 1

def correctionHolesizeMudweight_corr(df, dmud, cali, dsonda, GR, c, unit_cali, columns):

    df['GRcorr'] = 0
    GRindex = columns.index(GR)
    Calindex = columns.index(cali)
    grcorr = []

    print(type(dsonda))
    print(type(c))
    print(c)
    print(dsonda)


    print((dsonda == 3.375) and (c == 'centered'))

    if (dsonda == 3.375) and (c == 'centered'):

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(25.4*2))-((2.54*dsonda)/(2)))

            elif unit_cali == 'INCHES':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(2))-((2.54*dsonda)/(2)))

            cf = ((0.0039)*(t**2)) - ((0.0378)*t) + 1.0558

            grcorr.append((df.iloc[i, GRindex])*cf)
            
    elif (dsonda == 3.375) and (c == 'eccentered'):

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(25.4*2))-((2.54*dsonda)/(2)))

            elif unit_cali == 'INCHES':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(2))-((2.54*dsonda)/(2)))

            
            cf = ((-0.0005)*(t**2)) + ((0.0393)*t) + 0.7912

            grcorr.append((df.iloc[i, GRindex])*cf)

    elif (dsonda == 1.6875) and (c == 'centered'):

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(25.4*2))-((2.54*dsonda)/(2)))

            elif unit_cali == 'INCHES':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(2))-((2.54*dsonda)/(2)))

            
            cf = ((0.0016)*(t**2)) + ((0.0158)*t) + 0.7986

            grcorr.append((df.iloc[i, GRindex])*cf)

    elif (dsonda == 1.6875) and (c == 'eccentered'):
        
        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(25.4*2))-((2.54*dsonda)/(2)))

            elif unit_cali == 'INCHES':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(2))-((2.54*dsonda)/(2)))
 
            
            cf = ((-0.0002)*(t**2)) + ((0.0235)*t) + 0.796

            grcorr.append((df.iloc[i, GRindex])*cf)
    
    print(len(grcorr))
    
    df['GRcorr'] = grcorr

#Correcion GR 2

def correctionCasedHoles_corr(df, dmud, dsonda, idCsg, dCsg, odCsg, dCement, GR, cali, unit_cali, columns):

    df['GRcorr'] = 0
    GRindex = columns.index(GR)
    Calindex = columns.index(cali)
    grcorr = []

    if (dsonda == 3.375):

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (2.54/2)*( ( (dmud/8.345)*(idCsg - dsonda) ) + ((dCsg)*(odCsg - idCsg))+ ((dCement)*((df.iloc[i, Calindex]/25.4) - odCsg)) )

            elif unit_cali == 'INCHES':

                t = (2.54/2)*( ( (dmud/8.345)*(idCsg - dsonda) ) + ((dCsg)*(odCsg - idCsg))+ ((dCement)*(df.iloc[i, Calindex] - odCsg)) )

            cf = ((0.0042)*(t**2)) - ((0.045)*t) + 1.0555

            grcorr.append((df.iloc[i, GRindex])*cf)
            
    elif (dsonda == 1.6875):

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (2.54/2)*( ( (dmud/8.345)*(idCsg - dsonda) ) + ((dCsg)*(odCsg - idCsg))+ ((dCement)*((df.iloc[i, Calindex]/25.4) - odCsg)) )

            elif unit_cali == 'INCHES':

                t = (2.54/2)*( ( (dmud/8.345)*(idCsg - dsonda) ) + ((dCsg)*(odCsg - idCsg))+ ((dCement)*(df.iloc[i, Calindex] - odCsg)) )

            
            cf = ((0.0017)*(t**2)) + ((0.0124)*t) + 0.8178

            grcorr.append((df.iloc[i, GRindex])*cf)
    
    df['GRcorr'] = grcorr

#Correción GR 3

def LWDcorrectionHolesizeMudweight_corr(df, dmud, cali, dsonda, GR, unit_cali, columns):

    df['GRcorr'] = 0
    GRindex = columns.index(GR)
    Calindex = columns.index(cali)
    grcorr = []


    if (dsonda == 6.5):

        ST = 2.125

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (dmud/8.345)*((df.iloc[i, Calindex]/25.4) - 3.5 - ST)

            elif unit_cali == 'INCHES':

                t = (dmud/8.345)*((df.iloc[i, Calindex]) - 3.5 - ST)

            cf = ((0.0002)*(t**2)) + ((0.0849)*t) + 0.6604

            grcorr.append((df.iloc[i, GRindex])*cf)
            
    elif (dsonda == 6.75):

        ST = 2.031

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (dmud/8.345)*((df.iloc[i, Calindex]/25.4) - 3.5 - ST)

            elif unit_cali == 'INCHES':

                t = (dmud/8.345)*((df.iloc[i, Calindex]) - 3.5 - ST)

            
            cf = ((-5E-5)*(t**2)) + ((0.094)*t) + 0.573

            grcorr.append((df.iloc[i, GRindex])*cf)

    elif (dsonda == 8):

        ST = 3.156

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (dmud/8.345)*((df.iloc[i, Calindex]/25.4) - 3.5 - ST)

            elif unit_cali == 'INCHES':

                t = (dmud/8.345)*((df.iloc[i, Calindex]) - 3.5 - ST)

            cf = ((-0.0001)*(t**2)) + ((0.0917)*t) + 1.4415

            grcorr.append((df.iloc[i, GRindex])*cf)

    elif (dsonda == 8.25):

        ST = 2.656
        
        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(25.4*2))-((2.54*dsonda)/(2)))

            elif unit_cali == 'INCHES':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(2))-((2.54*dsonda)/(2)))
 
            
            cf = ((-5E-5)*(t**2)) + ((0.0893)*t) + 1.113

            grcorr.append((df.iloc[i, GRindex])*cf)

    elif (dsonda == 9.5):

        ST = 3.937
        
        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(25.4*2))-((2.54*dsonda)/(2)))

            elif unit_cali == 'INCHES':

                t = (dmud/8.345)*(((2.54*df.iloc[i, Calindex])/(2))-((2.54*dsonda)/(2)))
 
            
            cf = ((-0.0004)*(t**2)) + ((0.1026)*t) + 1.9219

            grcorr.append((df.iloc[i, GRindex])*cf)
    
    df['GRcorr'] = grcorr

#Correción GR 4    

def GRbariteMudSmallBoreholes_corr(df, dmud, cali, dsonda, GR, c, unit_cali, columns):

    df['GRcorr'] = 0
    GRindex = columns.index(GR)
    Calindex = columns.index(cali)
    grcorr = []

    if (dsonda == 3.375) and (c == 'centered'):

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                dd = ((df.iloc[i, Calindex]/25.4) - dsonda)

            elif unit_cali == 'INCHES':

                dd = ((df.iloc[i, Calindex]) - dsonda)

            F = ((0.0003)*(dd**2)) + ((0.0329)*dd) - 0.2748

            B = ((-0.0205)*(dmud**2)) + ((0.2859)*dmud) - 0.0908

            cf = 1 + (F*B)

            grcorr.append((df.iloc[i, GRindex])*cf)
            
    elif (dsonda == 3.375) and (c == 'eccentered'):

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                dd = ((df.iloc[i, Calindex]/25.4) - dsonda)

            elif unit_cali == 'INCHES':

                dd = ((df.iloc[i, Calindex]) - dsonda)

            F = ((0.0002)*(dd**2)) + ((0.0167)*dd) - 0.1444

            B = ((-0.0205)*(dmud**2)) + ((0.2859)*dmud) - 0.0908

            cf = 1 + (F*B)

            grcorr.append((df.iloc[i, GRindex])*cf)

    elif (dsonda == 1.6875) and (c == 'centered'):

        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                dd = ((df.iloc[i, Calindex]/25.4) - dsonda)

            elif unit_cali == 'INCHES':

                dd = ((df.iloc[i, Calindex]) - dsonda)

            F = ((0.0005)*(dd**2)) + ((0.0707)*dd) - 0.5968

            B = ((-0.0187)*(dmud**2)) + ((0.2806)*dmud) - 0.0014

            cf = 1 + (F*B)

            grcorr.append((df.iloc[i, GRindex])*cf)

    elif (dsonda == 1.6875) and (c == 'eccentered'):
        
        for i in range(0, df.shape[0], 1):

            if unit_cali == 'MM':

                dd = ((df.iloc[i, Calindex]/25.4) - dsonda)

            elif unit_cali == 'INCHES':

                dd = ((df.iloc[i, Calindex]) - dsonda)

            F = ((0.0003)*(dd**2)) + ((0.04)*dd) - 0.3329

            B = ((-0.0187)*(dmud**2)) + ((0.2806)*dmud) - 0.0014

            cf = 1 + (F*B)

            grcorr.append((df.iloc[i, GRindex])*cf)
    
    df['GRcorr'] = grcorr