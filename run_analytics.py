#!/usr/bin/env python3
"""
Main runner script for The Hundred Analytics System
Orchestrates all components and launches the dashboard
"""

import os
import sys
import subprocess
from datetime import datetime

def print_banner():
    """Print system banner"""
    print("=" * 60)
    print("🏏 THE HUNDRED ANALYTICS SYSTEM")
    print("=" * 60)
    print("Complete cricket analytics suite for The Hundred 2025")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def run_data_setup():
    """Run initial data setup"""
    print("\n📊 Phase 1: Setting up data files...")
    try:
        result = subprocess.run([sys.executable, "data_setup.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Data setup completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Data setup failed: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def run_venue_scraper():
    """Run venue statistics scraper"""
    print("\n🏟️ Phase 2a: Scraping venue statistics...")
    try:
        result = subprocess.run([sys.executable, "scrapers/venue_scraper.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Venue scraping completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Venue scraping failed: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def run_player_scraper():
    """Run player statistics scraper"""
    print("\n👤 Phase 2b: Scraping player statistics...")
    try:
        result = subprocess.run([sys.executable, "scrapers/player_scraper.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Player scraping completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Player scraping failed: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def run_team_calculator():
    """Run team strength calculator"""
    print("\n⚡ Phase 3: Calculating team strengths...")
    try:
        result = subprocess.run([sys.executable, "team_strength_calculator.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Team strength calculation completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Team strength calculation failed: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def run_tournament_simulator():
    """Run tournament simulator"""
    print("\n🎰 Phase 4: Running tournament simulation...")
    try:
        result = subprocess.run([sys.executable, "tournament_simulator.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Tournament simulation completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tournament simulation failed: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def launch_dashboard():
    """Launch the interactive dashboard"""
    print("\n🚀 Phase 5: Launching interactive dashboard...")
    print("📊 Dashboard URL: http://127.0.0.1:8050")
    print("🎯 Press Ctrl+C to stop the dashboard")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "hundred_analytics_dash.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Dashboard launch failed: {e}")

def check_data_files():
    """Check if all required data files exist"""
    import config
    
    required_files = [
        config.SCHEDULE_FILE,
        config.SQUADS_FILE,
        config.VENUE_STATS_FILE,
        config.PLAYER_STATS_FILE,
        config.TEAM_RATINGS_FILE,
        config.TOURNAMENT_PREDICTIONS_FILE
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    return missing_files

def main():
    """Main function to run the complete analytics system"""
    print_banner()
    
    # Check if we need to run the full pipeline
    missing_files = check_data_files()
    
    if missing_files:
        print("🔄 Some data files are missing. Running full pipeline...")
        
        # Run all phases in sequence
        phases = [
            run_data_setup,
            run_venue_scraper,
            run_player_scraper,
            run_team_calculator,
            run_tournament_simulator
        ]
        
        for phase in phases:
            if not phase():
                print("❌ Pipeline failed. Exiting.")
                return False
    else:
        print("✅ All data files found. Skipping to dashboard...")
    
    # Launch dashboard
    launch_dashboard()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 System stopped by user")
    except Exception as e:
        print(f"❌ System error: {e}")