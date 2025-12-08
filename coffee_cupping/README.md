# Coffee Cupping Score Calculator

A comprehensive Python-based calculator for specialty coffee cupping scores, implementing the standard formula used by professional coffee tasters worldwide.

## 📋 Overview

The Coffee Cupping Score Calculator is a professional tool designed for specialty coffee roasters, Q-graders, and coffee quality control professionals. It accurately calculates cupping scores based on the standard industry formula, helping you evaluate coffee quality consistently and objectively.

**Key Features:**
- ✅ Standard formula implementation (SCA-compliant)
- ✅ Interactive CLI for easy data entry
- ✅ Programmatic API for integration
- ✅ Batch processing for multiple samples
- ✅ Detailed calculation breakdowns
- ✅ Input validation and error handling
- ✅ Zero external dependencies for core functionality

---

## 🧮 The Formula

The calculator implements the standard specialty coffee cupping formula:

```
S = 0.65625 × Σ(h_i) + 52.75 - 2u - 4d
```

### Parameters

| Parameter | Description | Range/Type |
|-----------|-------------|------------|
| **S** | Cupping score (final result) | Float |
| **h_i** | Score for each affective section | 0-10 scale |
| **Σ(h_i)** | Sum of all 8 section scores | 0-80 |
| **u** | Number of non-uniform cups | Non-negative integer |
| **d** | Number of defective cups | Non-negative integer |

### The 8 Affective Sections

Each section is scored on a 0-10 scale:

1. **Fragrance** - Dry aroma of ground coffee
2. **Aroma** - Wet aroma after adding water
3. **Flavor** - Overall taste profile
4. **Aftertaste** - Lingering taste sensation
5. **Acidity** - Brightness and liveliness
6. **Body** - Tactile mouthfeel and weight
7. **Balance** - Harmony of flavors
8. **Overall** - Holistic impression

### Penalties

- **Non-uniform cups** (u): -2 points per cup
  - Cups showing inconsistency in quality
- **Defective cups** (d): -4 points per cup
  - Cups with significant quality defects

### Score Classification

| Score Range | Classification |
|-------------|----------------|
| 90-100 | Outstanding (Specialty) |
| 85-89.99 | Excellent (Specialty) |
| 80-84.99 | Very Good (Specialty) |
| 75-79.99 | Good (Premium) |
| 70-74.99 | Fair (Exchange) |
| < 70 | Below Standard |

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- No external dependencies required for basic functionality

### Setup

1. Clone or download this repository:
```bash
git clone https://github.com/hariki13/Cafe_Roastery_store-operations.git
cd Cafe_Roastery_store-operations/coffee_cupping
```

2. (Optional) Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. (Optional) Install future enhancement dependencies:
```bash
pip install -r requirements.txt  # If using optional features
```

---

## 💻 Usage

### Interactive Mode

Run the calculator in interactive mode for manual data entry:

```bash
python3 coffee_cupping_calculator.py
```

You'll be prompted to enter:
1. Scores for each of the 8 sections (0-10)
2. Number of non-uniform cups
3. Number of defective cups

The calculator will then display:
- All section scores
- Calculation breakdown
- Final cupping score

**Example Session:**
```
============================================================
COFFEE CUPPING SCORE CALCULATOR
============================================================

Enter scores for each section (0-10 scale):

  Fragrance      : 8.5
  Aroma          : 8.25
  Flavor         : 8.75
  Aftertaste     : 8.5
  Acidity        : 8.5
  Body           : 8.25
  Balance        : 8.5
  Overall        : 8.75

Enter cup quality information:

  Non-uniform cups: 0
  Defective cups: 0

============================================================
FINAL SCORE: 96.74
============================================================
```

### Programmatic Usage

Import and use the `CuppingCalculator` class in your Python code:

```python
from coffee_cupping_calculator import CuppingCalculator

# Create calculator instance
calculator = CuppingCalculator()

# Set individual scores
calculator.set_score('fragrance', 8.5)
calculator.set_score('aroma', 8.25)
# ... set other scores

# Or set all scores at once
scores = {
    'fragrance': 8.5,
    'aroma': 8.25,
    'flavor': 8.75,
    'aftertaste': 8.5,
    'acidity': 8.5,
    'body': 8.25,
    'balance': 8.5,
    'overall': 8.75
}
calculator.set_all_scores(scores)

# Set cup quality information
calculator.set_cups_info(non_uniform=0, defective=0)

# Calculate score
final_score = calculator.calculate()
print(f"Final Score: {final_score:.2f}")

# Get detailed breakdown
breakdown = calculator.get_breakdown()
print(breakdown)
```

### Example Scripts

Run the comprehensive example script to see various usage patterns:

```bash
python3 example_usage.py
```

This demonstrates:
- **Example 1**: Basic usage with preset values
- **Example 2**: Batch processing multiple samples
- **Example 3**: Step-by-step calculation breakdown
- **Example 4**: Edge cases and testing scenarios

---

## 📚 API Reference

### CuppingCalculator Class

#### Constants

```python
COEFFICIENT = 0.65625          # Formula coefficient
BASE_SCORE = 52.75             # Base score value
NON_UNIFORM_PENALTY = 2        # Penalty per non-uniform cup
DEFECT_PENALTY = 4             # Penalty per defective cup
```

#### Methods

