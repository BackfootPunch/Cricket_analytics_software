#!/usr/bin/env python3
"""
Advanced Demo - Interactive Cricket Analytics Exploration
Shows advanced features and detailed analysis capabilities
"""

import pandas as pd
from match_analyzer import MatchAnalyzer
from tournament_simulator import TournamentSimulator
import config

def advanced_match_analysis():
    """Demonstrate advanced match analysis with multiple scenarios"""
    print("🎯 ADVANCED MATCH ANALYSIS")
    print("=" * 50)
    
    analyzer = MatchAnalyzer()
    
    # Analyze high-profile matches with different scenarios
    key_matches = [
        {"id": 1, "desc": "Tournament Opener", "teams": "London Spirit vs Oval Invincibles"},
        {"id": 29, "desc": "London Derby Return", "teams": "Oval Invincibles vs London Spirit"},
        {"id": 15, "desc": "High-Scoring Venue", "teams": "Trent Rockets vs Southern Brave"},
        {"id": 25, "desc": "Top Teams Clash", "teams": "Northern Superchargers vs Oval Invincibles"}
    ]
    
    for match in key_matches:
        print(f"\n📍 {match['desc']}: {match['teams']}")
        print("-" * 40)
        
        # Test both toss scenarios
        scenarios = [
            ("Team A", "Bat", "🏏"),
            ("Team A", "Bowl", "⚡"),
            ("Team B", "Bat", "🏏"),
            ("Team B", "Bowl", "⚡")
        ]
        
        for toss_winner, decision, emoji in scenarios:
            result = analyzer.calculate_win_probability(match["id"], toss_winner, decision)
            toss_impact = f"Team A wins toss, {decision.lower()}s" if toss_winner == "Team A" else f"Team B wins toss, {decision.lower()}s"
            
            print(f"{emoji} {toss_impact}: {result['team1']} {result['win_prob'][0]:.1f}% - {result['win_prob'][1]:.1f}% {result['team2']}")
    
def venue_deep_dive():
    """Deep analysis of venue characteristics"""
    print("\n\n🏟️ VENUE DEEP DIVE ANALYSIS")
    print("=" * 50)
    
    venue_df = pd.read_csv(config.VENUE_STATS_FILE)
    
    for _, venue in venue_df.iterrows():
        print(f"\n📍 {venue['venue']}")
        print("-" * 30)
        print(f"   🏏 Bat First Success: {venue['win_percent_bat_first']:.0f}%")
        print(f"   ⚡ Bowl First Success: {venue['win_percent_bowl_first']:.0f}%")
        print(f"   📊 Avg Score: {venue['avg_first_innings_score']:.0f}")
        print(f"   🚀 Run Rate: {venue['run_rate']:.1f}")
        print(f"   📈 Total Runs: {venue['total_runs']:,}")
        print(f"   🎯 Total Wickets: {venue['total_wickets']}")
        
        # Determine venue character
        if venue['win_percent_bat_first'] > 50:
            character = "🏏 BATTER'S PARADISE"
        else:
            character = "⚡ BOWLER'S DREAM"
        print(f"   🏟️ Character: {character}")

def team_strength_breakdown():
    """Detailed team strength analysis"""
    print("\n\n⚡ TEAM STRENGTH DETAILED BREAKDOWN")
    print("=" * 50)
    
    team_ratings_df = pd.read_csv(config.TEAM_RATINGS_FILE)
    player_stats_df = pd.read_csv(config.PLAYER_STATS_FILE)
    
    for _, team in team_ratings_df.iterrows():
        print(f"\n🏏 {team['Team']}")
        print("-" * 30)
        print(f"   📊 Overall Rating: {team['Overall_Rating']:.1f}")
        print(f"   🏏 Batting Strength: {team['Bat_Rating']:.1f}")
        print(f"   ⚡ Bowling Strength: {team['Bowl_Rating']:.1f}")
        
        # Get top players
        team_players = player_stats_df[player_stats_df['team'] == team['Team']]
        
        # Top batter
        batters = team_players[team_players['role'].isin(['Batter', 'All-rounder'])]
        batters = batters[batters['bat_avg_first'] > 0]
        if len(batters) > 0:
            top_batter = batters.loc[batters['bat_avg_first'].idxmax()]
            print(f"   🌟 Top Batter: {top_batter['player']} (Avg: {top_batter['bat_avg_first']:.1f}, SR: {top_batter['bat_sr_first']:.1f})")
        
        # Top bowler
        bowlers = team_players[team_players['role'].isin(['Bowler', 'All-rounder'])]
        bowlers = bowlers[bowlers['bowl_econ_first'] > 0]
        if len(bowlers) > 0:
            top_bowler = bowlers.loc[bowlers['bowl_econ_first'].idxmin()]
            print(f"   🎯 Top Bowler: {top_bowler['player']} (Econ: {top_bowler['bowl_econ_first']:.1f}, Avg: {top_bowler['bowl_avg_first']:.1f})")

