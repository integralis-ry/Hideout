# app.py
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import pandas as pd
import requests
import io
from functools import lru_cache
from collections import Counter

app = Flask(__name__)

@lru_cache(maxsize=1)
def fetch_google_sheet_data_cached(cache_key):
    sheet_url = "https://docs.google.com/spreadsheets/d/1FS9Dej3jq0BuCQGPjzCIJH1_WI9ddHgS6n_00NjsEJw/edit?gid=217936795"
    file_id = sheet_url.split('/')[5]
    export_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
    
    try:
        response = requests.get(export_url)
        response.raise_for_status()
        return pd.read_csv(io.StringIO(response.text))
    except Exception as e:
        print(f"Error fetching sheet data: {e}")
        return None

def get_funny_comments(df):
   comments = []
   last_cols = df.columns[-7:]
   
   for col in last_cols:
       col_name = col.split()[-1]  # Get last word of column name
       col_comments = df[col].dropna().tolist()
       for comment in col_comments:
           if isinstance(comment, str) and comment.strip():
               comments.append(f"{col_name}: {comment}")
   print(comments)
   return comments

def parse_game_data(df):
    rows = []
    winner_counts = Counter()
    
    for _, row in df.iterrows():
        try:
            timestamp = datetime.strptime(row['Timestamp'], '%d/%m/%Y %H:%M:%S')
            game_type = row['What game did you play?']

            players = [col for col in df.columns if col.startswith('Other player')]
            for player_col in players:
                if pd.notna(row[player_col]):
                    winner = row[player_col]
                    winner_counts[winner] += 1
                    break
            
            rows.append({
                'timestamp': timestamp,
                'game': game_type,
                'winner': winner
            })
        except Exception as e:
            print(f"Error parsing row: {e}")
            continue
    
    # Return the winner counts as a list of dicts, sorted by wins
    sorted_winners = [
        {'name': name, 'wins': count} 
        for name, count in sorted(winner_counts.items(), key=lambda x: (-x[1], x[0]))
    ]
    
    return pd.DataFrame(rows), sorted_winners

# Update the /get_data route to use the new structure
@app.route('/get_data')
def get_data():
    cache_key = datetime.now().strftime('%Y%m%d%H%M')
    raw_data = fetch_google_sheet_data_cached(cache_key)
    
    if raw_data is None:
        return jsonify({'error': 'Failed to fetch data'}), 500
    
    df, winner_counts = parse_game_data(raw_data)
    funny_comments = get_funny_comments(raw_data)
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    today_games = df[df['timestamp'].dt.date == today].to_dict('records')
    yesterday_games = df[df['timestamp'].dt.date == yesterday].to_dict('records')
    
    return jsonify({
        'today_games': today_games,
        'yesterday_games': yesterday_games,
        'today': today.strftime('%d/%m/%Y'),
        'yesterday': yesterday.strftime('%d/%m/%Y'),
        'winner_counts': winner_counts,  # This is now a list of dicts
        'funny_comments': funny_comments
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)