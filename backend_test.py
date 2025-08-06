#!/usr/bin/env python3
"""
Comprehensive Backend Testing for The Hundred Cricket Analytics System
Tests all core components: data integrity, match analysis, tournament simulation, and dashboard
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import traceback

# Add current directory to path for imports
sys.path.append('/app')

try:
    import config
    from match_analyzer import MatchAnalyzer
    from tournament_simulator import TournamentSimulator
    import hundred_analytics_dash
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

class CricketAnalyticsTestSuite:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
    def log_test(self, test_name, passed, message="", error=None):
        """Log test result"""
        self.tests_run += 1
        if passed:
            self.tests_passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'error': str(error) if error else None
        }
        self.test_results.append(result)
        print(f"{status}: {test_name} - {message}")
        if error:
            print(f"   Error: {error}")
    
    def test_data_integrity(self):
        """Test 1: Data Integrity - Verify all CSV files exist and have correct structure"""
        print("\n🔍 Testing Data Integrity...")
        
        required_files = [
            (config.SCHEDULE_FILE, "Schedule file"),
            (config.SQUADS_FILE, "Squads file"),
            (config.VENUE_STATS_FILE, "Venue stats file"),
            (config.PLAYER_STATS_FILE, "Player stats file"),
            (config.TEAM_RATINGS_FILE, "Team ratings file"),
            (config.TOURNAMENT_PREDICTIONS_FILE, "Tournament predictions file")
        ]
        
        for file_path, description in required_files:
            try:
                if not os.path.exists(file_path):
                    self.log_test(f"File Exists: {description}", False, f"File not found: {file_path}")
                    continue
                
                df = pd.read_csv(file_path)
                if len(df) == 0:
                    self.log_test(f"File Content: {description}", False, "File is empty")
                else:
                    self.log_test(f"File Content: {description}", True, f"Loaded {len(df)} records")
                    
            except Exception as e:
                self.log_test(f"File Load: {description}", False, f"Failed to load", e)
        
        # Test specific data structure requirements
        try:
            schedule_df = pd.read_csv(config.SCHEDULE_FILE)
            required_schedule_cols = ['Match_ID', 'Team1', 'Team2', 'Venue', 'Date', 'Time']
            missing_cols = [col for col in required_schedule_cols if col not in schedule_df.columns]
            
            if missing_cols:
                self.log_test("Schedule Structure", False, f"Missing columns: {missing_cols}")
            else:
                self.log_test("Schedule Structure", True, f"All required columns present")
                
                # Check for 32 matches
                if len(schedule_df) == 32:
                    self.log_test("Schedule Count", True, "Correct number of matches (32)")
                else:
                    self.log_test("Schedule Count", False, f"Expected 32 matches, found {len(schedule_df)}")
                    
        except Exception as e:
            self.log_test("Schedule Validation", False, "Failed to validate schedule", e)
    
    def test_match_analyzer(self):
        """Test 2: Match Analyzer - Test core match analysis functionality"""
        print("\n🎯 Testing Match Analyzer...")
        
        try:
            analyzer = MatchAnalyzer()
            self.log_test("Match Analyzer Init", True, "Successfully initialized")
            
            # Test specific match scenarios as mentioned in requirements
            test_matches = [
                {'match_id': 1, 'toss_winner': 'Team A', 'toss_decision': 'Bat', 'description': 'Opening Match'},
                {'match_id': 5, 'toss_winner': 'Team B', 'toss_decision': 'Bowl', 'description': 'Mid-tournament'},
                {'match_id': 15, 'toss_winner': 'Team A', 'toss_decision': 'Bat', 'description': 'High-scoring venue'}
            ]
            
            for test_match in test_matches:
                try:
                    result = analyzer.calculate_win_probability(
                        test_match['match_id'], 
                        test_match['toss_winner'], 
                        test_match['toss_decision']
                    )
                    
                    # Validate result structure
                    required_keys = ['team1', 'team2', 'venue', 'win_prob', 'key_factor']
                    missing_keys = [key for key in required_keys if key not in result]
                    
                    if missing_keys:
                        self.log_test(f"Match {test_match['match_id']} Structure", False, f"Missing keys: {missing_keys}")
                        continue
                    
                    # Validate probability ranges (15-85% as per requirements)
                    prob1, prob2 = result['win_prob']
                    if 15 <= prob1 <= 85 and 15 <= prob2 <= 85:
                        self.log_test(f"Match {test_match['match_id']} Probabilities", True, 
                                    f"{result['team1']}: {prob1}%, {result['team2']}: {prob2}%")
                    else:
                        self.log_test(f"Match {test_match['match_id']} Probabilities", False, 
                                    f"Probabilities out of range: {prob1}%, {prob2}%")
                    
                    # Check probability sum
                    if abs(prob1 + prob2 - 100) < 0.1:
                        self.log_test(f"Match {test_match['match_id']} Probability Sum", True, "Probabilities sum to 100%")
                    else:
                        self.log_test(f"Match {test_match['match_id']} Probability Sum", False, 
                                    f"Probabilities sum to {prob1 + prob2}%")
                        
                except Exception as e:
                    self.log_test(f"Match {test_match['match_id']} Analysis", False, 
                                f"Failed to analyze {test_match['description']}", e)
                    
        except Exception as e:
            self.log_test("Match Analyzer Init", False, "Failed to initialize", e)
    
    def test_tournament_simulator(self):
        """Test 3: Tournament Simulator - Test tournament prediction functionality"""
        print("\n🏆 Testing Tournament Simulator...")
        
        try:
            # Test with smaller simulation count for faster testing
            simulator = TournamentSimulator(num_simulations=10)
            self.log_test("Tournament Simulator Init", True, "Successfully initialized")
            
            # Test single simulation
            try:
                single_result = simulator.run_simulation()
                
                required_keys = ['winner', 'standings', 'playoff_teams']
                missing_keys = [key for key in required_keys if key not in single_result]
                
                if missing_keys:
                    self.log_test("Single Simulation Structure", False, f"Missing keys: {missing_keys}")
                else:
                    self.log_test("Single Simulation Structure", True, "All required keys present")
                    
                    # Validate winner is a valid team
                    teams = pd.read_csv(config.TEAM_RATINGS_FILE)['Team'].tolist()
                    if single_result['winner'] in teams:
                        self.log_test("Single Simulation Winner", True, f"Winner: {single_result['winner']}")
                    else:
                        self.log_test("Single Simulation Winner", False, f"Invalid winner: {single_result['winner']}")
                        
            except Exception as e:
                self.log_test("Single Simulation", False, "Failed to run single simulation", e)
            
            # Test multiple simulations (small count for testing)
            try:
                results = simulator.run_multiple_simulations()
                analysis = simulator.analyze_results(results)
                
                # Check if analysis has all teams
                teams = pd.read_csv(config.TEAM_RATINGS_FILE)['Team'].tolist()
                analyzed_teams = analysis['Team'].tolist()
                
                if set(teams) == set(analyzed_teams):
                    self.log_test("Tournament Analysis Teams", True, "All teams included in analysis")
                else:
                    missing = set(teams) - set(analyzed_teams)
                    self.log_test("Tournament Analysis Teams", False, f"Missing teams: {missing}")
                
                # Check probability ranges
                win_probs = analysis['Win_Probability_%'].tolist()
                if all(0 <= prob <= 100 for prob in win_probs):
                    self.log_test("Tournament Win Probabilities", True, "All probabilities in valid range")
                else:
                    invalid = [prob for prob in win_probs if not (0 <= prob <= 100)]
                    self.log_test("Tournament Win Probabilities", False, f"Invalid probabilities: {invalid}")
                
                # Check if probabilities are realistic (no team should have >90% or <1% unless very unbalanced)
                extreme_probs = [prob for prob in win_probs if prob > 90 or prob < 1]
                if len(extreme_probs) == 0:
                    self.log_test("Tournament Probability Realism", True, "Probabilities appear realistic")
                else:
                    self.log_test("Tournament Probability Realism", False, f"Extreme probabilities found: {extreme_probs}")
                    
            except Exception as e:
                self.log_test("Multiple Simulations", False, "Failed to run multiple simulations", e)
                
        except Exception as e:
            self.log_test("Tournament Simulator Init", False, "Failed to initialize", e)
    
    def test_dashboard_components(self):
        """Test 4: Dashboard Components - Test if dashboard can be imported and basic components work"""
        print("\n🚀 Testing Dashboard Components...")
        
        try:
            # Test dashboard import
            app = hundred_analytics_dash.app
            self.log_test("Dashboard Import", True, "Successfully imported dashboard")
            
            # Test if required data is loaded
            try:
                schedule_df = pd.read_csv(config.SCHEDULE_FILE)
                team_ratings_df = pd.read_csv(config.TEAM_RATINGS_FILE)
                venue_stats_df = pd.read_csv(config.VENUE_STATS_FILE)
                
                if len(schedule_df) > 0 and len(team_ratings_df) > 0 and len(venue_stats_df) > 0:
                    self.log_test("Dashboard Data Loading", True, "All required data files loaded")
                else:
                    self.log_test("Dashboard Data Loading", False, "Some data files are empty")
                    
            except Exception as e:
                self.log_test("Dashboard Data Loading", False, "Failed to load data for dashboard", e)
            
            # Test match analyzer integration
            try:
                analyzer = MatchAnalyzer()
                test_result = analyzer.calculate_win_probability(1, 'Team A', 'Bat')
                if 'win_prob' in test_result:
                    self.log_test("Dashboard Match Analysis Integration", True, "Match analyzer works with dashboard")
                else:
                    self.log_test("Dashboard Match Analysis Integration", False, "Match analyzer result incomplete")
            except Exception as e:
                self.log_test("Dashboard Match Analysis Integration", False, "Match analyzer integration failed", e)
                
        except Exception as e:
            self.log_test("Dashboard Import", False, "Failed to import dashboard", e)
    
    def test_demo_script(self):
        """Test 5: Demo Script - Test if demo script can run successfully"""
        print("\n🎪 Testing Demo Script...")
        
        try:
            # Import demo module
            import demo
            self.log_test("Demo Import", True, "Successfully imported demo module")
            
            # Test individual demo functions
            demo_functions = [
                ('demo_data_overview', demo.demo_data_overview),
                ('demo_match_analysis', demo.demo_match_analysis),
                ('demo_tournament_predictions', demo.demo_tournament_predictions),
                ('demo_venue_insights', demo.demo_venue_insights)
            ]
            
            for func_name, func in demo_functions:
                try:
                    func()
                    self.log_test(f"Demo Function: {func_name}", True, "Executed successfully")
                except Exception as e:
                    self.log_test(f"Demo Function: {func_name}", False, "Failed to execute", e)
                    
        except Exception as e:
            self.log_test("Demo Import", False, "Failed to import demo", e)
    
    def test_integration_pipeline(self):
        """Test 6: Integration Pipeline - Test the main runner components"""
        print("\n🔄 Testing Integration Pipeline...")
        
        try:
            import run_analytics
            self.log_test("Runner Import", True, "Successfully imported run_analytics")
            
            # Test data file checking function
            try:
                missing_files = run_analytics.check_data_files()
                if len(missing_files) == 0:
                    self.log_test("Data Files Check", True, "All required data files present")
                else:
                    self.log_test("Data Files Check", False, f"Missing files: {missing_files}")
            except Exception as e:
                self.log_test("Data Files Check", False, "Failed to check data files", e)
                
        except Exception as e:
            self.log_test("Runner Import", False, "Failed to import run_analytics", e)
    
    def run_all_tests(self):
        """Run all test suites"""
        print("=" * 70)
        print("🏏 THE HUNDRED ANALYTICS SYSTEM - COMPREHENSIVE TEST SUITE")
        print("=" * 70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Run all test suites
        test_suites = [
            self.test_data_integrity,
            self.test_match_analyzer,
            self.test_tournament_simulator,
            self.test_dashboard_components,
            self.test_demo_script,
            self.test_integration_pipeline
        ]
        
        for test_suite in test_suites:
            try:
                test_suite()
            except Exception as e:
                print(f"❌ Test suite failed: {test_suite.__name__} - {e}")
                traceback.print_exc()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%" if self.tests_run > 0 else "No tests run")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if "FAIL" in result['status']]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['message']}")
                if test['error']:
                    print(f"     Error: {test['error']}")
        
        # Show critical issues
        critical_issues = []
        for result in self.test_results:
            if "FAIL" in result['status']:
                if any(keyword in result['test'].lower() for keyword in ['import', 'init', 'file', 'data']):
                    critical_issues.append(result['test'])
        
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES:")
            for issue in critical_issues:
                print(f"   • {issue}")
        
        print("\n" + "=" * 70)
        
        # Return overall success
        return self.tests_passed == self.tests_run

def main():
    """Main function to run all tests"""
    test_suite = CricketAnalyticsTestSuite()
    success = test_suite.run_all_tests()
    
    if success:
        print("🎉 ALL TESTS PASSED - System is ready for use!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - Please review issues above")
        return 1

if __name__ == "__main__":
    sys.exit(main())