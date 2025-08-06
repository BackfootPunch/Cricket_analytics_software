#!/usr/bin/env python3
"""
Demo script to showcase The Hundred Analytics System capabilities
"""

import pandas as pd
from match_analyzer import MatchAnalyzer
import config

def demo_banner():
    """Display demo banner"""
    print("=" * 70)
    print("🏏 THE HUNDRED ANALYTICS SYSTEM - DEMO")
    print("=" * 70)
    print("Showcasing cricket analytics capabilities for The Hundred 2025")
    print("=" * 70)

def demo_data_overview():
    """Show data overview"""
    print("\n📊 DATA OVERVIEW:")
    print("-" * 40)
    
    # Load data files
    schedule_df = pd.read_csv(config.SCHEDULE_FILE)
    squads_df = pd.read_csv(config.SQUADS_FILE)
    team_ratings_df = pd.read_csv(config.TEAM_RATINGS_FILE)
    venue_stats_df = pd.read_csv(config.VENUE_STATS_FILE)
    tournament_df = pd.read_csv(config.OUTPUTS_DIR + "/tournament_analysis.csv")
    
    print(f"📅 Total Matches: {len(schedule_df)}")
    print(f"👥 Total Players: {len(squads_df)}")
    print(f"🏟️ Venues: {len(venue_stats_df)}")
    print(f"⚡ Teams: {len(team_ratings_df)}")
    
    print(f"\n🏆 TOP 3 TEAMS BY RATING:")
    top_teams = team_ratings_df.nlargest(3, 'Overall_Rating')
    for i, (_, team) in enumerate(top_teams.iterrows(), 1):
        print(f"{i}. {team['Team']}: {team['Overall_Rating']} (Bat: {team['Bat_Rating']}, Bowl: {team['Bowl_Rating']})")

def demo_match_analysis():
    """Demonstrate match analysis capabilities"""
    print("\n🎯 MATCH ANALYSIS DEMO:")
    print("-" * 40)
    
    analyzer = MatchAnalyzer()
    
    # Demo matches
    demo_matches = [
        {"id": 1, "description": "Opening Match - London Spirit vs Oval Invincibles"},
        {"id": 15, "description": "High-scoring venue - Trent Bridge"},
        {"id": 29, "description": "London Derby - Oval Invincibles vs London Spirit"}
    ]
    
    for match in demo_matches:
        print(f"\n📍 {match['description']}:")
        
        # Analyze with different toss scenarios
        scenarios = [
            ("Team A", "Bat", "Batting first"),
            ("Team B", "Bowl", "Bowling first")
        ]
        
        for toss_winner, toss_decision, desc in scenarios:
            result = analyzer.calculate_win_probability(match["id"], toss_winner, toss_decision)
            print(f"   {desc}: {result['team1']} {result['win_prob'][0]}% - {result['win_prob'][1]}% {result['team2']}")

def demo_tournament_predictions():
    """Show tournament predictions"""
    print("\n🏆 TOURNAMENT PREDICTIONS (1000 simulations):")
    print("-" * 40)
    
    tournament_df = pd.read_csv(config.OUTPUTS_DIR + "/tournament_analysis.csv")
    tournament_df = tournament_df.sort_values('Win_Probability_%', ascending=False)
    
    print("🥇 CHAMPIONSHIP CONTENDERS:")
    for i, (_, team) in enumerate(tournament_df.head(4).iterrows(), 1):
        print(f"{i}. {team['Team']}: {team['Win_Probability_%']}% win | {team['Playoff_Probability_%']}% playoffs")
    
    print("\n📊 PLAYOFF BUBBLE:")
    bubble_teams = tournament_df.iloc[4:6]
    for _, team in bubble_teams.iterrows():
        print(f"   {team['Team']}: {team['Win_Probability_%']}% win | {team['Playoff_Probability_%']}% playoffs")

def demo_venue_insights():
    """Show venue analysis"""
    print("\n🏟️ VENUE INSIGHTS:")
    print("-" * 40)
    
    venue_stats_df = pd.read_csv(config.VENUE_STATS_FILE)
    
    # Most batting friendly
    bat_friendly = venue_stats_df.loc[venue_stats_df['win_percent_bat_first'].idxmax()]
    print(f"🏏 Most Batting Friendly: {bat_friendly['venue']}")
    print(f"   Batting first wins: {bat_friendly['win_percent_bat_first']}%")
    print(f"   Average score: {bat_friendly['avg_first_innings_score']}")
    
    # Most bowling friendly  
    bowl_friendly = venue_stats_df.loc[venue_stats_df['win_percent_bat_first'].idxmin()]
    print(f"\n⚡ Most Bowling Friendly: {bowl_friendly['venue']}")
    print(f"   Batting first wins: {bowl_friendly['win_percent_bat_first']}%")
    print(f"   Chasing teams win: {bowl_friendly['win_percent_bowl_first']}%")
    
    # Highest scoring
    high_scoring = venue_stats_df.loc[venue_stats_df['avg_first_innings_score'].idxmax()]
    print(f"\n🚀 Highest Scoring: {high_scoring['venue']}")
    print(f"   Average first innings: {high_scoring['avg_first_innings_score']}")
    print(f"   Run rate: {high_scoring['run_rate']}")

def demo_key_matches():
    """Show key matches to watch"""
    print("\n🔥 KEY MATCHES TO WATCH:")
    print("-" * 40)
    
    crucial_df = pd.read_csv(config.OUTPUTS_DIR + "/crucial_matches.csv")
    
    print("📈 MOST CRUCIAL MATCHES (close contests between top teams):")
    for i, (_, match) in enumerate(crucial_df.head(5).iterrows(), 1):
        print(f"{i}. {match['teams']} at {match['venue']}")
        print(f"   Winner: {match['winner']} | Importance: {match['importance_score']}")
        print()

def demo_dashboard_info():
    """Show dashboard information"""
    print("\n🚀 INTERACTIVE DASHBOARD:")
    print("-" * 40)
    print("Launch the full interactive dashboard with:")
    print("   python hundred_analytics_dash.py")
    print()
    print("Dashboard Features:")
    print("✅ Match-by-match probability analysis")
    print("✅ Real-time toss impact simulation")
    print("✅ Team strength radar comparisons")
    print("✅ Venue impact visualizations")
    print("✅ Player matchup heatmaps")
    print("✅ Tournament bracket predictions")
    print()
    print("Dashboard URL: http://127.0.0.1:8050")

def main():
    """Main demo function"""
    demo_banner()
    demo_data_overview()
    demo_match_analysis()
    demo_tournament_predictions()
    demo_venue_insights() 
    demo_key_matches()
    demo_dashboard_info()
    
    print("\n" + "=" * 70)
    print("🎯 DEMO COMPLETE - The Hundred Analytics System Ready!")
    print("=" * 70)

if __name__ == "__main__":
    main()