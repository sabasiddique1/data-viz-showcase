"""
Hurricane Analysis Module
Analyzes hurricane data and identifies patterns, statistics, and insights
"""

import json
import os
from typing import Dict, List, Any

def load_hurricane_data() -> Dict[str, Any]:
    """Load hurricane data from JSON file"""
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'hurricanes.json')
    with open(data_path, 'r') as f:
        return json.load(f)

def analyze_hurricanes() -> Dict[str, Any]:
    """Analyze hurricane data and return insights"""
    data = load_hurricane_data()
    hurricanes = data.get('hurricanes', [])
    
    if not hurricanes:
        return {"error": "No hurricane data available"}
    
    # Calculate statistics
    total_hurricanes = len(hurricanes)
    total_damage = sum(h.get('damage_cost_billions', 0) for h in hurricanes)
    total_fatalities = sum(h.get('fatalities', 0) for h in hurricanes)
    avg_wind_speed = sum(h.get('max_wind_speed', 0) for h in hurricanes) / total_hurricanes
    avg_category = sum(h.get('category', 0) for h in hurricanes) / total_hurricanes
    
    # Find extremes
    strongest = max(hurricanes, key=lambda x: x.get('max_wind_speed', 0))
    most_damaging = max(hurricanes, key=lambda x: x.get('damage_cost_billions', 0))
    deadliest = max(hurricanes, key=lambda x: x.get('fatalities', 0))
    
    # Category distribution
    category_dist = {}
    for h in hurricanes:
        cat = h.get('category', 0)
        category_dist[cat] = category_dist.get(cat, 0) + 1
    
    # Year analysis
    year_dist = {}
    for h in hurricanes:
        year = h.get('year', 0)
        year_dist[year] = year_dist.get(year, 0) + 1
    
    # Affected areas
    all_areas = []
    for h in hurricanes:
        all_areas.extend(h.get('affected_areas', []))
    area_counts = {}
    for area in all_areas:
        area_counts[area] = area_counts.get(area, 0) + 1
    
    return {
        "summary": {
            "total_hurricanes": total_hurricanes,
            "total_damage_billions": round(total_damage, 2),
            "total_fatalities": total_fatalities,
            "average_wind_speed": round(avg_wind_speed, 1),
            "average_category": round(avg_category, 1)
        },
        "extremes": {
            "strongest": strongest,
            "most_damaging": most_damaging,
            "deadliest": deadliest
        },
        "category_distribution": category_dist,
        "year_distribution": year_dist,
        "affected_areas": area_counts,
        "all_hurricanes": hurricanes
    }

def main():
    """Main function for command-line use"""
    results = analyze_hurricanes()
    print("\n=== Hurricane Analysis Results ===")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
