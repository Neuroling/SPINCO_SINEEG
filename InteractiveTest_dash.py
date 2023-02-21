# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:31:20 2023

@author: gfraga
"""
import io
import dash
import base64
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import scipy.io.wavfile as wav

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Waveform and PSD Viewer'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-data-upload')
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        fs, data = wav.read(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    # create time and frequency arrays
    N = len(data)
    T = 1.0 / fs
    time = np.arange(0, N) * T
    freq = np.fft.fftfreq(N, T)

    # calculate power spectral density
    psd = np.abs(np.fft.fft(data))**2 / N
    psd = psd[freq >= 0]
    freq = freq[freq >= 0]

    # create waveform plot
    waveform = go.Scatter(x=time, y=data, mode='lines', name='Waveform')

    # create PSD plot
    psd_plot = go.Scatter(x=freq, y=psd, mode='lines', name='PSD')

    # return a dictionary of the two plots
    return {
        'waveform': waveform,
        'psd': psd_plot
    }

@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
              [dash.dependencies.Input('upload-data', 'contents')],
              [dash.dependencies.State('upload-data', 'filename')])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)
        ]
        waveform_plots = [c['waveform'] for c in children]
        psd_plots = [c['psd'] for c in children]
        return html.Div([
            html.H3('Waveform Plots'),
            dcc.Graph(
                id='waveform-graph',
                figure={
                    'data': waveform_plots,
                    'layout': go.Layout(
                        title='Waveform Plot'
                    )
                }
            ),
            html.H3('PSD Plots'),
            dcc.Graph(
                id='psd-graph',
                figure={
                    'data': psd_plots,
                    'layout': go.Layout(
                        title='Power Spectral Density Plot'
                    )
                }
            )
        ])
    else:
        return html.Div([
            'Drag and drop or click "Select Files" to browse .wav files.'
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
