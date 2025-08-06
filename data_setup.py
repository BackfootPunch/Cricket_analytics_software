#!/usr/bin/env python3
"""
Data Setup Script for Cricket Analytics System
Creates initial CSV files from provided schedule and squad data
"""

import pandas as pd
import csv
from datetime import datetime
import config

def create_schedule_csv():
    """Create schedule_2025.csv from the provided match schedule"""
    
    # Match schedule data from the problem statement
    matches_data = [
        {"Match_ID": 1, "Date": "2025-08-05", "Time": "11:00 PM", "Team1": "London Spirit", "Team2": "Oval Invincibles", "Venue": "Lord's, London"},
        {"Match_ID": 2, "Date": "2025-08-06", "Time": "11:00 PM", "Team1": "Manchester Originals", "Team2": "Southern Brave", "Venue": "Emirates Old Trafford, Manchester"},
        {"Match_ID": 3, "Date": "2025-08-07", "Time": "11:00 PM", "Team1": "Northern Superchargers", "Team2": "Welsh Fire", "Venue": "Headingley, Leeds"},
        {"Match_ID": 4, "Date": "2025-08-08", "Time": "11:00 PM", "Team1": "Birmingham Phoenix", "Team2": "Trent Rockets", "Venue": "Edgbaston, Birmingham"},
        {"Match_ID": 5, "Date": "2025-08-09", "Time": "7:00 PM", "Team1": "Oval Invincibles", "Team2": "Manchester Originals", "Venue": "Kennington Oval, London"},
        {"Match_ID": 6, "Date": "2025-08-09", "Time": "10:30 PM", "Team1": "Welsh Fire", "Team2": "London Spirit", "Venue": "Sophia Gardens, Cardiff"},
        {"Match_ID": 7, "Date": "2025-08-10", "Time": "7:00 PM", "Team1": "Southern Brave", "Team2": "Birmingham Phoenix", "Venue": "The Rose Bowl, Southampton"},
        {"Match_ID": 8, "Date": "2025-08-10", "Time": "10:30 PM", "Team1": "Trent Rockets", "Team2": "Northern Superchargers", "Venue": "Trent Bridge, Nottingham"},
        {"Match_ID": 9, "Date": "2025-08-11", "Time": "11:00 PM", "Team1": "Manchester Originals", "Team2": "London Spirit", "Venue": "Emirates Old Trafford, Manchester"},
        {"Match_ID": 10, "Date": "2025-08-12", "Time": "11:00 PM", "Team1": "Birmingham Phoenix", "Team2": "Oval Invincibles", "Venue": "Edgbaston, Birmingham"},
        {"Match_ID": 11, "Date": "2025-08-13", "Time": "7:30 PM", "Team1": "Southern Brave", "Team2": "Northern Superchargers", "Venue": "The Rose Bowl, Southampton"},
        {"Match_ID": 12, "Date": "2025-08-13", "Time": "11:00 PM", "Team1": "Welsh Fire", "Team2": "Manchester Originals", "Venue": "Sophia Gardens, Cardiff"},
        {"Match_ID": 13, "Date": "2025-08-14", "Time": "11:00 PM", "Team1": "London Spirit", "Team2": "Trent Rockets", "Venue": "Lord's, London"},
        {"Match_ID": 14, "Date": "2025-08-15", "Time": "11:00 PM", "Team1": "Northern Superchargers", "Team2": "Birmingham Phoenix", "Venue": "Headingley, Leeds"},
        {"Match_ID": 15, "Date": "2025-08-16", "Time": "7:00 PM", "Team1": "Trent Rockets", "Team2": "Southern Brave", "Venue": "Trent Bridge, Nottingham"},
        {"Match_ID": 16, "Date": "2025-08-16", "Time": "10:30 PM", "Team1": "Oval Invincibles", "Team2": "Welsh Fire", "Venue": "Kennington Oval, London"},
        {"Match_ID": 17, "Date": "2025-08-17", "Time": "7:00 PM", "Team1": "Manchester Originals", "Team2": "Northern Superchargers", "Venue": "Emirates Old Trafford, Manchester"},
        {"Match_ID": 18, "Date": "2025-08-17", "Time": "10:30 PM", "Team1": "Birmingham Phoenix", "Team2": "London Spirit", "Venue": "Edgbaston, Birmingham"},
        {"Match_ID": 19, "Date": "2025-08-18", "Time": "11:00 PM", "Team1": "Southern Brave", "Team2": "Oval Invincibles", "Venue": "The Rose Bowl, Southampton"},
        {"Match_ID": 20, "Date": "2025-08-19", "Time": "11:00 PM", "Team1": "Trent Rockets", "Team2": "Manchester Originals", "Venue": "Trent Bridge, Nottingham"},
        {"Match_ID": 21, "Date": "2025-08-20", "Time": "7:30 PM", "Team1": "Welsh Fire", "Team2": "Southern Brave", "Venue": "Sophia Gardens, Cardiff"},
        {"Match_ID": 22, "Date": "2025-08-20", "Time": "11:00 PM", "Team1": "London Spirit", "Team2": "Northern Superchargers", "Venue": "Lord's, London"},
        {"Match_ID": 23, "Date": "2025-08-21", "Time": "11:00 PM", "Team1": "Oval Invincibles", "Team2": "Trent Rockets", "Venue": "Kennington Oval, London"},
        {"Match_ID": 24, "Date": "2025-08-22", "Time": "11:00 PM", "Team1": "Birmingham Phoenix", "Team2": "Welsh Fire", "Venue": "Edgbaston, Birmingham"},
        {"Match_ID": 25, "Date": "2025-08-23", "Time": "7:00 PM", "Team1": "Northern Superchargers", "Team2": "Oval Invincibles", "Venue": "Headingley, Leeds"},
        {"Match_ID": 26, "Date": "2025-08-23", "Time": "10:30 PM", "Team1": "London Spirit", "Team2": "Southern Brave", "Venue": "Lord's, London"},
        {"Match_ID": 27, "Date": "2025-08-24", "Time": "7:00 PM", "Team1": "Welsh Fire", "Team2": "Trent Rockets", "Venue": "Sophia Gardens, Cardiff"},
        {"Match_ID": 28, "Date": "2025-08-24", "Time": "10:30 PM", "Team1": "Manchester Originals", "Team2": "Birmingham Phoenix", "Venue": "Emirates Old Trafford, Manchester"},
        {"Match_ID": 29, "Date": "2025-08-25", "Time": "11:00 PM", "Team1": "Oval Invincibles", "Team2": "London Spirit", "Venue": "Kennington Oval, London"},
        {"Match_ID": 30, "Date": "2025-08-26", "Time": "11:00 PM", "Team1": "Northern Superchargers", "Team2": "Manchester Originals", "Venue": "Headingley, Leeds"},
        {"Match_ID": 31, "Date": "2025-08-27", "Time": "11:00 PM", "Team1": "Trent Rockets", "Team2": "Birmingham Phoenix", "Venue": "Trent Bridge, Nottingham"},
        {"Match_ID": 32, "Date": "2025-08-28", "Time": "11:00 PM", "Team1": "Southern Brave", "Team2": "Welsh Fire", "Venue": "The Rose Bowl, Southampton"}
    ]
    
    df = pd.DataFrame(matches_data)
    df.to_csv(config.SCHEDULE_FILE, index=False)
    print(f"Schedule CSV created: {config.SCHEDULE_FILE}")
    print(f"Total matches: {len(df)}")


