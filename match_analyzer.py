#!/usr/bin/env python3
"""
Match Analyzer for The Hundred
Core functionality to analyze matches and calculate win probabilities
"""

import pandas as pd
import numpy as np
import random
from typing import Dict, Tuple
import config

class MatchAnalyzer:
    def __init__(self):
        self.schedule_df = pd.read_csv(config.SCHEDULE_FILE)
        self.team_ratings_df = pd.read_csv(config.TEAM_RATINGS_FILE)
        self.venue_stats_df = pd.read_csv(config.VENUE_STATS_FILE)
        self.player_stats_df = pd.read_csv(config.PLAYER_STATS_FILE)
        
        # Create team ratings lookup
        self.team_ratings = {
            row['Team']: {
                'batting': row['Bat_Rating'],
                'bowling': row['Bowl_Rating'], 
                'overall': row['Overall_Rating']
            }
            for _, row in self.team_ratings_df.iterrows()
        }
        
        # Create venue stats lookup
        self.venue_stats = {
            row['venue']: {
                'bat_first_win_pct': row['win_percent_bat_first'],
                'bowl_first_win_pct': row['win_percent_bowl_first'],
                'avg_score': row['avg_first_innings_score'],
                'run_rate': row['run_rate']
            }
            for _, row in self.venue_stats_df.iterrows()
        }
    
    def get_match_details(self, match_id: int) -> Dict:
        """Get match details from schedule"""
        match_data = self.schedule_df[self.schedule_df['Match_ID'] == match_id]
        
        if len(match_data) == 0:
            raise ValueError(f"Match ID {match_id} not found")
        
        match = match_data.iloc[0]
        return {
            'match_id': match_id,
            'team1': match['Team1'],
            'team2': match['Team2'],
            'venue': match['Venue'],
            'date': match['Date'],
            'time': match['Time']
        }
    
    def get_team_rating(self, team_name: str) -> Dict:
        """Get team ratings"""
        return self.team_ratings.get(team_name, {
            'batting': 50.0,
            'bowling': 50.0,
            'overall': 50.0
        })
    
    def get_venue_impact(self, venue: str) -> Dict:
        """Get venue impact factors"""
        return self.venue_stats.get(venue, {
            'bat_first_win_pct': 50.0,
            'bowl_first_win_pct': 50.0,
            'avg_score': 150,
            'run_rate': 8.5
        })
    
    def get_head_to_head_record(self, team1: str, team2: str) -> Dict:
        """Get head-to-head record (simulated for now)"""
        # In a real scenario, this would query historical match data
        # For now, generate based on team ratings
        
        team1_rating = self.get_team_rating(team1)['overall']
        team2_rating = self.get_team_rating(team2)['overall']
        
        # Simulate a realistic head-to-head based on ratings
        total_matches = random.randint(8, 15)  # Historical matches played
        
        if team1_rating > team2_rating:
            team1_wins = int(total_matches * (0.5 + (team1_rating - team2_rating) / 100))
        else:
            team1_wins = int(total_matches * (0.5 - (team2_rating - team1_rating) / 100))
        
        team2_wins = total_matches - team1_wins
        
        return {
            'total_matches': total_matches,
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'team1_win_pct': (team1_wins / total_matches) * 100 if total_matches > 0 else 50,
            'team2_win_pct': (team2_wins / total_matches) * 100 if total_matches > 0 else 50
        }
    
    def get_player_to_watch(self, team: str, venue: str) -> str:
        """Get key player to watch for the match"""
        team_players = self.player_stats_df[self.player_stats_df['team'] == team]
        
        # Look for best performer (batting average for batters)
        batters = team_players[team_players['role'].isin(['Batter', 'All-rounder'])]
        batters = batters[batters['bat_avg_first'] > 0]
        
        if len(batters) > 0:
            best_batter = batters.loc[batters['bat_avg_first'].idxmax()]
            avg = best_batter['bat_avg_first']
            sr = best_batter['bat_sr_first']
            return f"{best_batter['player']} (avg {avg}, SR {sr})"
        
        # Fallback to bowlers
        bowlers = team_players[team_players['role'].isin(['Bowler', 'All-rounder'])]
        bowlers = bowlers[bowlers['bowl_econ_first'] > 0]
        
        if len(bowlers) > 0:
            best_bowler = bowlers.loc[bowlers['bowl_econ_first'].idxmin()]
            econ = best_bowler['bowl_econ_first']
            return f"{best_bowler['player']} (economy {econ})"
        
        return "Key player stats unavailable"
    
    def calculate_win_probability(self, match_id: int, toss_winner: str, toss_decision: str) -> Dict:
        """
        Calculate win probability for a match
        
        Args:
            match_id: Match ID from schedule
            toss_winner: 'Team A' or 'Team B' (team1 or team2)
            toss_decision: 'Bat' or 'Bowl'
        
        Returns:
            Dictionary with win probabilities and analysis
        """
        
        # Get match details
        match_details = self.get_match_details(match_id)
        team1 = match_details['team1']
        team2 = match_details['team2']
        venue = match_details['venue']
        
        # Get team ratings
        team1_ratings = self.get_team_rating(team1)
        team2_ratings = self.get_team_rating(team2)
        
        # Get venue impact
        venue_impact = self.get_venue_impact(venue)
        
        # Get head-to-head
        h2h = self.get_head_to_head_record(team1, team2)
        
        # Base calculation: Team batting strength vs opponent bowling strength
        team1_bat_vs_team2_bowl = team1_ratings['batting'] / (team2_ratings['bowling'] + 20) * 100
        team2_bat_vs_team1_bowl = team2_ratings['batting'] / (team1_ratings['bowling'] + 20) * 100
        
        # Venue impact factor
        venue_bat_impact = venue_impact['bat_first_win_pct'] / 50.0  # Normalize around 1.0
        venue_bowl_impact = venue_impact['bowl_first_win_pct'] / 50.0
        
        # Apply venue impact
        if venue_impact['bat_first_win_pct'] > 50:  # Batting friendly venue
            team1_bat_vs_team2_bowl *= venue_bat_impact
            team2_bat_vs_team1_bowl *= venue_bat_impact
        else:  # Bowling friendly venue  
            team1_bat_vs_team2_bowl *= venue_bowl_impact
            team2_bat_vs_team1_bowl *= venue_bowl_impact
        
        # Base win probability (50-50 split, adjusted by team strength difference)
        base_prob_team1 = 50 + (team1_ratings['overall'] - team2_ratings['overall']) * 1.5
        base_prob_team2 = 100 - base_prob_team1
        
        # Apply head-to-head factor (10% weight)
        h2h_factor = 0.1
        base_prob_team1 = base_prob_team1 * (1 - h2h_factor) + h2h['team1_win_pct'] * h2h_factor
        base_prob_team2 = 100 - base_prob_team1
        
        # Apply toss advantage
        toss_advantage = 15.0  # 15% advantage for winning toss and making preferred choice
        
        # Determine who benefits from toss
        if toss_winner == 'Team A':  # team1 wins toss
            if toss_decision == 'Bat':
                if venue_impact['bat_first_win_pct'] > 50:  # Good decision
                    base_prob_team1 += toss_advantage
                else:  # Suboptimal decision
                    base_prob_team1 += toss_advantage * 0.5
            else:  # Bowl first
                if venue_impact['bowl_first_win_pct'] > 50:  # Good decision
                    base_prob_team1 += toss_advantage
                else:  # Suboptimal decision
                    base_prob_team1 += toss_advantage * 0.5
        else:  # team2 wins toss
            if toss_decision == 'Bat':
                if venue_impact['bat_first_win_pct'] > 50:  # Good decision
                    base_prob_team2 += toss_advantage
                else:  # Suboptimal decision
                    base_prob_team2 += toss_advantage * 0.5
            else:  # Bowl first
                if venue_impact['bowl_first_win_pct'] > 50:  # Good decision
                    base_prob_team2 += toss_advantage
                else:  # Suboptimal decision
                    base_prob_team2 += toss_advantage * 0.5
        
        # Normalize probabilities
        total_prob = base_prob_team1 + base_prob_team2
        if total_prob != 100:
            base_prob_team1 = (base_prob_team1 / total_prob) * 100
            base_prob_team2 = (base_prob_team2 / total_prob) * 100
        
        # Ensure probabilities are within reasonable bounds
        base_prob_team1 = max(15, min(85, base_prob_team1))
        base_prob_team2 = 100 - base_prob_team1
        
        # Determine key factor
        key_factors = []
        if venue_impact['bat_first_win_pct'] > 55:
            key_factors.append("Venue favors batting first teams")
        elif venue_impact['bowl_first_win_pct'] > 55:
            key_factors.append("Venue favors chasing teams")
        
        if abs(team1_ratings['overall'] - team2_ratings['overall']) > 3:
            stronger_team = team1 if team1_ratings['overall'] > team2_ratings['overall'] else team2
            key_factors.append(f"{stronger_team} has higher overall rating")
        
        if not key_factors:
            key_factors.append("Evenly matched teams")
        
        key_factor = "; ".join(key_factors)
        
        # Get players to watch
        team1_player = self.get_player_to_watch(team1, venue)
        team2_player = self.get_player_to_watch(team2, venue)
        
        return {
            'team1': team1,
            'team2': team2,
            'venue': venue,
            'win_prob': [round(base_prob_team1, 1), round(base_prob_team2, 1)],
            'key_factor': key_factor,
            'player_to_watch': f"{team1}: {team1_player}; {team2}: {team2_player}",
            'venue_impact': f"Bat first: {venue_impact['bat_first_win_pct']:.0f}%, Bowl first: {venue_impact['bowl_first_win_pct']:.0f}%",
            'head_to_head': f"{team1} {h2h['team1_wins']}-{h2h['team2_wins']} {team2}",
            'toss_impact': f"Toss won by {toss_winner}, chose to {toss_decision.lower()}"
        }


def main():
    """Main function for testing match analyzer"""
    print("Testing Match Analyzer...")
    
    analyzer = MatchAnalyzer()
    
    # Test with a few sample matches
    test_matches = [
        {'match_id': 1, 'toss_winner': 'Team A', 'toss_decision': 'Bat'},
        {'match_id': 5, 'toss_winner': 'Team B', 'toss_decision': 'Bowl'},
        {'match_id': 10, 'toss_winner': 'Team A', 'toss_decision': 'Bat'}
    ]
    
    for test in test_matches:
        print(f"\n--- Match ID {test['match_id']} ---")
        result = analyzer.calculate_win_probability(
            test['match_id'], 
            test['toss_winner'], 
            test['toss_decision']
        )
        
        print(f"Match: {result['team1']} vs {result['team2']}")
        print(f"Venue: {result['venue']}")
        print(f"Win Probability: {result['team1']} {result['win_prob'][0]}% - {result['win_prob'][1]}% {result['team2']}")
        print(f"Key Factor: {result['key_factor']}")
        print(f"Toss: {result['toss_impact']}")
        print(f"Players to Watch: {result['player_to_watch']}")


if __name__ == "__main__":
    main()