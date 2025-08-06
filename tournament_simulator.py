#!/usr/bin/env python3
"""
Tournament Simulator for The Hundred
Monte Carlo simulation engine for tournament predictions
"""

import pandas as pd
import numpy as np
import random
from collections import defaultdict, Counter
from typing import Dict, List
import config
from match_analyzer import MatchAnalyzer

class TournamentSimulator:
    def __init__(self, num_simulations: int = 1000):
        self.num_simulations = num_simulations
        self.schedule_df = pd.read_csv(config.SCHEDULE_FILE)
        self.team_ratings_df = pd.read_csv(config.TEAM_RATINGS_FILE)
        self.venue_stats_df = pd.read_csv(config.VENUE_STATS_FILE)
        
        self.analyzer = MatchAnalyzer()
        self.teams = self.team_ratings_df['Team'].tolist()
        
        # Initialize results tracking
        self.simulation_results = []
        
    def simulate_optimal_toss_decision(self, venue: str) -> str:
        """Determine optimal toss decision based on venue stats"""
        venue_data = self.venue_stats_df[self.venue_stats_df['venue'] == venue]
        
        if len(venue_data) == 0:
            return random.choice(['Bat', 'Bowl'])
        
        bat_first_win_pct = venue_data.iloc[0]['win_percent_bat_first']
        
        # Choose the decision with higher win percentage, with some randomness
        if bat_first_win_pct > 52:
            return 'Bat' if random.random() > 0.2 else 'Bowl'  # 80% chance of optimal choice
        elif bat_first_win_pct < 48:
            return 'Bowl' if random.random() > 0.2 else 'Bat'  # 80% chance of optimal choice
        else:
            return random.choice(['Bat', 'Bowl'])  # Neutral venue
    
    def simulate_single_match(self, match_data: dict) -> dict:
        """Simulate a single match with optimal toss decisions"""
        match_id = match_data['Match_ID']
        team1 = match_data['Team1']
        team2 = match_data['Team2']
        venue = match_data['Venue']
        
        # Determine toss winner (50-50)
        toss_winner = random.choice(['Team A', 'Team B'])
        
        # Make optimal toss decision
        toss_decision = self.simulate_optimal_toss_decision(venue)
        
        # Calculate win probability using the match analyzer
        match_result = self.analyzer.calculate_win_probability(
            match_id, toss_winner, toss_decision
        )
        
        # Simulate match outcome based on probabilities
        team1_prob = match_result['win_prob'][0] / 100
        
        if random.random() < team1_prob:
            winner = team1
            loser = team2
        else:
            winner = team2
            loser = team1
        
        return {
            'match_id': match_id,
            'team1': team1,
            'team2': team2,
            'venue': venue,
            'winner': winner,
            'loser': loser,
            'win_prob_team1': match_result['win_prob'][0],
            'win_prob_team2': match_result['win_prob'][1],
            'toss_winner': toss_winner,
            'toss_decision': toss_decision
        }
    
    def simulate_group_stage(self) -> dict:
        """Simulate the group stage and return team standings"""
        team_stats = {team: {'wins': 0, 'losses': 0, 'points': 0} for team in self.teams}
        match_results = []
        
        # Simulate all matches
        for _, match in self.schedule_df.iterrows():
            result = self.simulate_single_match(match)
            match_results.append(result)
            
            # Update team stats (2 points for win, 0 for loss)
            team_stats[result['winner']]['wins'] += 1
            team_stats[result['winner']]['points'] += 2
            team_stats[result['loser']]['losses'] += 1
        
        # Convert to DataFrame for easier manipulation
        standings = []
        for team, stats in team_stats.items():
            standings.append({
                'team': team,
                'wins': stats['wins'],
                'losses': stats['losses'],
                'points': stats['points']
            })
        
        standings_df = pd.DataFrame(standings).sort_values('points', ascending=False)
        
        return {
            'standings': standings_df,
            'match_results': match_results
        }
    
    def determine_playoffs(self, standings_df: pd.DataFrame) -> dict:
        """Determine playoff teams (top 3 + eliminator)"""
        # In The Hundred format: Top 3 qualify directly, 4th and 5th play eliminator
        standings_df = standings_df.sort_values('points', ascending=False)
        
        top_3 = standings_df.head(3)['team'].tolist()
        eliminator_teams = standings_df.iloc[3:5]['team'].tolist() if len(standings_df) >= 5 else []
        
        return {
            'top_3': top_3,
            'eliminator': eliminator_teams,
            'final_4': top_3 + eliminator_teams[:1] if eliminator_teams else top_3
        }
    
    def simulate_playoffs(self, playoff_teams: dict) -> str:
        """Simulate playoff matches and return tournament winner"""
        
        if len(playoff_teams['top_3']) < 3:
            return playoff_teams['top_3'][0] if playoff_teams['top_3'] else self.teams[0]
        
        # Simplified playoff simulation
        # In real Hundred: Eliminator, then Final
        # Here we simulate a final between top 2 teams
        
        team1 = playoff_teams['top_3'][0]  # Highest ranked
        team2 = playoff_teams['top_3'][1]  # Second highest
        
        # Create a dummy match for the final
        final_match = {
            'Match_ID': 999,  # Dummy ID
            'Team1': team1,
            'Team2': team2,
            'Venue': "Lord's, London"  # Traditional final venue
        }
        
        final_result = self.simulate_single_match(final_match)
        return final_result['winner']
    
    def run_simulation(self) -> dict:
        """Run a single tournament simulation"""
        group_result = self.simulate_group_stage()
        standings = group_result['standings']
        match_results = group_result['match_results']
        
        playoff_teams = self.determine_playoffs(standings)
        winner = self.simulate_playoffs(playoff_teams)
        
        return {
            'winner': winner,
            'standings': standings,
            'playoff_teams': playoff_teams,
            'match_results': match_results
        }
    
    def run_multiple_simulations(self) -> dict:
        """Run multiple tournament simulations"""
        print(f"Running {self.num_simulations} tournament simulations...")
        
        winners = []
        playoff_appearances = defaultdict(int)
        final_standings = defaultdict(list)
        all_match_results = []
        
        for i in range(self.num_simulations):
            if (i + 1) % 100 == 0:
                print(f"Completed {i + 1} simulations...")
            
            sim_result = self.run_simulation()
            
            # Track winners
            winners.append(sim_result['winner'])
            
            # Track playoff appearances
            for team in sim_result['playoff_teams']['top_3']:
                playoff_appearances[team] += 1
            for team in sim_result['playoff_teams']['eliminator']:
                playoff_appearances[team] += 1
            
            # Track final standings
            for _, row in sim_result['standings'].iterrows():
                final_standings[row['team']].append(row['points'])
            
            # Store match results (only from first simulation for analysis)
            if i == 0:
                all_match_results = sim_result['match_results']
        
        return {
            'winners': winners,
            'playoff_appearances': playoff_appearances,
            'final_standings': final_standings,
            'sample_match_results': all_match_results
        }
    
    def analyze_results(self, simulation_data: dict) -> pd.DataFrame:
        """Analyze simulation results and create summary"""
        winners = simulation_data['winners']
        playoff_appearances = simulation_data['playoff_appearances']
        
        # Calculate probabilities
        winner_counts = Counter(winners)
        
        analysis = []
        for team in self.teams:
            win_probability = (winner_counts[team] / self.num_simulations) * 100
            playoff_probability = (playoff_appearances[team] / self.num_simulations) * 100
            
            analysis.append({
                'Team': team,
                'Win_Probability_%': round(win_probability, 1),
                'Playoff_Probability_%': round(playoff_probability, 1),
                'Titles_Won': winner_counts[team],
                'Playoff_Appearances': playoff_appearances[team]
            })
        
        analysis_df = pd.DataFrame(analysis).sort_values('Win_Probability_%', ascending=False)
        return analysis_df
    
    def find_crucial_matches(self, match_results: List[dict]) -> List[dict]:
        """Identify most crucial matches (biggest point swings)"""
        
        # For simplicity, identify matches between top teams
        top_teams = self.team_ratings_df.nlargest(4, 'Overall_Rating')['Team'].tolist()
        
        crucial_matches = []
        for match in match_results:
            if match['team1'] in top_teams and match['team2'] in top_teams:
                # Calculate importance based on how close the probability was
                prob_diff = abs(match['win_prob_team1'] - match['win_prob_team2'])
                importance = 100 - prob_diff  # Higher importance for closer matches
                
                crucial_matches.append({
                    'match_id': match['match_id'],
                    'teams': f"{match['team1']} vs {match['team2']}",
                    'venue': match['venue'],
                    'winner': match['winner'],
                    'importance_score': round(importance, 1),
                    'prob_difference': round(prob_diff, 1)
                })
        
        # Sort by importance
        crucial_matches.sort(key=lambda x: x['importance_score'], reverse=True)
        return crucial_matches[:5]  # Top 5 crucial matches
    
    def create_match_predictions(self, match_results: List[dict]) -> pd.DataFrame:
        """Create match-by-match predictions CSV"""
        predictions = []
        
        for match in match_results:
            predictions.append({
                'Match_ID': match['match_id'],
                'Team1': match['team1'],
                'Team2': match['team2'],
                'Venue': match['venue'],
                'Predicted_Winner': match['winner'],
                'Team1_Win_Prob_%': round(match['win_prob_team1'], 1),
                'Team2_Win_Prob_%': round(match['win_prob_team2'], 1),
                'Toss_Winner': match['toss_winner'],
                'Toss_Decision': match['toss_decision']
            })
        
        return pd.DataFrame(predictions)
    
    def save_results(self, analysis_df: pd.DataFrame, predictions_df: pd.DataFrame, crucial_matches: List[dict]):
        """Save all results to files"""
        
        # Save main analysis
        analysis_file = config.OUTPUTS_DIR + "/tournament_analysis.csv"
        analysis_df.to_csv(analysis_file, index=False)
        print(f"Tournament analysis saved to: {analysis_file}")
        
        # Save match predictions
        predictions_df.to_csv(config.TOURNAMENT_PREDICTIONS_FILE, index=False)
        print(f"Match predictions saved to: {config.TOURNAMENT_PREDICTIONS_FILE}")
        
        # Save crucial matches
        crucial_file = config.OUTPUTS_DIR + "/crucial_matches.csv"
        pd.DataFrame(crucial_matches).to_csv(crucial_file, index=False)
        print(f"Crucial matches saved to: {crucial_file}")
        
        # Display summary
        print(f"\n=== TOURNAMENT SIMULATION RESULTS ({self.num_simulations} simulations) ===")
        print("\nWin Probabilities:")
        print(analysis_df[['Team', 'Win_Probability_%', 'Playoff_Probability_%']].to_string(index=False))
        
        print(f"\nTop 3 Crucial Matches:")
        for i, match in enumerate(crucial_matches[:3], 1):
            print(f"{i}. {match['teams']} at {match['venue']} (Importance: {match['importance_score']})")


def main():
    """Main function to run tournament simulation"""
    print("Starting Tournament Simulation...")
    
    # Run simulation with 1000 iterations
    simulator = TournamentSimulator(num_simulations=1000)
    
    # Run simulations
    results = simulator.run_multiple_simulations()
    
    # Analyze results
    analysis = simulator.analyze_results(results)
    
    # Find crucial matches
    crucial_matches = simulator.find_crucial_matches(results['sample_match_results'])
    
    # Create match predictions
    predictions = simulator.create_match_predictions(results['sample_match_results'])
    
    # Save all results
    simulator.save_results(analysis, predictions, crucial_matches)
    
    print("\nTournament simulation complete!")


if __name__ == "__main__":
    main()