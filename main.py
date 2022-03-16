from matplotlib.style import use
from flask import request, make_response, redirect, render_template, session, url_for, flash, Response
import os
from werkzeug.utils import secure_filename
import lasio

from app import create_app
from app.forms import LoginForm, correctionHolesizeMudweight, correctionCasedHoles, LWDcorrectionHolesizeMudweight, GRbariteMudSmallBoreholes, mnemonic
from app.correciones import Vshh, correctionCasedHoles_corr, correctionHolesizeMudweight_corr, GRbariteMudSmallBoreholes_corr, LWDcorrectionHolesizeMudweight_corr
from io import StringIO
import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = create_app()

mnemonics = []

@app.route('/')
def index():
    
    response = make_response(redirect('/login'))

    return response

@app.route('/aboutus')
def aboutus():

    return render_template('aboutus.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    context = {

        'login_form': login_form

    }

    if login_form.validate_on_submit():

        username = login_form.username.data
        password = login_form.password.data
        usernameTrue = 'EIPEF@uis.edu.co'
        passwordTrue = 'EF2021-2'

        if ((username == usernameTrue) and (password == passwordTrue)):


            session['username'] = username
            session['password'] = password

            return make_response(redirect(url_for('deposito')))
    
    return render_template('index.html', **context)

@app.route('/deposito', methods=['GET', 'POST'])
def deposito():

    if request.method == 'POST':

        f = request.files['archivo']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        session['filename'] = filename

        return make_response(redirect(url_for('MNEMONIC')))

    return render_template('deposito.html')

@app.route('/mnemonic', methods=['GET', 'POST']) 
def MNEMONIC():

    mnemonic_form = mnemonic()
    url = './app/static/folder/' + session['filename']
    las = lasio.read(url)
    mnemonics = []

    for i in las.curves:

        mnemonics.append(i.mnemonic)

    context = {

        'mnemonic_form': mnemonic_form,
        'mnemonics': mnemonics

    }

    if mnemonic_form.validate_on_submit():

        session['mnemonic_gr']= mnemonic_form.gr.data
        session['mnemonic_den'] = mnemonic_form.density.data
        session['mnemonic_dphi'] = mnemonic_form.dphi.data
        session['mnemonic_ilm'] = mnemonic_form.ilm.data
        session['mnemonic_ild'] = mnemonic_form.ild.data
        session['mnemonic_sflu'] = mnemonic_form.sflu.data
        session['mnemonic_cali'] = mnemonic_form.cali.data
        session['mnemonic_drho'] = mnemonic_form.drho.data
        session['mnemonic_nphi'] = mnemonic_form.nphi.data

        print(session['mnemonic_gr'])

        if session['mnemonic_gr'] != '':

            return make_response(redirect(url_for('seleccionGR')))
    
    return render_template('mnemonic.html', **context)


 

@app.route('/SeleccionGR', methods=['GET', 'POST'])
def seleccionGR():

    return render_template('SeleccionGR.html')


@app.route('/GRCHSMW', methods=['GET', 'POST'])
def grchsmw():

    hswm_form = correctionHolesizeMudweight()

    context = {

        'hswm_form': hswm_form

    }

    if hswm_form.validate_on_submit():

        dm = hswm_form.dm.data
        dsonda = hswm_form.dsonda.data
        centered = hswm_form.centered.data

        session['dm'] = dm
        session['dsonda'] = dsonda
        session['centered'] = centered
        session['GR_method'] = 'correctionHolesizeMudweight'

        return make_response(redirect(url_for('graphic')))
    
    return render_template('GRCHSMW.html', **context)

@app.route('/GRCCH', methods=['GET', 'POST'])
def grcch():

    ch_form = correctionCasedHoles()

    context = {

        'ch_form': ch_form

    }

    if ch_form.validate_on_submit():

        dm = ch_form.dm.data
        dsonda = ch_form.dsonda.data 
        odCsg = ch_form.odCsg.data
        idCsg = ch_form.idCsg.data
        dCsg = ch_form.dCsg.data
        dCement = ch_form.dCement.data

        session['dm'] = dm
        session['dsonda'] = dsonda
        session['odCsg'] = odCsg
        session['idCsg'] = idCsg
        session['dCsg'] = dCsg
        session['dCement'] = dCement
        session['GR_method'] = 'correctionCasedHoles'

        return make_response(redirect(url_for('graphic')))
    
    return render_template('GRCCH.html', **context)