def tournament_what_if_scenarios():
    """Explore what-if tournament scenarios"""
    print("\n\n🎰 TOURNAMENT WHAT-IF SCENARIOS")
    print("=" * 50)
    
    # Run quick simulations with different parameters
    scenarios = [
        {"sims": 100, "desc": "Quick Simulation"},
        {"sims": 500, "desc": "Medium Simulation"},
    ]
    
    for scenario in scenarios:
        print(f"\n🔄 {scenario['desc']} ({scenario['sims']} iterations)")
        print("-" * 40)
        
        simulator = TournamentSimulator(num_simulations=scenario['sims'])
        results = simulator.run_multiple_simulations()
        analysis = simulator.analyze_results(results)
        
        # Show top 5 teams
        top_5 = analysis.head(5)
        for i, (_, team) in enumerate(top_5.iterrows(), 1):
            medal = ["🥇", "🥈", "🥉", "🏅", "🏅"][i-1]
            print(f"   {medal} {team['Team']}: {team['Win_Probability_%']:.1f}% win chance")

def match_prediction_confidence():
    """Show prediction confidence intervals"""
    print("\n\n📊 PREDICTION CONFIDENCE ANALYSIS")
    print("=" * 50)
    
    analyzer = MatchAnalyzer()
    
    # Test match predictions with uncertainty
    test_matches = [1, 5, 10, 15, 20]
    
    for match_id in test_matches:
        match_details = analyzer.get_match_details(match_id)
        print(f"\n📍 Match {match_id}: {match_details['team1']} vs {match_details['team2']}")
        
        # Test multiple toss scenarios to show range
        probabilities = []
        for toss_winner in ['Team A', 'Team B']:
            for decision in ['Bat', 'Bowl']:
                result = analyzer.calculate_win_probability(match_id, toss_winner, decision)
                probabilities.append(result['win_prob'][0])
        
        min_prob = min(probabilities)
        max_prob = max(probabilities)
        avg_prob = sum(probabilities) / len(probabilities)
        
        print(f"   📈 {match_details['team1']} Win Probability Range:")
        print(f"      Minimum: {min_prob:.1f}% | Average: {avg_prob:.1f}% | Maximum: {max_prob:.1f}%")
        print(f"      Confidence Spread: ±{(max_prob - min_prob)/2:.1f}%")

def system_statistics():
    """Show comprehensive system statistics"""
    print("\n\n📊 SYSTEM COMPREHENSIVE STATISTICS")
    print("=" * 50)
    
    # Load all data files
    schedule_df = pd.read_csv(config.SCHEDULE_FILE)
    squads_df = pd.read_csv(config.SQUADS_FILE)
    venue_df = pd.read_csv(config.VENUE_STATS_FILE)
    player_df = pd.read_csv(config.PLAYER_STATS_FILE)
    team_df = pd.read_csv(config.TEAM_RATINGS_FILE)
    
    print(f"📅 Tournament Schedule:")
    print(f"   • Total Matches: {len(schedule_df)}")
    print(f"   • Teams: {len(schedule_df['Team1'].unique())}")
    print(f"   • Venues: {len(schedule_df['Venue'].unique())}")
    print(f"   • Duration: {schedule_df['Date'].min()} to {schedule_df['Date'].max()}")
    
    print(f"\n👥 Player Database:")
    print(f"   • Total Players: {len(player_df)}")
    print(f"   • Batters: {len(player_df[player_df['role'] == 'Batter'])}")
    print(f"   • Bowlers: {len(player_df[player_df['role'] == 'Bowler'])}")
    print(f"   • All-rounders: {len(player_df[player_df['role'] == 'All-rounder'])}")
    
    print(f"\n🏟️ Venue Analysis:")
    print(f"   • Total Venues: {len(venue_df)}")
    print(f"   • Avg Run Rate: {venue_df['run_rate'].mean():.1f}")
    print(f"   • Highest Avg Score: {venue_df['avg_first_innings_score'].max():.0f}")
    print(f"   • Lowest Avg Score: {venue_df['avg_first_innings_score'].min():.0f}")
    
    print(f"\n⚡ Team Ratings:")
    print(f"   • Strongest Batting: {team_df.loc[team_df['Bat_Rating'].idxmax()]['Team']} ({team_df['Bat_Rating'].max():.1f})")
    print(f"   • Strongest Bowling: {team_df.loc[team_df['Bowl_Rating'].idxmax()]['Team']} ({team_df['Bowl_Rating'].max():.1f})")
    print(f"   • Most Balanced: {team_df.loc[team_df['Overall_Rating'].idxmax()]['Team']} ({team_df['Overall_Rating'].max():.1f})")

def main():
    """Run all advanced demos"""
    print("🏏 THE HUNDRED ANALYTICS - ADVANCED EXPLORATION")
    print("=" * 60)
    print("Diving deep into cricket analytics capabilities...")
    print("=" * 60)
    
    advanced_match_analysis()
    venue_deep_dive()
    team_strength_breakdown()
    tournament_what_if_scenarios()
    match_prediction_confidence()
    system_statistics()
    
    print("\n" + "=" * 60)
    print("🎯 ADVANCED EXPLORATION COMPLETE!")
    print("💡 Key Insights: Oval Invincibles lead, but competition is tight!")
    print("🏟️ Venue impact is significant - toss decisions matter!")
    print("📊 System provides realistic, data-driven predictions!")
    print("=" * 60)

if __name__ == "__main__":
    main()