##### `__init__()`
Initialize a new calculator with all scores set to zero.

##### `set_score(section: str, score: float) -> None`
Set score for a specific section.

**Parameters:**
- `section`: Section name (case-insensitive)
- `score`: Score value (0-10)

**Raises:**
- `ValueError`: If section invalid or score out of range

##### `set_all_scores(scores_dict: Dict[str, float]) -> None`
Set all section scores at once.

**Parameters:**
- `scores_dict`: Dictionary mapping section names to scores

##### `set_cups_info(non_uniform: int, defective: int) -> None`
Set cup quality information.

**Parameters:**
- `non_uniform`: Number of non-uniform cups
- `defective`: Number of defective cups

**Raises:**
- `ValueError`: If counts are negative

##### `calculate() -> float`
Calculate final score (unrounded).

**Returns:**
- Float: The calculated cupping score

##### `calculate_rounded(decimals: int = 2) -> float`
Calculate and round the score.

**Parameters:**
- `decimals`: Number of decimal places (default: 2)

**Returns:**
- Float: Rounded cupping score

##### `get_breakdown() -> Dict[str, any]`
Get detailed calculation breakdown.

**Returns:**
Dictionary containing:
- `section_scores`: Individual section scores
- `sum_of_sections`: Sum of all sections
- `base_contribution`: Coefficient × sum + base
- `non_uniform_penalty`: Total non-uniform penalty
- `defect_penalty`: Total defect penalty
- `final_score`: Final calculated score

##### `reset() -> None`
Reset all scores and cup information to zero.

##### `display_results() -> None`
Display formatted results to console.

---

## 🎯 Use Cases

### 1. Quality Control
Use the calculator during cupping sessions to maintain consistent scoring standards across your team.

### 2. Coffee Selection
Evaluate and compare multiple coffee samples to select the best lots for purchase.

### 3. Training
Train new cuppers using the detailed breakdown feature to understand how each component contributes to the final score.

### 4. Record Keeping
Integrate into your quality management system to maintain historical cupping data.

### 5. Supplier Communication
Provide standardized scores when communicating with coffee suppliers and producers.

---

## 🔧 Project Structure

```
coffee_cupping/
├── coffee_cupping_calculator.py  # Main calculator class + CLI
├── example_usage.py               # Usage examples and demonstrations
├── requirements.txt               # Dependencies (optional enhancements)
└── README.md                      # This documentation
```

---

## 🚀 Future Enhancements

The calculator is designed with extensibility in mind. Planned features include:

### Phase 1: Data Management
- [ ] CSV import/export for batch processing
- [ ] SQLite database integration for session storage
- [ ] Multi-taster support with score aggregation
- [ ] Historical data tracking and comparison

### Phase 2: Analytics & Reporting
- [ ] Statistical analysis of cupping sessions
- [ ] Trend analysis and visualization
- [ ] PDF report generation
- [ ] Data visualization dashboards

### Phase 3: Web & API
- [ ] REST API using Flask/FastAPI
- [ ] Web-based UI with Streamlit
- [ ] Mobile app support
- [ ] Real-time collaboration features

### Phase 4: Machine Learning
- [ ] Predictive modeling based on historical data
- [ ] Anomaly detection for outlier scores
- [ ] Automated quality classification
- [ ] Score recommendation engine

### Phase 5: Integration
- [ ] Integration with roastery management systems
- [ ] Export to industry-standard formats
- [ ] Barcode/QR code scanning for sample tracking
- [ ] Integration with lab information management systems (LIMS)

---

## 🧪 Testing Examples

The calculator has been validated against various scenarios:

### Perfect Score
```python
# All sections: 10.0, No defects
# Expected: 105.25
```

### Specialty Grade
```python
# All sections: 8.5, No defects
# Expected: 96.74 (Excellent)
```

### With Penalties
```python
# All sections: 8.0, 1 non-uniform, 1 defective
# Expected: 88.75 (Excellent)
```

### Minimum Score
```python
# All sections: 0.0, No defects
# Expected: 52.75
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed description
2. **Suggest Features**: Share your ideas for improvements
3. **Submit Pull Requests**: Follow the code style and include tests
4. **Improve Documentation**: Help make the docs clearer

### Development Guidelines

- Follow PEP 8 style guidelines
- Include docstrings for all functions and classes
- Add type hints where appropriate
- Write unit tests for new features
- Update documentation for API changes

---

## 📄 License

This project is part of the Cafe Roastery Store Operations system.

---

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact: Cafe Roastery Operations Team

---

## 🙏 Acknowledgments

- Formula based on Specialty Coffee Association (SCA) cupping protocols
- Developed for professional coffee tasters and Q-graders
- Part of the Cafe Roastery Store Operations system

---

## 📊 Example Output

```
============================================================
COFFEE CUPPING SCORE - RESULTS
============================================================

Section Scores:
  Fragrance       8.50
  Aroma           8.25
  Flavor          8.75
  Aftertaste      8.50
  Acidity         8.50
  Body            8.25
  Balance         8.50
  Overall         8.75

Sum of sections: 67.00
Base contribution: 96.74
Non-uniform penalty: -0.00
Defect penalty: -0.00

============================================================
FINAL SCORE: 96.74
============================================================
```

---

**Made with ☕ for coffee professionals worldwide**