@app.route('/LWD', methods=['GET', 'POST'])
def lwd():

    lwd_form = LWDcorrectionHolesizeMudweight()

    context = {

        'lwd_form': lwd_form

    }

    if lwd_form.validate_on_submit():

        dm = lwd_form.dm.data
        dsonda = lwd_form.dsonda.data 

        session['dm'] = dm
        session['dsonda'] = dsonda
        session['GR_method'] = 'LWDcorrectionHolesizeMudweight'

        return make_response(redirect(url_for('graphic')))
    
    return render_template('LWD.html', **context)

@app.route('/MSBH', methods=['GET', 'POST'])
def msbh():

    sbh_form = GRbariteMudSmallBoreholes()

    context = {

        'sbh_form': sbh_form

    }

    if sbh_form.validate_on_submit():

        dm = sbh_form.dm.data
        dsonda = sbh_form.dsonda.data 
        centered = sbh_form.centered.data

        session['dm'] = dm
        session['dsonda'] = dsonda
        session['centered'] = centered
        session['GR_method'] = 'GRbariteMudSmallBoreholes'

        return make_response(redirect(url_for('graphic')))
    
    return render_template('SBH.html', **context)

@app.route('/graphic', methods=['GET', 'POST'])
def graphic():

    return render_template('graphic.html')

def create_header(name):

    url = './app/static/folder/' + name

    file = lasio.read(url)
    df = file.df()
    df.reset_index(inplace=True)

    fig = Figure(df.head())

    return fig


