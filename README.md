# Coffee Roasting and Operations Management System

A comprehensive web application for managing specialty coffee shop operations with roasting capabilities. Built with Flask, SQLAlchemy, and Bootstrap 5.

## Features

### 1. Dashboard Module
- Centralized overview of all operations
- Real-time statistics (batches, inventory, financial)
- Recent roast batches display
- Low stock alerts
- Recent cupping scores
- Monthly financial summary

### 2. Roast Profiler Module
- Create and manage roast profiles
- Log individual roast batches
- Track roasting parameters (temperature, time, weight)
- Automatic weight loss calculation
- Profile library with search capabilities

### 3. Inventory Management Module
- **Green Bean Inventory**: Track varieties, origins, stock levels, suppliers
- **Roasted Coffee Inventory**: Track roasted batches, SKUs, shelf life
- Low stock alerts
- Inventory transaction tracking

### 4. Cupping Form Module
- Digital cupping score sheets (SCA protocol)
- Score tracking for all sensory attributes
- Automatic grade calculation (Outstanding to Below Specialty)
- Tasting notes and defects tracking
- Link to specific roast batches

### 5. Financial Management Module
- COGS (Cost of Goods Sold) tracking
- COGM (Cost of Goods Manufactured) calculation
- Revenue and expense tracking
- Profit margin analysis
- Date range filtering for reports

### 6. Coffee Color Analyzer Module
- Manual entry of roast color values (Agtron/Colortrack scale)
- Automatic roast level classification
- Color measurement tracking
- Link to roast batches

### 7. Batch Comparison Feature
- Side-by-side comparison of roast batches
- Compare profiles, yields, costs, and cupping scores
- API endpoint for batch data

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/hariki13/store-operations.git
cd store-operations
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask --app run init-db
```

5. Run the application:
```bash
python run.py
```

6. Access the application at `http://localhost:5000`

## Default Credentials

After initializing the database, use these credentials to log in:

**Admin User:**
- Username: `admin`
- Password: `admin123`

**Roaster User:**
- Username: `roaster`
- Password: `roaster123`

## Project Structure

```
store-operations/
├── app/
│   ├── __init__.py           # Flask application factory
│   ├── models/               # Database models
│   │   ├── user.py          # User authentication
│   │   ├── roast.py         # Roast profiles and batches
│   │   ├── inventory.py     # Inventory management
│   │   ├── cupping.py       # Cupping sessions
│   │   ├── financial.py     # Financial records
│   │   └── color.py         # Color measurements
│   ├── routes/               # API endpoints and views
│   │   ├── auth.py          # Authentication routes
│   │   ├── dashboard.py     # Dashboard
│   │   ├── roast.py         # Roast management
│   │   ├── inventory.py     # Inventory management
│   │   ├── cupping.py       # Cupping forms
│   │   ├── financial.py     # Financial reports
│   │   ├── color.py         # Color analyzer
│   │   └── comparison.py    # Batch comparison
│   ├── static/               # CSS, JS, images
│   │   ├── css/style.css    # Custom styles
│   │   └── js/app.js        # Custom JavaScript
│   └── templates/            # HTML templates
│       ├── base.html        # Base template
│       ├── auth/            # Authentication pages
│       ├── dashboard/       # Dashboard
│       └── [other modules]  # Module-specific templates
├── migrations/               # Database migrations
├── tests/                    # Unit and integration tests
├── config.py                 # Configuration
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── run.py                    # Application entry point
```

## User Roles

- **Admin**: Full access to all modules, can manage users
- **Roaster**: Can create/edit roast profiles and batches, record cupping sessions
- **Viewer**: Read-only access to view data and reports

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout
- `POST /auth/register` - User registration

### Roast Management
- `GET /roast/profiles` - List roast profiles
- `POST /roast/profiles/new` - Create roast profile
- `GET /roast/profiles/<id>` - View profile details
- `GET /roast/batches` - List roast batches
- `POST /roast/batches/new` - Create roast batch

### Inventory
- `GET /inventory` - Inventory overview
- `POST /inventory/green-beans/new` - Add green bean inventory
- `POST /inventory/roasted-coffee/new` - Add roasted coffee inventory

### Cupping
- `GET /cupping` - List cupping sessions
- `POST /cupping/new` - Create cupping session
- `GET /cupping/<id>` - View session details

### Financial
- `GET /financial` - Financial reports
- `POST /financial/new` - Create financial record

### Color Analysis
- `GET /color` - List color measurements
- `POST /color/new` - Create color measurement

### Batch Comparison
- `GET /comparison` - Comparison tool
- `POST /comparison/compare` - Compare batches
- `GET /comparison/api/batch/<id>` - Get batch data (JSON)

## Database Schema

The application uses SQLAlchemy ORM with the following main models:

- **User**: User authentication and roles
- **RoastProfile**: Roast profile templates
- **RoastBatch**: Individual roast sessions
- **GreenBeanInventory**: Green bean stock tracking
- **RoastedCoffeeInventory**: Roasted coffee stock tracking
- **InventoryTransaction**: Inventory movement tracking
- **CuppingSession**: Cupping evaluations (SCA protocol)
- **FinancialRecord**: Financial transactions
- **ColorMeasurement**: Roast color measurements

## Configuration

Edit `config.py` to configure:
- Database URI
- Secret key
- Session lifetime
- File upload settings
- Pagination settings

Environment-specific configs:
- `development`: Debug mode enabled
- `production`: Debug mode disabled, requires SECRET_KEY
- `testing`: In-memory database

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python run.py
```

### Database Migrations
```bash
flask db init
flask db migrate -m "Migration message"
flask db upgrade
```

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Future Enhancements

- Hardware integration for color analyzer devices
- Real-time roast monitoring with temperature sensors
- Mobile app companion
- Multi-location support
- Advanced analytics and machine learning predictions
- Integration with e-commerce platforms
- PDF report generation
- CSV data export

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Copyright © 2024 Coffee Roasting Operations. All rights reserved.

## Support

For issues and questions, please open an issue on GitHub.
