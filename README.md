# Coffee Supply Chain & Retail Analytics

A comprehensive data analytics solution specializing in Coffee Supply Chain & Retail Analytics. This project provides tools for optimizing operations in coffee shops, specialty coffee retailers, and WARKOP (Indonesian coffee stall) systems.

## 🎯 Project Overview

This analytics platform helps coffee businesses make data-driven decisions by analyzing:
- **Sales Performance**: Track revenue, identify top products, and analyze sales trends
- **Supply Chain Efficiency**: Monitor inventory levels, supplier performance, and lead times
- **Retail Operations**: Understand customer behavior, peak hours, and seasonal patterns
- **Profitability Analysis**: Calculate margins, track waste, and optimize pricing

## 📊 Analytics Modules

### 1. Descriptive Analytics (`project 1 cleaning,descriptive analytics.py`)
- Data cleaning and preprocessing
- Basic sales statistics (total, average, min, max)
- Product performance analysis
- Daily sales trend visualization

### 2. Supply Chain Analytics (`supply_chain_analytics.py`)
- Inventory turnover analysis
- Reorder point calculations
- Supplier performance metrics
- Lead time analysis
- Stock-out risk assessment

### 3. Retail Analytics (`retail_analytics.py`)
- Peak hours analysis
- Customer purchase patterns
- Product basket analysis
- Sales forecasting
- Seasonal trend detection

### 4. Coffee Metrics (`coffee_metrics.py`)
- Product profitability analysis
- Waste tracking and analysis
- Category performance comparison
- Revenue per product metrics
- Trend analysis by product type

## 🛠️ Technologies Used

- **Python 3.x**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Matplotlib & Seaborn**: Data visualization
- **NumPy**: Numerical computations

## 📁 Project Structure

```
store-operations/
├── README.md
├── .gitignore
├── project 1 cleaning,descriptive analytics.py  # Basic descriptive analytics
├── supply_chain_analytics.py                     # Supply chain analysis module
├── retail_analytics.py                           # Retail operations analytics
├── coffee_metrics.py                             # Coffee-specific metrics
└── data/                                         # Data directory (not tracked)
    └── coffee sales dataset.csv                  # Sample sales data
```

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas matplotlib seaborn numpy
```

### Running the Analytics

1. **Basic Descriptive Analytics**:
```bash
python "project 1 cleaning,descriptive analytics.py"
```

2. **Supply Chain Analytics**:
```bash
python supply_chain_analytics.py
```

3. **Retail Analytics**:
```bash
python retail_analytics.py
```

4. **Coffee Metrics**:
```bash
python coffee_metrics.py
```

## 📈 Sample Outputs

The analytics modules generate:
- Statistical summaries in console output
- Visualization charts (PNG files)
- Cleaned/processed data (CSV files)

## 🔧 Configuration

Each module can be configured by modifying the data file path at the top of each script. Default path: `coffee sales dataset.csv`

## 📝 Data Requirements

The analytics modules expect a CSV file with the following columns:
- `datetime`: Transaction timestamp
- `coffee_name`: Name of the coffee product
- `money`: Transaction amount
- Additional columns for extended analytics (e.g., `cash_type`, `card`)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests for:
- New analytics features
- Bug fixes
- Documentation improvements
- Performance optimizations

## 📄 License

This project is open source and available for educational and commercial use.

---
*Specializing in Coffee Supply Chain & Retail Analytics*
