#!/usr/bin/env python3
"""
Team Strength Calculator for The Hundred
Calculates team ratings based on squad composition and player statistics
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import config

class TeamStrengthCalculator:
    def __init__(self):
        self.squads_df = pd.read_csv(config.SQUADS_FILE)
        self.player_stats_df = pd.read_csv(config.PLAYER_STATS_FILE)
        self.venue_stats_df = pd.read_csv(config.VENUE_STATS_FILE)
        
        # Merge squad and player stats
        self.full_data = self.squads_df.merge(
            self.player_stats_df, 
            left_on=['Team', 'Player'], 
            right_on=['team', 'player'], 
            how='left'
        )
    
    def calculate_batting_strength(self, team_name):
        """Calculate batting strength for a team"""
        team_data = self.full_data[self.full_data['Team'] == team_name]
        
        # Get all players who can bat (Batters and All-rounders)
        batters = team_data[team_data['Role'].isin(['Batter', 'All-rounder'])]
        batters = batters[batters['bat_avg_first'] > 0]  # Filter valid batting stats
        
        if len(batters) == 0:
            return 50.0  # Default rating
        
        # Get top 5 batters by average
        top_batters = batters.nlargest(5, 'bat_avg_first')
        
        if len(top_batters) < 5:
            # Fill with remaining batters
            remaining = batters.nsmallest(len(batters) - len(top_batters), 'bat_avg_first')
            top_batters = pd.concat([top_batters, remaining])
        
        # Calculate average of top batters
        avg_batting = top_batters['bat_avg_first'].mean()
        avg_strike_rate = top_batters['bat_sr_first'].mean()
        
        # Get team's historical run rate from venue data (using team's home venue)
        team_venue_map = {
            'London Spirit': "Lord's, London",
            'Oval Invincibles': 'Kennington Oval, London',
            'Manchester Originals': 'Emirates Old Trafford, Manchester',
            'Birmingham Phoenix': 'Edgbaston, Birmingham',
            'Northern Superchargers': 'Headingley, Leeds',
            'Southern Brave': 'The Rose Bowl, Southampton',
            'Trent Rockets': 'Trent Bridge, Nottingham',
            'Welsh Fire': 'Sophia Gardens, Cardiff'
        }
        
        home_venue = team_venue_map.get(team_name)
        venue_data = self.venue_stats_df[self.venue_stats_df['venue'] == home_venue]
        
        if len(venue_data) > 0:
            historical_run_rate = venue_data.iloc[0]['run_rate']
        else:
            historical_run_rate = 8.5  # Default run rate for The Hundred
        
        # Calculate batting strength: AVG(top 5 batters) * (historical run rate/10)
        batting_strength = avg_batting * (historical_run_rate / 10)
        
        # Add strike rate factor (bonus for high SR)
        sr_factor = min(avg_strike_rate / 130, 1.2)  # Cap at 1.2x multiplier
        batting_strength *= sr_factor
        
        return round(batting_strength, 1)
    
    def calculate_bowling_strength(self, team_name):
        """Calculate bowling strength for a team"""
        team_data = self.full_data[self.full_data['Team'] == team_name]
        
        # Get all players who can bowl (Bowlers and All-rounders)
        bowlers = team_data[team_data['Role'].isin(['Bowler', 'All-rounder'])]
        bowlers = bowlers[bowlers['bowl_econ_first'] > 0]  # Filter valid bowling stats
        
        if len(bowlers) == 0:
            return 50.0  # Default rating
        
        # Get top 5 bowlers by economy rate (lower is better)
        top_bowlers = bowlers.nsmallest(5, 'bowl_econ_first')
        
        if len(top_bowlers) < 5:
            # Fill with remaining bowlers
            remaining = bowlers.nlargest(len(bowlers) - len(top_bowlers), 'bowl_econ_first')
            top_bowlers = pd.concat([top_bowlers, remaining])
        
        # Calculate average economy of top bowlers
        avg_economy = top_bowlers['bowl_econ_first'].mean()
        avg_bowling_avg = top_bowlers['bowl_avg_first'].mean()
        
        # Calculate bowling strength: (10 - AVG(top 5 bowlers' economy)) * 2
        bowling_strength = (10 - avg_economy) * 2
        
        # Add bowling average factor (lower average is better)
        avg_factor = max(1.0, (30 - avg_bowling_avg) / 30)  # Bonus for low averages
        bowling_strength *= avg_factor
        
        # Ensure positive rating
        bowling_strength = max(bowling_strength, 10.0)
        
        return round(bowling_strength, 1)
    
    def calculate_all_team_ratings(self):
        """Calculate ratings for all teams"""
        teams = self.squads_df['Team'].unique()
        team_ratings = []
        
        for team in teams:
            bat_rating = self.calculate_batting_strength(team)
            bowl_rating = self.calculate_bowling_strength(team)
            
            # Calculate overall rating (weighted average)
            overall_rating = (bat_rating * 0.55 + bowl_rating * 0.45)  # Slightly favor batting in T20
            
            team_ratings.append({
                'Team': team,
                'Bat_Rating': bat_rating,
                'Bowl_Rating': bowl_rating,
                'Overall_Rating': round(overall_rating, 1)
            })
            
            print(f"{team}: Batting={bat_rating}, Bowling={bowl_rating}, Overall={overall_rating:.1f}")
        
        return pd.DataFrame(team_ratings)
    
    def create_radar_plots(self, team_ratings_df):
        """Create radar plots comparing teams"""
        
        # Create subplot for radar charts (2x4 layout for 8 teams)
        fig = make_subplots(
            rows=2, cols=4,
            subplot_titles=team_ratings_df['Team'].tolist(),
            specs=[[{"type": "polar"}]*4, [{"type": "polar"}]*4]
        )
        
        # Define categories for radar chart
        categories = ['Batting Rating', 'Bowling Rating', 'Overall Rating']
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']
        
        for idx, team_data in team_ratings_df.iterrows():
            row = (idx // 4) + 1
            col = (idx % 4) + 1
            
            # Normalize ratings to 0-100 scale for better visualization
            max_rating = team_ratings_df[['Bat_Rating', 'Bowl_Rating', 'Overall_Rating']].max().max()
            
            values = [
                (team_data['Bat_Rating'] / max_rating) * 100,
                (team_data['Bowl_Rating'] / max_rating) * 100,
                (team_data['Overall_Rating'] / max_rating) * 100,
                (team_data['Bat_Rating'] / max_rating) * 100  # Close the polygon
            ]
            
            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories + [categories[0]],  # Close the polygon
                    fill='toself',
                    name=team_data['Team'],
                    line_color=colors[idx % len(colors)],
                    fillcolor=colors[idx % len(colors)],
                    opacity=0.6
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            title="Team Strength Comparison - The Hundred 2025",
            height=800,
            showlegend=False
        )
        
        # Save the plot
        plot_file = config.OUTPUTS_DIR + "/team_radar_plots.html"
        fig.write_html(plot_file)
        print(f"Radar plots saved to: {plot_file}")
        
        return fig
    
    def save_team_ratings(self, team_ratings_df):
        """Save team ratings to CSV"""
        team_ratings_df.to_csv(config.TEAM_RATINGS_FILE, index=False)
        print(f"Team ratings saved to: {config.TEAM_RATINGS_FILE}")
        
        # Display summary
        print("\nTeam Ratings Summary:")
        print(team_ratings_df.sort_values('Overall_Rating', ascending=False).to_string(index=False))


def main():
    """Main function to calculate team strengths"""
    print("Calculating team strengths...")
    
    calculator = TeamStrengthCalculator()
    
    # Calculate team ratings
    team_ratings = calculator.calculate_all_team_ratings()
    
    # Save ratings
    calculator.save_team_ratings(team_ratings)
    
    # Create radar plots
    calculator.create_radar_plots(team_ratings)
    
    print("\nTeam strength calculation complete!")


if __name__ == "__main__":
    main()