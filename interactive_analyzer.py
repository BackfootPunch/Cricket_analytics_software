#!/usr/bin/env python3
"""
Interactive Cricket Analytics Command-Line Interface
Allows real-time exploration of matches, teams, and predictions
"""

import pandas as pd
from match_analyzer import MatchAnalyzer
import config

class InteractiveCricketAnalyzer:
    def __init__(self):
        self.analyzer = MatchAnalyzer()
        self.schedule_df = pd.read_csv(config.SCHEDULE_FILE)
        self.team_ratings_df = pd.read_csv(config.TEAM_RATINGS_FILE)
        
    def show_banner(self):
        """Display interactive analyzer banner"""
        print("🏏" + "="*60 + "🏏")
        print("    THE HUNDRED INTERACTIVE CRICKET ANALYZER")
        print("🏏" + "="*60 + "🏏")
        print("Real-time match analysis and predictions")
        print("Type 'help' for commands or 'quit' to exit")
        print("-" * 62)
    
    def show_help(self):
        """Show available commands"""
        print("\n📋 AVAILABLE COMMANDS:")
        print("-" * 30)
        print("🎯 analyze [match_id] - Analyze specific match")
        print("📅 schedule - Show tournament schedule")
        print("🏆 teams - Show team ratings")
        print("🏟️ venues - Show venue statistics")
        print("🎲 simulate [match_id] - Run match scenarios")
        print("📊 compare [team1] vs [team2] - Compare teams")
        print("❓ help - Show this help")
        print("🚪 quit - Exit analyzer")
        print("-" * 30)
    
    def show_schedule(self):
        """Display tournament schedule"""
        print("\n📅 THE HUNDRED 2025 SCHEDULE:")
        print("-" * 80)
        for _, match in self.schedule_df.head(10).iterrows():  # Show first 10
            print(f"Match {match['Match_ID']:2d}: {match['Team1']} vs {match['Team2']}")
            print(f"          {match['Date']} at {match['Venue']}")
        
        if len(self.schedule_df) > 10:
            print(f"\n... and {len(self.schedule_df) - 10} more matches")
        print(f"\n📊 Total: {len(self.schedule_df)} matches across 8 teams")
    
    def show_teams(self):
        """Display team ratings"""
        print("\n🏆 TEAM STRENGTH RANKINGS:")
        print("-" * 60)
        ranked_teams = self.team_ratings_df.sort_values('Overall_Rating', ascending=False)
        
        for i, (_, team) in enumerate(ranked_teams.iterrows(), 1):
            medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 5
            print(f"{medals[i-1]} {i}. {team['Team']:<25} Rating: {team['Overall_Rating']:4.1f}")
            print(f"     Batting: {team['Bat_Rating']:4.1f} | Bowling: {team['Bowl_Rating']:4.1f}")
    
    def analyze_match(self, match_id):
        """Analyze a specific match with multiple scenarios"""
        try:
            match_id = int(match_id)
            match_details = self.analyzer.get_match_details(match_id)
            
            print(f"\n🎯 MATCH {match_id} ANALYSIS:")
            print("=" * 50)
            print(f"📍 {match_details['team1']} vs {match_details['team2']}")
            print(f"🏟️ Venue: {match_details['venue']}")
            print(f"📅 Date: {match_details['date']} at {match_details['time']}")
            print("-" * 50)
            
            # Analyze different toss scenarios
            scenarios = [
                ("Team A", "Bat", f"{match_details['team1']} wins toss, bats first"),
                ("Team A", "Bowl", f"{match_details['team1']} wins toss, bowls first"),
                ("Team B", "Bat", f"{match_details['team2']} wins toss, bats first"),
                ("Team B", "Bowl", f"{match_details['team2']} wins toss, bowls first")
            ]
            
            print("🎲 TOSS SCENARIO ANALYSIS:")
            for toss_winner, decision, description in scenarios:
                result = self.analyzer.calculate_win_probability(match_id, toss_winner, decision)
                print(f"\n🏏 {description}:")
                print(f"   Win Probability: {result['team1']} {result['win_prob'][0]:.1f}% - {result['win_prob'][1]:.1f}% {result['team2']}")
                print(f"   Key Factor: {result['key_factor']}")
            
            # Show additional insights
            result = self.analyzer.calculate_win_probability(match_id, "Team A", "Bat")
            print(f"\n💡 ADDITIONAL INSIGHTS:")
            print(f"   🏟️ {result['venue_impact']}")
            print(f"   ⭐ {result['player_to_watch']}")
            
        except ValueError:
            print("❌ Please enter a valid match ID (number)")
        except Exception as e:
            print(f"❌ Error analyzing match: {e}")
    
    def simulate_match(self, match_id):
        """Run multiple simulations for a match"""
        try:
            match_id = int(match_id)
            match_details = self.analyzer.get_match_details(match_id)
            
            print(f"\n🎲 MATCH {match_id} SIMULATION:")
            print("=" * 50)
            print(f"📍 {match_details['team1']} vs {match_details['team2']}")
            print("-" * 50)
            
            # Simulate 10 different scenarios with random toss
            import random
            results = []
            
            for i in range(10):
                toss_winner = random.choice(["Team A", "Team B"])
                decision = random.choice(["Bat", "Bowl"])
                
                result = self.analyzer.calculate_win_probability(match_id, toss_winner, decision)
                results.append(result['win_prob'][0])
                
                team_won_toss = match_details['team1'] if toss_winner == "Team A" else match_details['team2']
                print(f"Sim {i+1:2d}: {team_won_toss} wins toss, {decision.lower()}s → {match_details['team1']} {result['win_prob'][0]:.1f}% - {result['win_prob'][1]:.1f}% {match_details['team2']}")
            
            # Show summary statistics
            avg_prob = sum(results) / len(results)
            min_prob = min(results)
            max_prob = max(results)
            
            print(f"\n📊 SIMULATION SUMMARY:")
            print(f"   Average {match_details['team1']} win probability: {avg_prob:.1f}%")
            print(f"   Range: {min_prob:.1f}% - {max_prob:.1f}%")
            print(f"   Toss impact: ±{(max_prob - min_prob)/2:.1f}%")
            
        except ValueError:
            print("❌ Please enter a valid match ID (number)")
        except Exception as e:
            print(f"❌ Error simulating match: {e}")
    
    def compare_teams(self, team1, team2):
        """Compare two teams"""
        # Find teams (case insensitive, partial match)
        all_teams = self.team_ratings_df['Team'].tolist()
        
        team1_matches = [t for t in all_teams if team1.lower() in t.lower()]
        team2_matches = [t for t in all_teams if team2.lower() in t.lower()]
        
        if not team1_matches:
            print(f"❌ Team '{team1}' not found. Available: {', '.join(all_teams)}")
            return
        if not team2_matches:
            print(f"❌ Team '{team2}' not found. Available: {', '.join(all_teams)}")
            return
        
        team1_full = team1_matches[0]
        team2_full = team2_matches[0]
        
        team1_data = self.team_ratings_df[self.team_ratings_df['Team'] == team1_full].iloc[0]
        team2_data = self.team_ratings_df[self.team_ratings_df['Team'] == team2_full].iloc[0]
        
        print(f"\n⚔️ TEAM COMPARISON: {team1_full} vs {team2_full}")
        print("=" * 70)
        
        categories = [
            ("Overall Rating", "Overall_Rating"),
            ("Batting Strength", "Bat_Rating"),
            ("Bowling Strength", "Bowl_Rating")
        ]
        
        for category, col in categories:
            val1 = team1_data[col]
            val2 = team2_data[col]
            
            if val1 > val2:
                advantage = f"{team1_full} +{val1-val2:.1f}"
                symbol = "🔹"
            elif val2 > val1:
                advantage = f"{team2_full} +{val2-val1:.1f}"
                symbol = "🔸"
            else:
                advantage = "Even"
                symbol = "⚖️"
            
            print(f"{symbol} {category:15}: {val1:5.1f} vs {val2:5.1f} → {advantage}")
        
        # Show head-to-head prediction
        sample_match = self.schedule_df[
            ((self.schedule_df['Team1'] == team1_full) & (self.schedule_df['Team2'] == team2_full)) |
            ((self.schedule_df['Team1'] == team2_full) & (self.schedule_df['Team2'] == team1_full))
        ]
        
        if len(sample_match) > 0:
            match_id = sample_match.iloc[0]['Match_ID']
            result = self.analyzer.calculate_win_probability(match_id, "Team A", "Bat")
            print(f"\n🎯 HEAD-TO-HEAD PREDICTION:")
            print(f"   {result['team1']} {result['win_prob'][0]:.1f}% - {result['win_prob'][1]:.1f}% {result['team2']}")
    
    def run(self):
        """Main interactive loop"""
        self.show_banner()
        
        while True:
            try:
                command = input("\n🏏 Enter command: ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("👋 Thanks for using The Hundred Analytics!")
                    break
                elif command == 'help':
                    self.show_help()
                elif command == 'schedule':
                    self.show_schedule()
                elif command == 'teams':
                    self.show_teams()
                elif command.startswith('analyze '):
                    match_id = command.split()[1]
                    self.analyze_match(match_id)
                elif command.startswith('simulate '):
                    match_id = command.split()[1]
                    self.simulate_match(match_id)
                elif 'vs' in command and command.startswith('compare'):
                    parts = command.replace('compare ', '').split(' vs ')
                    if len(parts) == 2:
                        self.compare_teams(parts[0].strip(), parts[1].strip())
                    else:
                        print("❌ Use format: compare [team1] vs [team2]")
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 Thanks for using The Hundred Analytics!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Run interactive analyzer"""
    analyzer = InteractiveCricketAnalyzer()
    analyzer.run()

if __name__ == "__main__":
    main()