def create_squads_csv():
    """Create squads_2025.csv from the provided squad data"""
    
    # Squad data from the problem statement
    squads_data = {
        "Oval Invincibles": ["Sam Billings", "Sam Curran", "Tom Curran", "Will Jacks", "Rashid Khan", "Jordan Cox", "Saqib Mahmood", "Jason Behrendorff", "Gus Atkinson", "Donovan Ferreira", "Nathan Sowter", "Tawanda Muyeye", "Miles Hammond", "George Scrimshaw", "Zafar Gohar"],
        
        "Birmingham Phoenix": ["Liam Livingstone", "Ben Duckett", "Trent Boult", "Joe Clarke", "Jacob Bethell", "Adam Milne", "Benny Howell", "Tim Southee", "Dan Mousley", "Will Smeed", "Chris Wood", "Harry Moore", "Tom Helm", "Aneurin Donald", "Liam Patterson-White", "Louis Kimber"],
        
        "London Spirit": ["Kane Williamson", "Jamie Smith", "Jamie Overton", "Liam Dawson", "David Warner", "Daniel Worrall", "Richard Gleeson", "Luke Wood", "Olly Stone", "Ashton Turner", "Ollie Pope", "Jafer Chohan", "Keaton Jennings", "Wayne Madsen", "Sean Dickson", "Ryan Higgins"],
        
        "Manchester Originals": ["Jos Buttler", "Noor Ahmad", "Phil Salt", "Rachin Ravindra", "Lewis Gregory", "Ben McKinney", "Heinrich Klaasen", "George Garton", "Matthew Hurst", "Josh Tongue", "Scott Currie", "Tom Hartley", "Sonny Baker", "Tom Aspinwall", "James Anderson", "Marchant de Lange"],
        
        "Southern Brave": ["Jofra Archer", "Michael Bracewell", "James Vince", "Chris Jordan", "Tymal Mills", "Leus Du Plooy", "Laurie Evans", "Craig Overton", "Reece Topley", "Finn Allen", "Jordan Thompson", "Danny Briggs", "James Coles", "Jason Roy", "Tory Albert", "Hilton Cartwright"],
        
        "Northern Superchargers": ["Harry Brook", "David Miller", "Adil Rashid", "Zak Crawley", "Mitchell Santner", "Dan Lawrence", "Brydon Carse", "Ben Dwarshuis", "Matthew Potts", "Michael Pepper", "Dawid Malan", "Pat Brown", "Graham Clark", "Tom Lawes", "James Fuller", "Rocky Flintoff"],
        
        "Trent Rockets": ["Joe Root", "David Willey", "Marcus Stoinis", "Lockie Ferguson", "Tom Banton", "Max Holden", "George Linde", "Sam Cook", "John Turner", "Adam Hose", "Rehan Ahmed", "Sam Hain", "Tom Alsop", "Calvin Harrison", "Callum Parkinson", "Ben Sanderson"],
        
        "Welsh Fire": ["Tom Abell", "Chris Woakes", "Jonny Bairstow", "Steve Smith", "David Payne", "Tom Kohler-Cadmore", "Paul Walter", "Riley Meredith", "Chris Green", "Saif Zaib", "Luke Wells", "Stephen Eskinazi", "Josh Hull", "Mason Crane", "Ajeet Singh Dale", "Ben Kellaway"]
    }
    
    # Create squad list with roles (basic classification)
    squad_records = []
    
    # Basic role classification based on player names and cricket knowledge
    batters = ["Sam Billings", "Ben Duckett", "Joe Clarke", "Kane Williamson", "Jamie Smith", "David Warner", "Ollie Pope", "Jos Buttler", "Phil Salt", "Heinrich Klaasen", "James Vince", "Jason Roy", "Laurie Evans", "Harry Brook", "David Miller", "Zak Crawley", "Dawid Malan", "Joe Root", "Tom Banton", "Jonny Bairstow", "Steve Smith", "Will Jacks", "Jordan Cox", "Jacob Bethell", "Will Smeed", "Liam Livingstone", "Keaton Jennings", "Wayne Madsen", "Rachin Ravindra", "Ben McKinney", "Leus Du Plooy", "Finn Allen", "Dan Lawrence", "Michael Pepper", "Marcus Stoinis", "Max Holden", "Tom Kohler-Cadmore", "Luke Wells", "Stephen Eskinazi"]
    
    bowlers = ["Sam Curran", "Tom Curran", "Rashid Khan", "Saqib Mahmood", "Jason Behrendorff", "Gus Atkinson", "Trent Boult", "Adam Milne", "Tim Southee", "Jamie Overton", "Liam Dawson", "Daniel Worrall", "Richard Gleeson", "Luke Wood", "Olly Stone", "Noor Ahmad", "Lewis Gregory", "George Garton", "Josh Tongue", "Tom Hartley", "James Anderson", "Marchant de Lange", "Jofra Archer", "Chris Jordan", "Tymal Mills", "Craig Overton", "Reece Topley", "Danny Briggs", "Adil Rashid", "Mitchell Santner", "Brydon Carse", "Ben Dwarshuis", "Matthew Potts", "Pat Brown", "David Willey", "Lockie Ferguson", "George Linde", "Sam Cook", "John Turner", "Rehan Ahmed", "Callum Parkinson", "Ben Sanderson", "Chris Woakes", "David Payne", "Riley Meredith", "Chris Green", "Josh Hull", "Mason Crane"]
    
    all_rounders = ["Michael Bracewell", "Jordan Thompson", "James Coles", "Tom Lawes", "James Fuller", "Rocky Flintoff", "Adam Hose", "Sam Hain", "Tom Alsop", "Calvin Harrison", "Tom Abell", "Paul Walter", "Saif Zaib", "Ajeet Singh Dale", "Ben Kellaway", "Benny Howell", "Dan Mousley", "Ashton Turner", "Ryan Higgins", "Scott Currie", "Sonny Baker", "Tom Aspinwall", "Tory Albert", "Hilton Cartwright", "Graham Clark"]
    
    for team, players in squads_data.items():
        for player in players:
            # Assign role based on classification
            if player in batters:
                role = "Batter"
            elif player in bowlers:
                role = "Bowler"
            elif player in all_rounders:
                role = "All-rounder"
            else:
                role = "All-rounder"  # Default for unclassified
                
            squad_records.append({
                "Team": team,
                "Player": player,
                "Role": role
            })
    
    df = pd.DataFrame(squad_records)
    df.to_csv(config.SQUADS_FILE, index=False)
    print(f"Squads CSV created: {config.SQUADS_FILE}")
    print(f"Total players: {len(df)}")
    print(f"Teams: {df['Team'].nunique()}")


def main():
    """Main function to set up initial data files"""
    print("Setting up Cricket Analytics System data files...")
    
    create_schedule_csv()
    print()
    create_squads_csv()
    
    print(f"\nData setup complete!")
    print(f"Files created in: {config.DATA_DIR}")


if __name__ == "__main__":
    main()