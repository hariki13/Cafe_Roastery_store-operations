"""Application entry point."""
import os
from app import create_app, db
from app.models import (
    User, RoastProfile, RoastBatch, GreenBeanInventory,
    RoastedCoffeeInventory, InventoryTransaction, CuppingSession,
    CuppingScore, FinancialRecord, ColorMeasurement
)

# Create application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Add database models to shell context."""
    return {
        'db': db,
        'User': User,
        'RoastProfile': RoastProfile,
        'RoastBatch': RoastBatch,
        'GreenBeanInventory': GreenBeanInventory,
        'RoastedCoffeeInventory': RoastedCoffeeInventory,
        'InventoryTransaction': InventoryTransaction,
        'CuppingSession': CuppingSession,
        'CuppingScore': CuppingScore,
        'FinancialRecord': FinancialRecord,
        'ColorMeasurement': ColorMeasurement
    }


@app.cli.command()
def init_db():
    """Initialize the database with sample data."""
    from werkzeug.security import generate_password_hash
    from datetime import datetime, timedelta
    
    print("Creating database tables...")
    db.create_all()
    
    print("Creating admin user...")
    admin = User(
        username='admin',
        email='admin@coffeeroast.com',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    print("Creating roaster user...")
    roaster = User(
        username='roaster',
        email='roaster@coffeeroast.com',
        role='roaster'
    )
    roaster.set_password('roaster123')
    db.session.add(roaster)
    
    print("Creating sample green bean inventory...")
    green_bean = GreenBeanInventory(
        name='Ethiopian Yirgacheffe',
        variety='Heirloom',
        origin='Ethiopia',
        region='Yirgacheffe',
        processing_method='Washed',
        current_stock=50.0,
        unit_cost=12.50,
        supplier_name='Coffee Importers Inc',
        arrival_date=datetime.utcnow() - timedelta(days=30),
        low_stock_threshold=10.0
    )
    green_bean.update_days_since_arrival()
    green_bean.check_low_stock()
    db.session.add(green_bean)
    
    print("Creating sample roast profile...")
    profile = RoastProfile(
        name='Light Ethiopian Roast',
        description='Bright and floral light roast for Ethiopian beans',
        bean_type='Arabica',
        origin='Ethiopia',
        processing_method='Washed',
        target_temp=205.0,
        target_time=720,
        target_roast_level='light',
        development_time=180
    )
    db.session.add(profile)
    
    db.session.commit()
    print("Database initialized successfully!")


if __name__ == '__main__':
    # Only enable debug mode in development environment
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
