☕ Coffeeshop Operations Optimization System
![Specialty Coffee](https://img.shields.io/badge/Specialty-Coffee-6F4E37?style=flat-square&logo=coffeescript&logoColor=white)
![Roastery](https://img.shields.io/badge/🔥_Roastery-Operations-D2691E?style=flat-square)
![Barista](https://img.shields.io/badge/👨‍🍳_Barista-Tools-8B4513?style=flat-square)
![Quality](https://img.shields.io/badge/✨_Quality-Control-A0522D?style=flat-square)

##📋 Project Overview

A comprehensive operations management system designed specifically for specialty coffee shops, coffee roasteries, and traditional Indonesian warung kopi. This platform combines data analytics, machine learning, and operational tools to optimize every aspect of your coffee business—from bean sourcing and roasting to customer service and sales analytics.

### 🎯 Problem Statement
Coffee shop operators face challenges in: 
- Maintaining consistent roast quality
- Managing inventory efficiently
- Understanding customer preferences
- Optimizing operational costs
- Tracking bean-to-cup quality

### 💡 Solution
An integrated system that provides:
- **Real-time roast quality analysis** using color detection ML models
- **Data-driven insights** for inventory and sales optimization
- **Customer behavior analytics** for personalized service
- **Operational efficiency** tools for cost reduction

---

## ✨ Key Features

### 🏪 Coffee Shop Management
- ✅ **Inventory Tracking** - Real-time monitoring of coffee beans, supplies, and consumables
- ✅ **Point of Sale (POS) Integration** - Streamlined order processing and payment handling
- ✅ **Customer Relationship Management** - Loyalty programs and customer preference tracking
- ✅ **Staff Scheduling** - Optimized shift planning and labor cost management

### 🌱 Specialty Coffee Operations
- ✅ **Bean Origin Tracking** - Farm-to-cup transparency and quality control
- ✅ **Brew Methods Database** - Recipe management for various brewing techniques
- ✅ **Quality Scoring** - Cupping notes and quality assessment tools
- ✅ **Seasonal Menu Management** - Rotating offerings based on bean availability

### 🔥 Roastery Optimization
- ✅ **Batch Roasting Management** - Schedule, profile, and quality tracking
- ✅ **Coffee Color Analyzer** - ML-powered roast level detection ( Light, Medium, Dark, Very Dark)
- ✅ **Green Coffee Inventory** - Supplier management and stock optimization
- ✅ **Production Planning** - Demand forecasting and roast scheduling
- ✅ **Quality Control** - Roast profile consistency and defect tracking

### 📊 Analytics & Reporting
- ✅ **Sales Analytics** - Revenue, trends, and product performance
- ✅ **Cost Analysis** - Profit margins and operational efficiency
- ✅ **Customer Insights** - Purchase patterns and preference analysis
- ✅ **Sustainability Metrics** - Waste reduction and resource optimization

### ☕🍽️ Warung Kopi (Traditional Indonesian Coffee Shop)
Traditional Indonesian Coffee Shop Experience meets modern operations:
- ✅ **Atmospher Management** - comfortable "suasana nyaman" creation
- ✅ **Customer Behavior  Analysis** - Understanding local preferences
- ✅ **Inventory System** - Traditional + modern inventory tracking
- ✅ **Marketing Planning** - Community-focused marketing strategies

---

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **Data Analysis:** Pandas, NumPy
- **Machine Learning:** Scikit-learn, TensorFlow/PyTorch
- **Data Visualization:** Matplotlib, Seaborn
- **Database:** SQLite/PostgreSQL (specify your choice)

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
Git
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/hariki13/Cafe_Roastery_store-operations.git
cd Cafe_Roastery_store-operations
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the data cleaning and analysis**
```bash
python "project 1 cleaning,descriptive analytics.py"
```

5. **Test the coffee color analyzer model**
```bash
python test_color_analyzer.py  # You'll need to create this
```

---

## 📂 Project Structure

```
Cafe_Roastery_store-operations/
├── data/                              # Data directory
│   └── raw/                           # Raw roast level datasets
│       ├── light_roast.csv            # Light roast color data
│       ├── light_medium_roast.csv     # Light-medium roast data
│       ├── medium_roast.csv           # Medium roast data
│       ├── medium_dark_roast.csv      # Medium-dark roast data
│       ├── dark_roast.csv             # Dark roast data
│       └── very_dark_roast.csv        # Very dark roast data
├── models/                            # ML models (to be created)
│   └── coffee color analyzer model   # Trained color detection model
├── src/                               # Source code (to be organized)
│   ├── data_processing/
│   ├── ml_models/
│   └── analytics/
├── notebooks/                         # Jupyter notebooks (optional)
├── tests/                             # Unit tests (to be created)
├── docs/                              # Documentation (to be created)
├── requirements.txt                   # Python dependencies
├── .gitignore                        
└── README.md
```

---

## 📊 Data & Models

### Coffee Roast Level Dataset
The project includes comprehensive roast level data: 
- **5 Roast Categories:** Light, Light-Medium, Medium, Medium-Dark, Very Dark
- **Color Analysis:** RGB values for roast classification
- **Quality Metrics:** Temperature, time, and sensory data

### Machine Learning Model
- **Model Type:** Color-based classification
- **Input:** Coffee bean images or color data
- **Output:** Roast level prediction
- **Accuracy:** [Add your model's accuracy here]

---
## 🔬 Usage Examples

### 1. Data Cleaning & Descriptive Analytics
```python
# Run comprehensive data analysis
python "project 1 cleaning,descriptive analytics.py"

# Output:  Cleaned datasets, statistical summaries, visualizations
```

### 2. Roast Level Prediction
```python
from coffee_color_analyzer import predict_roast_level

# Predict roast level from color data
result = predict_roast_level(rgb_values)
print(f"Roast Level:  {result['level']}, Confidence: {result['confidence']}")

```
## 📈 Roadmap

- [x] Data collection for roast levels
- [x] Basic data cleaning and analytics
- [x] Coffee color analyzer model v1
- [ ] Web dashboard for real-time monitoring
- [ ] Mobile app for on-the-go management
- [ ] Integration with IoT roasting equipment
- [ ] Multi-location support
- [ ] AI-powered demand forecasting
- [ ] Customer mobile ordering system
- [ ] Integration with accounting software (QuickBooks, Xero)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct. 

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Author

**Hariki13**
- GitHub: [@hariki13](https://github.com/hariki13)
- Project Link: [Cafe_Roastery_store-operations](https://github.com/hariki13/Cafe_Roastery_store-operations)

---

## 🙏 Acknowledgments

- Specialty Coffee Association (SCA) for roasting standards
- Coffee roasting community for domain expertise
- Open-source ML libraries that power this project

---

## 📞 Support

If you have questions or need support: 
- **Issues:** [GitHub Issues](https://github.com/hariki13/Cafe_Roastery_store-operations/issues)
- **Discussions:** [GitHub Discussions](https://github.com/hariki13/Cafe_Roastery_store-operations/discussions)

---

**⭐ If you find this project useful, please consider giving it a star! **
```
✅Inventory system 
✅Marketing Planning
