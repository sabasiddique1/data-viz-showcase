"""
Page Visits Funnel Analysis Module
Analyzes e-commerce conversion funnel with interactive visualization
"""

from typing import Dict, Any, List
import random


def generate_sample_funnel_data() -> Dict[str, Any]:
    """Generate sample funnel data for demonstration"""
    # Simulate realistic funnel drop-offs
    visits = 1000
    cart = int(visits * 0.65)  # 65% add to cart
    checkout = int(cart * 0.75)  # 75% of cart proceed to checkout
    purchase = int(checkout * 0.85)  # 85% of checkout complete purchase
    
    return {
        'visits': visits,
        'cart': cart,
        'checkout': checkout,
        'purchase': purchase
    }


def analyze_funnel() -> Dict[str, Any]:
    """Main analysis function for funnel analysis"""
    data = generate_sample_funnel_data()
    
    # Calculate conversion rates
    cart_rate = (data['cart'] / data['visits']) * 100
    checkout_rate = (data['checkout'] / data['cart']) * 100 if data['cart'] > 0 else 0
    purchase_rate = (data['purchase'] / data['checkout']) * 100 if data['checkout'] > 0 else 0
    overall_conversion = (data['purchase'] / data['visits']) * 100
    
    # Calculate drop-off rates
    drop_off_visits_to_cart = 100 - cart_rate
    drop_off_cart_to_checkout = 100 - checkout_rate
    drop_off_checkout_to_purchase = 100 - purchase_rate
    
    # Identify weakest step
    drop_offs = {
        'Visits to Cart': drop_off_visits_to_cart,
        'Cart to Checkout': drop_off_cart_to_checkout,
        'Checkout to Purchase': drop_off_checkout_to_purchase
    }
    weakest_step = max(drop_offs, key=drop_offs.get)
    
    # Calculate average time (simulated)
    avg_time_to_cart = 2.5  # minutes
    avg_time_to_checkout = 5.2  # minutes
    avg_time_to_purchase = 8.7  # minutes
    
    return {
        'funnel_data': data,
        'conversion_rates': {
            'cart_rate': round(cart_rate, 2),
            'checkout_rate': round(checkout_rate, 2),
            'purchase_rate': round(purchase_rate, 2),
            'overall_conversion': round(overall_conversion, 2)
        },
        'drop_off_rates': {
            'visits_to_cart': round(drop_off_visits_to_cart, 2),
            'cart_to_checkout': round(drop_off_cart_to_checkout, 2),
            'checkout_to_purchase': round(drop_off_checkout_to_purchase, 2)
        },
        'weakest_step': weakest_step,
        'average_times': {
            'to_cart': avg_time_to_cart,
            'to_checkout': avg_time_to_checkout,
            'to_purchase': avg_time_to_purchase
        },
        'funnel_steps': [
            {'name': 'Visits', 'count': data['visits'], 'percentage': 100},
            {'name': 'Add to Cart', 'count': data['cart'], 'percentage': round(cart_rate, 2)},
            {'name': 'Checkout', 'count': data['checkout'], 'percentage': round(checkout_rate, 2)},
            {'name': 'Purchase', 'count': data['purchase'], 'percentage': round(purchase_rate, 2)}
        ]
    }

