"""
Linear Regression Analysis Module
Implements Reggie's Linear Regression Project with interactive visualization
"""

import json
from typing import Dict, Any, List, Tuple


def get_y(m: float, b: float, x: float) -> float:
    """Calculate y value for a given x using linear equation y = mx + b"""
    return m * x + b


def calculate_error(m: float, b: float, point: Tuple[float, float]) -> float:
    """Calculate the absolute error between a point and the line"""
    x_point, y_point = point
    y_line = get_y(m, b, x_point)
    return abs(y_line - y_point)


def calculate_all_error(m: float, b: float, points: List[Tuple[float, float]]) -> float:
    """Calculate total error for all points"""
    return sum(calculate_error(m, b, point) for point in points)


def find_best_line(points: List[Tuple[float, float]], 
                   m_range: Tuple[float, float] = (-10, 10),
                   b_range: Tuple[float, float] = (-20, 20),
                   step: float = 0.1) -> Dict[str, Any]:
    """Find the best m and b that minimize error"""
    possible_ms = [m / 10 for m in range(int(m_range[0] * 10), int(m_range[1] * 10) + 1)]
    possible_bs = [b / 10 for b in range(int(b_range[0] * 10), int(b_range[1] * 10) + 1)]
    
    smallest_error = float("inf")
    best_m = 0
    best_b = 0
    
    for m in possible_ms:
        for b in possible_bs:
            error = calculate_all_error(m, b, points)
            if error < smallest_error:
                smallest_error = error
                best_m = m
                best_b = b
    
    return {
        'best_m': round(best_m, 2),
        'best_b': round(best_b, 2),
        'smallest_error': round(smallest_error, 2),
        'equation': f"y = {round(best_m, 2)}x + {round(best_b, 2)}"
    }


def analyze_linear_regression() -> Dict[str, Any]:
    """Main analysis function for linear regression"""
    # Sample datapoints from the project
    datapoints = [(1, 2), (2, 0), (3, 4), (4, 4), (5, 3)]
    
    # Find best line
    best_line = find_best_line(datapoints)
    
    # Generate predictions for visualization
    x_values = [point[0] for point in datapoints]
    x_min, x_max = min(x_values), max(x_values)
    
    # Generate line points for visualization
    line_x = [x for x in range(int(x_min) - 1, int(x_max) + 2)]
    line_y = [get_y(best_line['best_m'], best_line['best_b'], x) for x in line_x]
    
    # Calculate predictions for original points
    predictions = [get_y(best_line['best_m'], best_line['best_b'], point[0]) for point in datapoints]
    
    # Calculate R-squared (coefficient of determination)
    y_actual = [point[1] for point in datapoints]
    y_mean = sum(y_actual) / len(y_actual)
    ss_res = sum((y_actual[i] - predictions[i])**2 for i in range(len(y_actual)))
    ss_tot = sum((y - y_mean)**2 for y in y_actual)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    
    return {
        'datapoints': datapoints,
        'best_line': best_line,
        'line_data': {
            'x': line_x,
            'y': line_y
        },
        'predictions': predictions,
        'r_squared': round(r_squared, 3),
        'summary': {
            'total_points': len(datapoints),
            'x_range': (x_min, x_max),
            'y_range': (min(y_actual), max(y_actual))
        }
    }

