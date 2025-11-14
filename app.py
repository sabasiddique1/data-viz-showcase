"""
Flask Web Application
Displays analysis results from all modules in a browser
"""

from flask import Flask, render_template, jsonify, request
import hurricane_analysis
import medical_system
import cipher_tools
import insurance_web

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

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Starting Flask Web Server...")
    print("="*60)
    print("Open your browser and navigate to: http://localhost:8080")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=8080)

