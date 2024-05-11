import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np


app = dash.Dash(__name__)
server = app.server

# Define the base directory where all folders are located
base_dir = os.path.join(".", "Finetuning_Results", "Finetuning_Results")

# Get all subdirectories (folders) in the base directory
folders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
data_dict = {}

# Iterate through each folder
for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    folder_data = []
    folder_names = []
    
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            folder_data.append(df)
            folder_names.append(os.path.splitext(filename)[0])  

    data_dict[folder] = {'data': folder_data, 'names': folder_names}

app.layout = html.Div([
    dcc.Dropdown(
        id='folders',
        options=[{'label': folder, 'value': folder} for folder in data_dict.keys()],
        value=folders[0],  
        multi=False  
    ),
    dcc.Dropdown(
        id='lines',
        multi=True,
    ),
    dcc.Graph(id='graph')
])

# Update the options of the lines dropdown based on the selected folder
@app.callback(
    Output('lines', 'options'),
    [Input('folders', 'value')]
)
def update_lines_options(selected_folder):
    folder_data = data_dict[selected_folder]['data']
    folder_names = data_dict[selected_folder]['names']
    return [{'label': name, 'value': i} for i, name in enumerate(folder_names)]

# Update the graph based on the selected folder and lines
@app.callback(
    Output('graph', 'figure'),
    [Input('folders', 'value'),
     Input('lines', 'value')]
)
def update_graph(selected_folder, selected_indices):
    fig = go.Figure()
    
    folder_data = data_dict[selected_folder]['data']
    folder_names = data_dict[selected_folder]['names']
    
    if selected_indices is None:
        selected_indices = []
    
    for i in selected_indices:
        fig.add_trace(go.Scatter(x=folder_data[i].index, y=folder_data[i]['Value'], mode='lines', name=folder_names[i]))
    
    #algorithm_name = selected_folder.split('_')[0]
    

    fig.update_layout(autosize=True, title=f"{selected_folder} Finetuning",
                      xaxis_title="Episode", yaxis_title="Mean Episodic Reward", title_x=0.5)
    
    return fig

if __name__ == '__main__':
    #app.run_server(host='0.0.0.0', port=8888 , debug=True)
    app.run_server(debug=True, port = 8050)


