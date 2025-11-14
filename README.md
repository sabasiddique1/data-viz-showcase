# Data Viz Showcase

A comprehensive Python web application featuring interactive data analysis dashboards, medical records management, encryption tools, and insurance cost analysis. Built with Flask and Chart.js for real-time data visualization.

## 🚀 Features

### 📊 Interactive Data Analysis Modules

- **Hurricane Analysis**: Analyze hurricane data including wind speeds, categories, damage costs, and affected areas with interactive charts
- **Medical Records System**: Manage and analyze patient medical records, diagnoses, medications, and vital signs
- **Insurance Cost Analysis**: Comprehensive analysis of medical insurance costs by demographics, lifestyle factors, and geographic regions
- **Cipher Tools**: Encryption and decryption tools including Caesar cipher, Reverse cipher, and Atbash cipher

### 🎨 Web Dashboard

- Modern, responsive web interface built with Flask
- Interactive charts and visualizations using Chart.js
- Real-time data analysis and filtering
- Beautiful UI with smooth animations and transitions

## 🛠️ Technologies

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualization**: Chart.js
- **Icons**: Font Awesome

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/data-viz-showcase.git
cd data-viz-showcase
```

2. Install dependencies (if needed):
```bash
# No external dependencies required - uses only Python standard library
```

3. Run the application:
```bash
python3 app.py
```

4. Open your browser and navigate to:
```
http://localhost:8080
```

## 📁 Project Structure

```
python_megaproject/
├── app.py                      # Flask web application
├── hurricane_analysis.py       # Hurricane data analysis module
├── medical_system.py            # Medical records system
├── cipher_tools.py              # Encryption/decryption tools
├── insurance_web.py             # Insurance analysis web module
├── insurance_analysis/          # Standalone insurance analysis project
│   ├── insurance_analysis.py   # Functional analysis script
│   ├── insurance_analysis_class.py  # OOP analysis script
│   └── README.md                # Insurance project documentation
├── templates/                   # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── hurricane.html
│   ├── medical.html
│   ├── cipher.html
│   └── insurance.html
├── static/
│   └── css/
│       └── style.css           # Styling
└── data/                       # Data files
    ├── hurricanes.json
    ├── medical_records.json
    └── insurance.csv
```

## 🎯 Modules

### Hurricane Analysis
- Statistical analysis of hurricane data
- Category distribution charts
- Damage over time visualization
- Wind speed comparisons
- Searchable and filterable data table

### Medical Records System
- Patient record management
- Diagnosis tracking
- Medication management
- Vital signs monitoring
- Statistical analysis

### Insurance Cost Analysis
- Analysis by smoker status (280% cost difference!)
- Regional cost comparisons
- Gender-based analysis
- BMI category impact
- Age group analysis
- Children factor analysis
- Interactive charts and visualizations

### Cipher Tools
- Caesar cipher encryption/decryption
- Reverse cipher
- Atbash cipher
- Real-time encryption/decryption

## 📊 Key Insights

### Insurance Analysis Findings:
- **Smoking Impact**: Smokers pay 280% more on average than non-smokers
- **Regional Differences**: Southeast has highest costs, Southwest has lowest
- **BMI Impact**: Obese individuals pay 49% more than normal BMI
- **Age Correlation**: Older individuals have significantly higher costs

## 🎓 Learning Outcomes

This project demonstrates:
- Data analysis and visualization
- Web application development with Flask
- Interactive dashboard creation
- Data manipulation and statistics
- Object-oriented programming
- API development
- Frontend-backend integration

## 📝 License

This project is for educational and portfolio purposes.

## 👤 Author

Created as a comprehensive portfolio project demonstrating data analysis and web development skills.

---

**Note**: This project includes both a web application and standalone analysis scripts. The insurance analysis can be run independently or viewed through the web interface.