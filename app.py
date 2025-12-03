"""
Flask Web Application
Displays analysis results from all modules in a browser
"""

from flask import Flask, render_template, jsonify, request
import hurricane_analysis
import medical_system
import cipher_tools
import insurance_web
import linear_regression
import funnel_analysis
import student_analysis
import nba_analysis
import mushroom_analysis
import airline_analysis
import life_expectancy_analysis
import census_analysis

app = Flask(__name__)

@app.route('/')
def index():
    """Main page with menu"""
    return render_template('index.html')

@app.route('/hurricane')
def hurricane():
    """Hurricane analysis page"""
    try:
        results = hurricane_analysis.analyze_hurricanes()
        return render_template('hurricane.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/medical')
def medical():
    """Medical system page"""
    try:
        results = medical_system.analyze_medical_records()
        return render_template('medical.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/cipher')
def cipher():
    """Cipher tools page"""
    try:
        results = cipher_tools.analyze_cipher_tools()
        return render_template('cipher.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/insurance')
def insurance():
    """Insurance analysis page"""
    try:
        results = insurance_web.analyze_insurance()
        return render_template('insurance.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/cipher/encrypt', methods=['POST'])
def encrypt_text():
    """API endpoint for encryption"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        cipher_type = data.get('cipher_type', 'caesar')
        shift = data.get('shift', 3)
        
        cipher = cipher_tools.CipherTools()
        
        if cipher_type == 'caesar':
            result = cipher.caesar_cipher(text, shift, encrypt=True)
        elif cipher_type == 'reverse':
            result = cipher.reverse_cipher(text)
        elif cipher_type == 'atbash':
            result = cipher.atbash_cipher(text)
        else:
            result = text
        
        return jsonify({'encrypted': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/cipher/decrypt', methods=['POST'])
def decrypt_text():
    """API endpoint for decryption"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        cipher_type = data.get('cipher_type', 'caesar')
        shift = data.get('shift', 3)
        
        cipher = cipher_tools.CipherTools()
        
        if cipher_type == 'caesar':
            result = cipher.caesar_cipher(text, shift, encrypt=False)
        elif cipher_type == 'reverse':
            result = cipher.reverse_cipher(text)
        elif cipher_type == 'atbash':
            result = cipher.atbash_cipher(text)
        else:
            result = text
        
        return jsonify({'decrypted': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/hurricane')
def api_hurricane():
    """API endpoint for hurricane data"""
    return jsonify(hurricane_analysis.analyze_hurricanes())

@app.route('/api/medical')
def api_medical():
    """API endpoint for medical data"""
    return jsonify(medical_system.analyze_medical_records())

@app.route('/api/cipher')
def api_cipher():
    """API endpoint for cipher data"""
    return jsonify(cipher_tools.analyze_cipher_tools())

@app.route('/api/insurance')
def api_insurance():
    """API endpoint for insurance data"""
    return jsonify(insurance_web.analyze_insurance())

@app.route('/api/insurance/raw')
def api_insurance_raw():
    """API endpoint for raw insurance data for filtering"""
    try:
        raw_data = insurance_web.load_insurance_data()
        # Convert to list of records for easier filtering
        records = []
        for i in range(len(raw_data['ages'])):
            records.append({
                'age': raw_data['ages'][i],
                'sex': raw_data['sexes'][i],
                'bmi': raw_data['bmis'][i],
                'children': raw_data['num_children'][i],
                'smoker': raw_data['smoker_statuses'][i],
                'region': raw_data['regions'][i],
                'charges': raw_data['insurance_charges'][i]
            })
        return jsonify(records)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/regression')
def regression():
    """Linear regression analysis page"""
    try:
        results = linear_regression.analyze_linear_regression()
        return render_template('regression.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/funnel')
def funnel():
    """Funnel analysis page"""
    try:
        results = funnel_analysis.analyze_funnel()
        return render_template('funnel.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/students')
def students():
    """Student analysis page"""
    try:
        results = student_analysis.analyze_students()
        return render_template('students.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/nba')
def nba():
    """NBA trends analysis page"""
    try:
        results = nba_analysis.analyze_nba()
        return render_template('nba.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/regression')
def api_regression():
    """API endpoint for regression data"""
    return jsonify(linear_regression.analyze_linear_regression())

@app.route('/api/funnel')
def api_funnel():
    """API endpoint for funnel data"""
    return jsonify(funnel_analysis.analyze_funnel())

@app.route('/api/students')
def api_students():
    """API endpoint for student data"""
    return jsonify(student_analysis.analyze_students())

@app.route('/api/nba')
def api_nba():
    """API endpoint for NBA data"""
    return jsonify(nba_analysis.analyze_nba())

@app.route('/mushrooms')
def mushrooms():
    """Mushroom analysis page"""
    try:
        results = mushroom_analysis.analyze_mushrooms()
        return render_template('mushrooms.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/airline')
def airline():
    """Airline analysis page"""
    try:
        results = airline_analysis.analyze_airline()
        return render_template('airline.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/life-expectancy')
def life_expectancy():
    """Life expectancy analysis page"""
    try:
        results = life_expectancy_analysis.analyze_life_expectancy()
        return render_template('life_expectancy.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/census')
def census():
    """Census analysis page"""
    try:
        results = census_analysis.analyze_census()
        return render_template('census.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/mushrooms')
def api_mushrooms():
    """API endpoint for mushroom data"""
    return jsonify(mushroom_analysis.analyze_mushrooms())

@app.route('/api/airline')
def api_airline():
    """API endpoint for airline data"""
    return jsonify(airline_analysis.analyze_airline())

@app.route('/api/life-expectancy')
def api_life_expectancy():
    """API endpoint for life expectancy data"""
    return jsonify(life_expectancy_analysis.analyze_life_expectancy())

@app.route('/api/census')
def api_census():
    """API endpoint for census data"""
    return jsonify(census_analysis.analyze_census())

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*60)
    print("Starting Flask Web Server...")
    print("="*60)
    print(f"Open your browser and navigate to: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

