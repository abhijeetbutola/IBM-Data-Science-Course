import pandas as pd
import dash
from dash import html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import no_update

df = pd.read_csv(r'D:\Downloads\airline_data.csv',
                encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

# Review1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

year = list(map(str, range(2005,2021)))


"""Compute graph data for creating yearly airline performance report 

Function that takes airline data as input and create 5 dataframes based on the grouping condition to be used for plottling charts and grphs.

Argument:
     
    df: Filtered dataframe
    
Returns:
   Dataframes to create graph. 
"""
def compute_data_choice_1(df_fil):
    # Cancellation Category Count
    bar_data = df_fil.groupby(['Month','CancellationCode'])['Flights'].sum().reset_index()
    # Average flight time by reporting airline
    line_data = df_fil.groupby(['Month','Reporting_Airline'])['AirTime'].mean().reset_index()
    # Diverted Airport Landings
    div_data = df_fil[df_fil['DivAirportLandings'] != 0.0]
    # Source state count
    map_data = df_fil.groupby(['OriginState'])['Flights'].sum().reset_index()
    # Destination state count
    tree_data = df_fil.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
    return bar_data, line_data, div_data, map_data, tree_data


"""Compute graph data for creating yearly airline delay report

This function takes in airline data and selected year as an input and performs computation for creating charts and plots.

Arguments:
    df: Input airline data.
    
Returns:
    Computed average dataframes for carrier delay, weather delay, NAS delay, security delay, and late aircraft delay.
"""
def compute_data_choice_2(df_fil):
    # Compute delay averages
    avg_car = df_fil.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df_fil.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df_fil.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df_fil.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df_fil.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


# Layout of dashboard
app.layout = html.Div(children=[
                html.H1('US Domestic Airline Flights Performance', style={'textAlign':'center', 'font-size':24, 'color':'#503D36'}),
                
                
                # html.Br(),
    

                html.Div([
                    
                    # html.Div([
                    
                    #html.Div([
                        html.H2('Report Type:', style={}),
                          dcc.Dropdown(id='input-type', options=[{'label':'Yearly Airline Performance Report', 'value':'Opt1'},
                                                          {'label':'Yearly Airline Delay Report', 'value':'Opt2'}],
                                                          placeholder='Select a Report Type', style={'max-width':'400px', 'width':'100%'})
                        #]),
                        # ]),
                ], style={'gap':'20px', 'align-items':'center', 'display':'flex', 'justify-content':'center', 'width':'100%'}),
    
                html.Div([
                    html.H2('Choose Year:', style={}),
                           dcc.Dropdown([i for i in year], id='input-year', placeholder='Select a year', style={'max-width':'400px', 'width':'100%'})
                
                ], style={'display':'flex','gap':'20px', 'align-items':'center', 'justify-content':'center', 'width':'100%'}),
    
            html.Div([html.Div([
                    html.Div([ ], id='plot1', style={'width':'100%'})
                    ], style={'display':'flex', 'width':'100%', 'max-width':'1400px', 'margin-left': 'auto', 'margin-right': 'auto'}),
        
                    
                html.Div([
                    html.Div([ ], id='plot2', style={'margin-left': 'auto'}),
                    html.Div([ ], id='plot3', style={'margin-right': 'auto'})
                ], style={'display':'flex'}),
                
    
                html.Div([
                    html.Div([ ], id='plot4', style={'margin-left': 'auto'}),
                    html.Div([ ], id='plot5', style={'margin-right': 'auto'})
                ], style={'display':'flex'})
                ], style={'width':'100%'})
                # html.Div([
                #     html.Div([ ], id='plot1', style={'width':'100%'})
                #     ], style={'display':'flex', 'width':'100%', 'max-width':'1400px'}),
        
                    
                # html.Div([
                #     html.Div([ ], id='plot2'),
                #     html.Div([ ], id='plot3')
                # ], style={'display':'flex'}),
                
    
                # html.Div([
                #     html.Div([ ], id='plot4'),
                #     html.Div([ ], id='plot5')
                # ], style={'display':'flex'}),


    ])


# Callback function definition
# Task4: Add 5 output components

@app.callback([
    Output('plot1','children'),
    Output('plot2','children'),
    Output('plot3','children'),
    Output('plot4','children'),
    Output('plot5','children')
    ], 
    [Input('input-type','value'),
     Input('input-year','value')],
    # Review4: Holding output state till user enters all the form information. In this case, it will be chart type and year
    [State("plot1", 'children'), State("plot2", "children"),
                State("plot3", "children"), State("plot4", "children"),
                State("plot5", "children")
    ])

# Add computation to callback function and return graph
def get_graph(chart, yr, c1, c2, c3, c4, c5):
    # print(yr)
    # Select data
    airline_data = df[df['Year']==int(yr)]

    if chart == 'Opt1':
        # Compute the required information for creating graph from the data
        bar_data, line_data, div_data, map_data, tree_data = compute_data_choice_1(airline_data)
        # Number of flights under different cancellation categories
        bar_fig = px.bar(bar_data, x='Month', y='Flights', color='CancellationCode', title='Monthly Flight Cancellation')
        # Average flight time by reporting airline using line chart
        line_fig = px.line(line_data, x='Month', y='AirTime', color='Reporting_Airline', title='Monthly AirTime of Each Airline')
        # Percentage of diverted airport landings per reporting airline using pie chart
        pie_fig = px.pie(div_data, values='DivAirportLandings', names='Reporting_Airline', title='Diverted Airport Landings by Airline')
        # Number of flights flying from each state using choropleth map
        map_fig = px.choropleth(map_data,  # Input data
                locations='OriginState', 
                color='Flights',  
                hover_data=['OriginState', 'Flights'], 
                locationmode = 'USA-states', # Set to plot as US States
                color_continuous_scale='GnBu',
                range_color=[0, map_data['Flights'].max()]) 
        map_fig.update_layout(
                title_text = 'Number of flights from origin state', 
                geo_scope='usa') # Plot only the USA instead of globe
        # Number of flights flying to each state from each reporting airline using treemap chart
        tree_fig = px.treemap(tree_data, path=['DestState', 'Reporting_Airline'], values='Flights')

        # Return dcc.Graph component to the empty division
        return [dcc.Graph(figure=tree_fig),
                dcc.Graph(figure=pie_fig),
                dcc.Graph(figure=map_fig),
                dcc.Graph(figure=bar_fig),
                dcc.Graph(figure=line_fig)
                ]
    else:
        # REVIEW7: This covers chart type 2 and we have completed this exercise under Flight Delay Time Statistics Dashboard section
        # Compute required information for creating graph from the data
        avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_data_choice_2(airline_data)
        
        # Create graph
        carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrrier delay time (minutes) by airline')
        weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline')
        nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS delay time (minutes) by airline')
        sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline')
        late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average late aircraft delay time (minutes) by airline')
        
        return[dcc.Graph(figure=carrier_fig), 
                dcc.Graph(figure=weather_fig), 
                dcc.Graph(figure=nas_fig), 
                dcc.Graph(figure=sec_fig), 
                dcc.Graph(figure=late_fig)]
    

# Run the application
if __name__ == '__main__':
    app.run_server()



# debug=True
# app.run_server(mode="inline", host="localhost", debug=False, dev_tools_ui=False, dev_tools_props_check=False)