def create_figure(name):

    url = './app/static/folder/' + name

    file = lasio.read(url)

    columns = []

    for curve in file.curves:
        columns.append(curve.mnemonic)

    for data in file.well:

        if data.mnemonic == 'STRT':
            
            start = data.value
            unit = data.unit
            print(f'start: {start}')
            print(f'Unit: {unit}')

        if data.mnemonic == 'STOP':

            stop = data.value
            print(f'Stop: {stop}')

    unit_cali = ''
    
    for curve in file.curves:
    
        if curve.mnemonic == session['mnemonic_cali']:

            unit_cali = curve.unit
    
    df = file.df()
    df.reset_index(inplace=True)
    df['Vsh'] = 5
    df['GRcorr'] = 0
    df['Vsh_GRcorr'] = 0
    df['porosidad_efectiva'] = 0
    columns.append('Vsh')
    columns.append('GRcorr')
    columns.append('Vsh_GRcorr')
    columns.append('porosidad_efectiva')

    if (session['mnemonic_cali'] != 'N/A') and (session['mnemonic_gr'] != 'N/A'):

        #Cálculo del V shale

        Vshh(df, session['mnemonic_gr'], 1, columns)

        #GR coreciones

        if (session['GR_method'] == 'correctionHolesizeMudweight'):

            correctionHolesizeMudweight_corr(df, float(session['dm']), session['mnemonic_cali'], float(session['dsonda']), session['mnemonic_gr'], session['centered'], unit_cali, columns)

        elif(session['GR_method'] == 'correctionCasedHoles'):

            correctionCasedHoles_corr(df, float(session['dm']), float(session['dsonda']), float(session['idCsg']), float(session['dCsg']), float(session['odCsg']), float(session['dCement']), session['mnemonic_gr'], session['mnemonic_cali'], unit_cali, columns)

        elif(session['GR_method'] == 'LWDcorrectionHolesizeMudweight'):

            LWDcorrectionHolesizeMudweight_corr(df, float(session['dm']), session['mnemonic_cali'], float(session['dsonda']), session['mnemonic_gr'], unit_cali, columns)

        elif(session['GR_method'] == 'GRbariteMudSmallBoreholes'):

            GRbariteMudSmallBoreholes_corr(df, float(session['dm']), session['mnemonic_cali'], float(session['dsonda']), session['mnemonic_gr'], session['centered'], unit_cali, columns)

        #Volumen de arcilla corregido

        Vshh(df, 'GRcorr', 2, columns)
    
    if (session['mnemonic_dphi'] != 'N/A') and ((session['mnemonic_gr'] != 'N/A')):

        #Porosidad efectiva

        efec_porr = []

        dphi_shale = 13

        for i in range(0, df.shape[0], 1):

            if i != df.shape[0]:

                dphi_sand = df.iloc[i, columns.index(session['mnemonic_dphi'])]

                if (session['mnemonic_gr'] != 'N/A'):

                    vshi = df.iloc[i, columns.index('Vsh')]

                elif(session['mnemonic_cali'] != 'N/A') and (session['mnemonic_gr'] != 'N/A'):

                    vshi = df.iloc[i, columns.index('Vsh_GRcorr')]

                dphi_vsh = (dphi_sand) - (dphi_shale*vshi)
                
                efec_porr.append(dphi_vsh.round(4))

        df['porosidad_efectiva'] = efec_porr

    #fig 
    fig = Figure(figsize=(15, 10))

    ax1 = fig.add_subplot(1, 8, 1)
    ax2 = fig.add_subplot(1, 8, 2)
    ax3 = fig.add_subplot(1, 8, 3)
    ax4 = fig.add_subplot(1, 8, 4)
    ax5 = ax4.twiny()
    ax6 = ax4.twiny()
    ax7 = fig.add_subplot(1, 8, 5)
    ax8 = ax3.twiny()
    ax10 = fig.add_subplot(1, 8, 6)
    ax11 = fig.add_subplot(1, 8, 7)
    ax12 = ax1.twiny()
    ax13 = ax11.twiny()
    ax14 = fig.add_subplot(1, 8, 8)

    ax1.plot(session['mnemonic_gr'], columns[0], data = df, color='green')
    ax1.set_xlabel(session['mnemonic_gr'])
    ax1.set_ylim(stop, start)
    ax1.grid()

    ax2.plot(session['mnemonic_den'], columns[0], data = df, color='black')
    ax2.set_xlabel(session['mnemonic_den'])
    ax2.set_ylim(stop, start)
    ax2.grid()
    ax2.get_yaxis().set_visible(False)

    ax3.plot(session['mnemonic_dphi'], columns[0], data = df, color='red')
    ax3.set_xlabel(session['mnemonic_dphi'])
    ax3.set_ylim(stop, start)
    ax3.grid()
    ax3.get_yaxis().set_visible(False)

    ax4.plot(session['mnemonic_ilm'], columns[0], data = df, color='blue')
    ax4.set_xlabel(session['mnemonic_ilm'])
    ax4.set_ylim(stop, start)
    ax4.grid()
    ax4.get_yaxis().set_visible(False)

    ax5.plot(session['mnemonic_ild'], columns[0], data = df, color='orange')
    ax5.set_xlabel(session['mnemonic_ild'])
    ax5.set_ylim(stop, start)
    ax5.grid()
    ax5.get_yaxis().set_visible(False)

    ax6.plot(session['mnemonic_sflu'], columns[0], data = df, color='black')
    ax6.set_xlabel(session['mnemonic_sflu'])
    ax6.set_ylim(stop, start)
    ax6.grid()
    ax6.get_yaxis().set_visible(False)

    ax7.plot(session['mnemonic_cali'], columns[0], data = df, color='brown')
    ax7.set_xlabel(session['mnemonic_cali'])
    ax7.set_ylim(stop, start)
    ax7.grid()
    ax7.get_yaxis().set_visible(False)

    ax8.plot(session['mnemonic_drho'], columns[0], data = df, color='yellow')
    ax8.set_xlabel(session['mnemonic_drho'])
    ax8.set_ylim(stop, start)
    ax8.grid()
    ax8.get_yaxis().set_visible(False)

    ax10.plot(session['mnemonic_nphi'], columns[0], data = df, color='gold')
    ax10.set_xlabel(session['mnemonic_nphi'])
    ax10.set_ylim(stop, start)
    ax10.grid()
    ax10.get_yaxis().set_visible(False)

    if (session['mnemonic_gr'] != 'N/A'):

        ax11.plot('Vsh', columns[0], data = df, color='green')
        ax11.set_xlabel('Vsh')
        ax11.set_xlim(0, 1, 0.5)
        ax11.set_ylim(stop, start)
        ax11.grid()
        ax11.get_yaxis().set_visible(False)
    
    if (session['mnemonic_cali'] != 'N/A') and (session['mnemonic_gr'] != 'N/A'):

        ax12.plot('GRcorr', columns[0], data = df, color='Blue')
        ax12.set_xlabel('GRcorr')
        ax12.set_ylim(stop, start)
        ax12.grid()
        ax12.get_yaxis().set_visible(False)

        ax13.plot('Vsh_GRcorr', columns[0], data = df, color='Blue')
        ax13.set_xlabel('Vsh_GRcorr')
        ax13.set_ylim(stop, start)
        ax13.grid()
        ax13.get_yaxis().set_visible(False)

    if (session['mnemonic_dphi'] != 'N/A') and ((session['mnemonic_gr'] != 'N/A')):

        ax14.plot('porosidad_efectiva', columns[0], data = df, color='Blue')
        ax14.set_xlabel('porosidad_efectiva')
        ax14.set_ylim(stop, start)
        ax14.grid()
        ax14.get_yaxis().set_visible(False)

    return fig


@app.route('/plot', methods=['GET', 'POST'])
def plot():
    fig = create_figure(session['filename'])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return base64.encodebytes(output.getvalue())


