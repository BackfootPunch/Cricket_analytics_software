#!/usr/bin/env python3
"""
Interactive Dashboard for The Hundred Analytics
Plotly Dash application for match analysis and predictions
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import config
from match_analyzer import MatchAnalyzer

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "The Hundred Analytics Dashboard"

# Load data
schedule_df = pd.read_csv(config.SCHEDULE_FILE)
team_ratings_df = pd.read_csv(config.TEAM_RATINGS_FILE)
venue_stats_df = pd.read_csv(config.VENUE_STATS_FILE)
tournament_analysis_df = pd.read_csv(config.OUTPUTS_DIR + "/tournament_analysis.csv")
player_stats_df = pd.read_csv(config.PLAYER_STATS_FILE)

# Initialize match analyzer
analyzer = MatchAnalyzer()

# Prepare dropdown options
match_options = []
for _, match in schedule_df.iterrows():
    match_options.append({
        'label': f"Match {match['Match_ID']}: {match['Team1']} vs {match['Team2']} at {match['Venue']}",
        'value': match['Match_ID']
    })

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🏏 The Hundred Analytics Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'margin': '20px 0'}),
        html.P("Interactive match analysis and tournament predictions for The Hundred 2025",
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '18px'})
    ]),
    
    # Main content
    html.Div([
        # Left column - Match Analysis
        html.Div([
            html.H3("🎯 Match Analyzer", style={'color': '#2c3e50'}),
            
            # Match selector
            html.Label("Select Match:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='match-selector',
                options=match_options,
                value=1,  # Default to first match
                style={'marginBottom': '20px'}
            ),
            
            # Toss inputs
            html.Div([
                html.Div([
                    html.Label("Toss Winner:", style={'fontWeight': 'bold'}),
                    dcc.RadioItems(
                        id='toss-winner',
                        options=[
                            {'label': 'Team A', 'value': 'Team A'},
                            {'label': 'Team B', 'value': 'Team B'}
                        ],
                        value='Team A',
                        inline=True,
                        style={'margin': '10px 0'}
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),
                
                html.Div([
                    html.Label("Toss Decision:", style={'fontWeight': 'bold'}),
                    dcc.RadioItems(
                        id='toss-decision',
                        options=[
                            {'label': 'Bat First', 'value': 'Bat'},
                            {'label': 'Bowl First', 'value': 'Bowl'}
                        ],
                        value='Bat',
                        inline=True,
                        style={'margin': '10px 0'}
                    )
                ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
            ]),
            
            # Match analysis output
            html.Div(id='match-analysis-output', style={'marginTop': '20px'})
            
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),
        
        # Right column - Tournament Overview
        html.Div([
            html.H3("🏆 Tournament Overview", style={'color': '#2c3e50'}),
            
            # Tournament predictions chart
            dcc.Graph(id='tournament-predictions-chart'),
            
            # Team comparison section
            html.H4("⚔️ Team Comparison", style={'color': '#2c3e50', 'marginTop': '30px'}),
            dcc.Graph(id='team-comparison-radar')
            
        ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
        
    ], style={'margin': '20px'}),
    
    # Bottom section - Venue Analysis
    html.Div([
        html.H3("🏟️ Venue Impact Analysis", style={'color': '#2c3e50', 'textAlign': 'center'}),
        
        html.Div([
            # Venue stats chart
            html.Div([
                dcc.Graph(id='venue-impact-chart')
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Player matchup heatmap
            html.Div([
                dcc.Graph(id='player-matchup-heatmap')
            ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
        ])
        
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
])

# Callback for match analysis
@app.callback(
    Output('match-analysis-output', 'children'),
    [Input('match-selector', 'value'),
     Input('toss-winner', 'value'),
     Input('toss-decision', 'value')]
)
def update_match_analysis(match_id, toss_winner, toss_decision):
    if not match_id:
        return "Please select a match"
    
    try:
        # Get match analysis
        result = analyzer.calculate_win_probability(match_id, toss_winner, toss_decision)
        
        # Create win probability gauge
        gauge_fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = result['win_prob'][0],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{result['team1']} Win Probability"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 100], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        gauge_fig.update_layout(height=300, font={'size': 14})
        
        # Return formatted output
        return html.Div([
            html.H4(f"📊 {result['team1']} vs {result['team2']}", style={'color': '#2c3e50'}),
            html.P(f"🏟️ Venue: {result['venue']}", style={'fontSize': '16px', 'margin': '5px 0'}),
            
            dcc.Graph(figure=gauge_fig),
            
            html.Div([
                html.P([
                    html.Strong("Win Probabilities: "),
                    f"{result['team1']}: {result['win_prob'][0]}% | {result['team2']}: {result['win_prob'][1]}%"
                ], style={'fontSize': '16px', 'margin': '10px 0'}),
                
                html.P([
                    html.Strong("Key Factor: "),
                    result['key_factor']
                ], style={'fontSize': '14px', 'margin': '5px 0'}),
                
                html.P([
                    html.Strong("Venue Impact: "),
                    result['venue_impact']
                ], style={'fontSize': '14px', 'margin': '5px 0'}),
                
                html.P([
                    html.Strong("Toss Impact: "),
                    result['toss_impact']
                ], style={'fontSize': '14px', 'margin': '5px 0'}),
                
                html.P([
                    html.Strong("Players to Watch: "),
                    result['player_to_watch']
                ], style={'fontSize': '14px', 'margin': '5px 0', 'fontStyle': 'italic'})
            ], style={'backgroundColor': '#e8f4f8', 'padding': '15px', 'borderRadius': '8px', 'marginTop': '10px'})
        ])
        
    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={'color': 'red'})

# Callback for tournament predictions chart
@app.callback(
    Output('tournament-predictions-chart', 'figure'),
    Input('match-selector', 'value')  # Dummy input to trigger initial load
)
def update_tournament_chart(_):
    # Create tournament win probability chart
    fig = px.bar(
        tournament_analysis_df.sort_values('Win_Probability_%', ascending=True),
        x='Win_Probability_%',
        y='Team',
        orientation='h',
        title='Tournament Win Probabilities',
        labels={'Win_Probability_%': 'Win Probability (%)', 'Team': 'Team'},
        color='Win_Probability_%',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_x=0.5,
        xaxis_title="Win Probability (%)",
        yaxis_title="Team"
    )
    
    return fig

# Callback for team comparison radar chart
@app.callback(
    Output('team-comparison-radar', 'figure'),
    Input('match-selector', 'value')  # Dummy input to trigger initial load
)
def update_team_radar(_):
    # Create radar chart comparing all teams
    fig = go.Figure()
    
    categories = ['Batting Rating', 'Bowling Rating', 'Tournament Win %']
    colors = px.colors.qualitative.Set1
    
    for idx, team_data in team_ratings_df.iterrows():
        # Get tournament win probability for this team
        win_prob = tournament_analysis_df[tournament_analysis_df['Team'] == team_data['Team']]['Win_Probability_%'].iloc[0]
        
        values = [
            team_data['Bat_Rating'],
            team_data['Bowl_Rating'],
            win_prob
        ]
        
        # Close the polygon
        values_closed = values + [values[0]]
        categories_closed = categories + [categories[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill='toself',
            name=team_data['Team'],
            line_color=colors[idx % len(colors)],
            opacity=0.6
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(team_ratings_df['Bat_Rating'].max(), team_ratings_df['Bowl_Rating'].max(), tournament_analysis_df['Win_Probability_%'].max())]
            )),
        showlegend=True,
        title="Team Strength Comparison",
        title_x=0.5,
        height=400
    )
    
    return fig

# Callback for venue impact chart
@app.callback(
    Output('venue-impact-chart', 'figure'),
    Input('match-selector', 'value')  # Dummy input to trigger initial load
)
def update_venue_chart(_):
    # Create venue impact visualization
    fig = px.scatter(
        venue_stats_df,
        x='win_percent_bat_first',
        y='avg_first_innings_score',
        size='run_rate',
        hover_name='venue',
        title='Venue Characteristics',
        labels={
            'win_percent_bat_first': 'Batting First Win %',
            'avg_first_innings_score': 'Average First Innings Score',
            'run_rate': 'Run Rate'
        },
        color='win_percent_bat_first',
        color_continuous_scale='RdYlBu_r'
    )
    
    fig.add_hline(y=venue_stats_df['avg_first_innings_score'].mean(), line_dash="dash", 
                  annotation_text="Average Score", annotation_position="bottom right")
    fig.add_vline(x=50, line_dash="dash", 
                  annotation_text="Neutral (50%)", annotation_position="top left")
    
    fig.update_layout(
        height=400,
        title_x=0.5
    )
    
    return fig

# Callback for player matchup heatmap
@app.callback(
    Output('player-matchup-heatmap', 'figure'),
    Input('match-selector', 'value')
)
def update_player_heatmap(match_id):
    if not match_id:
        return px.imshow([[0]], title="Select a match to see player matchups")
    
    try:
        # Get match details
        match_details = analyzer.get_match_details(match_id)
        team1 = match_details['team1']
        team2 = match_details['team2']
        
        # Get top players from each team
        team1_players = player_stats_df[
            (player_stats_df['team'] == team1) & 
            (player_stats_df['role'].isin(['Batter', 'All-rounder'])) &
            (player_stats_df['bat_avg_first'] > 0)
        ].nlargest(5, 'bat_avg_first')
        
        team2_players = player_stats_df[
            (player_stats_df['team'] == team2) & 
            (player_stats_df['role'].isin(['Batter', 'All-rounder'])) &
            (player_stats_df['bat_avg_first'] > 0)
        ].nlargest(5, 'bat_avg_first')
        
        if len(team1_players) == 0 or len(team2_players) == 0:
            return px.imshow([[0]], title="Insufficient player data")
        
        # Create matchup matrix (simplified - based on batting averages)
        matrix = []
        team1_names = []
        team2_names = []
        
        for _, p1 in team1_players.iterrows():
            row = []
            team1_names.append(p1['player'].split()[-1])  # Last name only
            for _, p2 in team2_players.iterrows():
                if p1 not in team2_names:
                    team2_names.append(p2['player'].split()[-1])
                # Simple matchup score based on batting averages
                matchup_score = (p1['bat_avg_first'] + p1['bat_sr_first']/5) - (p2['bat_avg_first'] + p2['bat_sr_first']/5)
                row.append(matchup_score)
            matrix.append(row)
        
        fig = px.imshow(
            matrix,
            x=team2_names[:len(team2_players)],
            y=team1_names,
            title=f"Player Matchup Matrix: {team1} vs {team2}",
            labels=dict(x=team2, y=team1, color="Advantage"),
            aspect="auto",
            color_continuous_scale="RdBu"
        )
        
        fig.update_layout(height=400, title_x=0.5)
        return fig
        
    except Exception as e:
        return px.imshow([[0]], title=f"Error: {str(e)}")

# Run the app
if __name__ == '__main__':
    print("🚀 Starting The Hundred Analytics Dashboard...")
    print("📊 Dashboard will be available at: http://0.0.0.0:8050")
    print("🎯 Features: Match Analysis, Tournament Predictions, Team Comparisons, Venue Analysis")
    print("🌐 Access the dashboard from your browser!")
    app.run_server(debug=False, host='0.0.0.0', port=8050, dev_tools_ui=False)