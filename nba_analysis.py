"""
NBA Trends Analysis Module
Analyzes NBA game statistics and trends
"""

from typing import Dict, Any, List
import random


def generate_sample_nba_data() -> Dict[str, Any]:
    """Generate sample NBA data for demonstration"""
    teams_2010 = {
        'Knicks': {'mean': 102, 'std': 8},
        'Nets': {'mean': 95, 'std': 7},
        'Lakers': {'mean': 108, 'std': 9},
        'Celtics': {'mean': 105, 'std': 8}
    }
    
    teams_2014 = {
        'Knicks': {'mean': 98, 'std': 7},
        'Nets': {'mean': 97, 'std': 8},
        'Lakers': {'mean': 100, 'std': 9},
        'Celtics': {'mean': 103, 'std': 8}
    }
    
    # Generate game data
    games_2010 = []
    games_2014 = []
    
    for team, stats in teams_2010.items():
        for _ in range(20):  # 20 games per team
            points = max(60, int(random.gauss(stats['mean'], stats['std'])))
            games_2010.append({
                'team': team,
                'points': points,
                'opponent_points': points - random.randint(-15, 15),
                'location': random.choice(['H', 'A']),
                'result': 'W' if random.random() > 0.4 else 'L'
            })
    
    for team, stats in teams_2014.items():
        for _ in range(20):
            points = max(60, int(random.gauss(stats['mean'], stats['std'])))
            games_2014.append({
                'team': team,
                'points': points,
                'opponent_points': points - random.randint(-15, 15),
                'location': random.choice(['H', 'A']),
                'result': 'W' if random.random() > 0.4 else 'L'
            })
    
    return {
        '2010': games_2010,
        '2014': games_2014
    }


def analyze_nba() -> Dict[str, Any]:
    """Main analysis function for NBA trends"""
    data = generate_sample_nba_data()
    
    games_2010 = data['2010']
    games_2014 = data['2014']
    
    # Team analysis
    teams = ['Knicks', 'Nets', 'Lakers', 'Celtics']
    
    team_stats_2010 = {}
    team_stats_2014 = {}
    
    for team in teams:
        team_games_2010 = [g for g in games_2010 if g['team'] == team]
        team_games_2014 = [g for g in games_2014 if g['team'] == team]
        
        if team_games_2010:
            team_stats_2010[team] = {
                'avg_points': sum(g['points'] for g in team_games_2010) / len(team_games_2010),
                'games': len(team_games_2010),
                'wins': sum(1 for g in team_games_2010 if g['result'] == 'W'),
                'points_list': [g['points'] for g in team_games_2010]
            }
        
        if team_games_2014:
            team_stats_2014[team] = {
                'avg_points': sum(g['points'] for g in team_games_2014) / len(team_games_2014),
                'games': len(team_games_2014),
                'wins': sum(1 for g in team_games_2014 if g['result'] == 'W'),
                'points_list': [g['points'] for g in team_games_2014]
            }
    
    # Knicks vs Nets comparison
    knicks_2010_pts = team_stats_2010['Knicks']['points_list']
    nets_2010_pts = team_stats_2010['Nets']['points_list']
    knicks_2014_pts = team_stats_2014['Knicks']['points_list']
    nets_2014_pts = team_stats_2014['Nets']['points_list']
    
    diff_2010 = sum(knicks_2010_pts) / len(knicks_2010_pts) - sum(nets_2010_pts) / len(nets_2010_pts)
    diff_2014 = sum(knicks_2014_pts) / len(knicks_2014_pts) - sum(nets_2014_pts) / len(nets_2014_pts)
    
    # Home vs Away analysis
    home_wins_2010 = sum(1 for g in games_2010 if g['location'] == 'H' and g['result'] == 'W')
    home_games_2010 = sum(1 for g in games_2010 if g['location'] == 'H')
    home_win_rate_2010 = (home_wins_2010 / home_games_2010 * 100) if home_games_2010 > 0 else 0
    
    return {
        'team_stats_2010': {k: {
            'avg_points': round(v['avg_points'], 1),
            'wins': v['wins'],
            'games': v['games'],
            'win_rate': round(v['wins'] / v['games'] * 100, 1) if v['games'] > 0 else 0
        } for k, v in team_stats_2010.items()},
        'team_stats_2014': {k: {
            'avg_points': round(v['avg_points'], 1),
            'wins': v['wins'],
            'games': v['games'],
            'win_rate': round(v['wins'] / v['games'] * 100, 1) if v['games'] > 0 else 0
        } for k, v in team_stats_2014.items()},
        'knicks_vs_nets': {
            '2010': {
                'knicks_avg': round(sum(knicks_2010_pts) / len(knicks_2010_pts), 1),
                'nets_avg': round(sum(nets_2010_pts) / len(nets_2010_pts), 1),
                'difference': round(diff_2010, 1)
            },
            '2014': {
                'knicks_avg': round(sum(knicks_2014_pts) / len(knicks_2014_pts), 1),
                'nets_avg': round(sum(nets_2014_pts) / len(nets_2014_pts), 1),
                'difference': round(diff_2014, 1)
            }
        },
        'home_advantage': {
            '2010': {
                'home_win_rate': round(home_win_rate_2010, 1),
                'home_games': home_games_2010,
                'home_wins': home_wins_2010
            }
        },
        'points_data': {
            'knicks_2010': knicks_2010_pts[:20],  # Limit for chart
            'nets_2010': nets_2010_pts[:20],
            'knicks_2014': knicks_2014_pts[:20],
            'nets_2014': nets_2014_pts[:20]
        }
    }

