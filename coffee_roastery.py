# --- Coffee Roastery Cost, Inventory, and Weight Loss Management ---
"""
This module provides functionality for:
1. Coffee roastery cost calculation
2. Inventory management for green and roasted beans
3. Weight loss calculation during roasting process

Key concepts:
- Green beans lose weight during roasting (typically 12-20%)
- Cost per kg of roasted coffee must account for this weight loss
- Inventory tracks both green beans and roasted beans separately
"""

import pandas as pd
from datetime import datetime


class CoffeeRoastery:
    """
    A class to manage coffee roastery operations including:
    - Cost tracking for green beans and roasting
    - Inventory management
    - Weight loss calculation during roasting
    """

    def __init__(self):
        """Initialize the roastery with empty inventory and records."""
        # Use lists for storage to avoid FutureWarning with empty DataFrame concatenation
        self._green_bean_records = []
        self._roasted_bean_records = []
        self._roasting_records = []

    @property
    def green_bean_inventory(self):
        """Get green bean inventory as DataFrame."""
        if not self._green_bean_records:
            return pd.DataFrame(columns=[
                'date', 'bean_type', 'quantity_kg', 'cost_per_kg', 'total_cost', 'supplier'
            ])
        return pd.DataFrame(self._green_bean_records)

    @property
    def roasted_bean_inventory(self):
        """Get roasted bean inventory as DataFrame."""
        if not self._roasted_bean_records:
            return pd.DataFrame(columns=[
                'date', 'bean_type', 'green_bean_used_kg', 'roasted_bean_kg',
                'weight_loss_kg', 'weight_loss_percent', 'roasting_cost',
                'green_bean_cost', 'total_cost', 'cost_per_kg_roasted'
            ])
        return pd.DataFrame(self._roasted_bean_records)

    @property
    def roasting_log(self):
        """Get roasting log as DataFrame."""
        if not self._roasting_records:
            return pd.DataFrame(columns=[
                'date', 'batch_id', 'bean_type', 'green_bean_kg', 'roasted_bean_kg',
                'weight_loss_kg', 'weight_loss_percent', 'roast_level', 'duration_minutes'
            ])
        return pd.DataFrame(self._roasting_records)

    def add_green_beans(self, bean_type, quantity_kg, cost_per_kg, supplier=None, date=None):
        """
        Add green beans to inventory.

        Args:
            bean_type (str): Type/origin of green coffee beans
            quantity_kg (float): Quantity in kilograms
            cost_per_kg (float): Cost per kilogram
            supplier (str, optional): Supplier name
            date (datetime, optional): Date of purchase, defaults to today

        Returns:
            dict: Summary of the added inventory
        """
        if date is None:
            date = datetime.now()

        total_cost = quantity_kg * cost_per_kg

        self._green_bean_records.append({
            'date': date,
            'bean_type': bean_type,
            'quantity_kg': float(quantity_kg),
            'cost_per_kg': float(cost_per_kg),
            'total_cost': float(total_cost),
            'supplier': supplier
        })

        return {
            'bean_type': bean_type,
            'quantity_kg': quantity_kg,
            'cost_per_kg': cost_per_kg,
            'total_cost': total_cost,
            'message': f"Added {quantity_kg} kg of {bean_type} green beans to inventory"
        }

    def calculate_weight_loss(self, green_bean_kg, roasted_bean_kg):
        """
        Calculate the weight loss during roasting.

        Args:
            green_bean_kg (float): Weight of green beans before roasting
            roasted_bean_kg (float): Weight of roasted beans after roasting

        Returns:
            dict: Weight loss in kg and percentage
        """
        weight_loss_kg = green_bean_kg - roasted_bean_kg
        weight_loss_percent = (weight_loss_kg / green_bean_kg) * 100

        return {
            'green_bean_kg': green_bean_kg,
            'roasted_bean_kg': roasted_bean_kg,
            'weight_loss_kg': round(weight_loss_kg, 3),
            'weight_loss_percent': round(weight_loss_percent, 2)
        }

    def estimate_roasted_weight(self, green_bean_kg, weight_loss_percent=15):
        """
        Estimate the weight of roasted beans based on expected weight loss.

        Args:
            green_bean_kg (float): Weight of green beans
            weight_loss_percent (float): Expected weight loss percentage (default 15%)

        Returns:
            dict: Estimated roasted weight and weight loss
        """
        weight_loss_kg = green_bean_kg * (weight_loss_percent / 100)
        roasted_bean_kg = green_bean_kg - weight_loss_kg

        return {
            'green_bean_kg': green_bean_kg,
            'estimated_roasted_kg': round(roasted_bean_kg, 3),
            'expected_weight_loss_kg': round(weight_loss_kg, 3),
            'weight_loss_percent': weight_loss_percent
        }

    def roast_beans(self, bean_type, green_bean_kg, roasted_bean_kg, roasting_cost,
                    roast_level='medium', duration_minutes=None, date=None):
        """
        Record a roasting batch and update inventories.

        Args:
            bean_type (str): Type/origin of coffee beans
            green_bean_kg (float): Weight of green beans used
            roasted_bean_kg (float): Weight of roasted beans produced
            roasting_cost (float): Cost of roasting (labor, energy, etc.)
            roast_level (str): Roast level (light, medium, dark)
            duration_minutes (int, optional): Duration of roasting
            date (datetime, optional): Date of roasting

        Returns:
            dict: Summary of the roasting batch including costs
        """
        if date is None:
            date = datetime.now()

        # Calculate weight loss
        weight_loss = self.calculate_weight_loss(green_bean_kg, roasted_bean_kg)

        # Get green bean cost (weighted average if multiple batches)
        green_bean_cost_per_kg = self._get_average_green_bean_cost(bean_type)
        green_bean_cost = green_bean_kg * green_bean_cost_per_kg

        # Calculate total cost and cost per kg of roasted coffee
        total_cost = green_bean_cost + roasting_cost
        cost_per_kg_roasted = total_cost / roasted_bean_kg if roasted_bean_kg > 0 else 0

        # Generate batch ID
        batch_id = f"ROAST-{date.strftime('%Y%m%d')}-{len(self._roasting_records) + 1:04d}"

        # Add to roasting log
        self._roasting_records.append({
            'date': date,
            'batch_id': batch_id,
            'bean_type': bean_type,
            'green_bean_kg': float(green_bean_kg),
            'roasted_bean_kg': float(roasted_bean_kg),
            'weight_loss_kg': float(weight_loss['weight_loss_kg']),
            'weight_loss_percent': float(weight_loss['weight_loss_percent']),
            'roast_level': roast_level,
            'duration_minutes': duration_minutes
        })

        # Add to roasted bean inventory
        self._roasted_bean_records.append({
            'date': date,
            'bean_type': bean_type,
            'green_bean_used_kg': float(green_bean_kg),
            'roasted_bean_kg': float(roasted_bean_kg),
            'weight_loss_kg': float(weight_loss['weight_loss_kg']),
            'weight_loss_percent': float(weight_loss['weight_loss_percent']),
            'roasting_cost': float(roasting_cost),
            'green_bean_cost': float(green_bean_cost),
            'total_cost': float(total_cost),
            'cost_per_kg_roasted': float(cost_per_kg_roasted)
        })

        # Update green bean inventory (reduce quantity)
        self._reduce_green_bean_inventory(bean_type, green_bean_kg)

        return {
            'batch_id': batch_id,
            'bean_type': bean_type,
            'green_bean_kg': green_bean_kg,
            'roasted_bean_kg': roasted_bean_kg,
            'weight_loss_kg': weight_loss['weight_loss_kg'],
            'weight_loss_percent': weight_loss['weight_loss_percent'],
            'green_bean_cost': round(green_bean_cost, 2),
            'roasting_cost': round(roasting_cost, 2),
            'total_cost': round(total_cost, 2),
            'cost_per_kg_roasted': round(cost_per_kg_roasted, 2),
            'roast_level': roast_level,
            'message': f"Roasted {green_bean_kg} kg of {bean_type} green beans → "
                       f"{roasted_bean_kg} kg roasted ({weight_loss['weight_loss_percent']}% weight loss)"
        }

    def _get_average_green_bean_cost(self, bean_type):
        """Get the weighted average cost of green beans for a specific type."""
        bean_records = [r for r in self._green_bean_records if r['bean_type'] == bean_type]
        if not bean_records:
            return 0
        total_quantity = sum(r['quantity_kg'] for r in bean_records)
        if total_quantity == 0:
            return 0
        total_value = sum(r['quantity_kg'] * r['cost_per_kg'] for r in bean_records)
        return total_value / total_quantity

    def _reduce_green_bean_inventory(self, bean_type, quantity_kg):
        """Reduce green bean inventory after roasting (FIFO method)."""
        remaining = quantity_kg
        for record in self._green_bean_records:
            if record['bean_type'] == bean_type:
                available = record['quantity_kg']
                if available <= remaining:
                    remaining -= available
                    record['quantity_kg'] = 0
                else:
                    record['quantity_kg'] -= remaining
                    remaining = 0
                if remaining == 0:
                    break

    def get_green_bean_inventory_summary(self):
        """
        Get a summary of current green bean inventory.

        Returns:
            DataFrame: Summary of green bean inventory by type
        """
        df = self.green_bean_inventory
        if df.empty:
            return pd.DataFrame(columns=['bean_type', 'total_quantity_kg', 'weighted_avg_cost_per_kg', 'total_value'])

        # Filter to only include records with remaining quantity
        df_remaining = df[df['quantity_kg'] > 0].copy()
        if df_remaining.empty:
            return pd.DataFrame(columns=['bean_type', 'total_quantity_kg', 'weighted_avg_cost_per_kg', 'total_value'])

        # Calculate weighted average cost using remaining quantity * cost_per_kg
        df_remaining['remaining_value'] = df_remaining['quantity_kg'] * df_remaining['cost_per_kg']
        
        summary = df_remaining.groupby('bean_type').agg({
            'quantity_kg': 'sum',
            'remaining_value': 'sum'
        }).reset_index()
        
        # Calculate weighted average: remaining_value / remaining_quantity
        summary['weighted_avg_cost_per_kg'] = summary['remaining_value'] / summary['quantity_kg']
        summary.columns = ['bean_type', 'total_quantity_kg', 'total_value', 'weighted_avg_cost_per_kg']
        summary = summary[['bean_type', 'total_quantity_kg', 'weighted_avg_cost_per_kg', 'total_value']]
        return summary

    def get_roasted_bean_inventory_summary(self):
        """
        Get a summary of roasted bean inventory.

        Returns:
            DataFrame: Summary of roasted bean inventory by type
        """
        df = self.roasted_bean_inventory
        if df.empty:
            return pd.DataFrame(columns=['bean_type', 'total_roasted_kg', 'weighted_avg_cost_per_kg', 'total_cost'])

        # Calculate weighted average cost per kg based on quantities
        summary = df.groupby('bean_type').agg({
            'roasted_bean_kg': 'sum',
            'total_cost': 'sum'
        }).reset_index()
        # Calculate weighted average: total_cost / total_roasted_kg
        summary['weighted_avg_cost_per_kg'] = summary['total_cost'] / summary['roasted_bean_kg']
        summary.columns = ['bean_type', 'total_roasted_kg', 'total_cost', 'weighted_avg_cost_per_kg']
        summary = summary[['bean_type', 'total_roasted_kg', 'weighted_avg_cost_per_kg', 'total_cost']]
        return summary

    def get_weight_loss_report(self):
        """
        Generate a report of weight loss across all roasting batches.

        Returns:
            dict: Weight loss statistics and summary
        """
        df = self.roasting_log
        if df.empty:
            return {
                'total_batches': 0,
                'message': 'No roasting records available'
            }

        return {
            'total_batches': len(df),
            'total_green_beans_used_kg': round(df['green_bean_kg'].sum(), 2),
            'total_roasted_beans_produced_kg': round(df['roasted_bean_kg'].sum(), 2),
            'total_weight_loss_kg': round(df['weight_loss_kg'].sum(), 2),
            'average_weight_loss_percent': round(df['weight_loss_percent'].mean(), 2),
            'min_weight_loss_percent': round(df['weight_loss_percent'].min(), 2),
            'max_weight_loss_percent': round(df['weight_loss_percent'].max(), 2),
            'by_roast_level': df.groupby('roast_level')['weight_loss_percent'].mean().to_dict()
        }

    def get_cost_report(self):
        """
        Generate a cost report for roasting operations.

        Returns:
            dict: Cost statistics and breakdown
        """
        df = self.roasted_bean_inventory
        if df.empty:
            return {
                'message': 'No roasting cost records available'
            }

        # Calculate weighted average cost per kg roasted
        total_cost = df['total_cost'].sum()
        total_roasted_kg = df['roasted_bean_kg'].sum()
        weighted_avg_cost = total_cost / total_roasted_kg if total_roasted_kg > 0 else 0

        # Calculate weighted average by bean type
        by_type = df.groupby('bean_type').agg({
            'green_bean_cost': 'sum',
            'roasting_cost': 'sum',
            'total_cost': 'sum',
            'roasted_bean_kg': 'sum'
        })
        by_type['weighted_avg_cost_per_kg'] = by_type['total_cost'] / by_type['roasted_bean_kg']

        return {
            'total_green_bean_cost': round(df['green_bean_cost'].sum(), 2),
            'total_roasting_cost': round(df['roasting_cost'].sum(), 2),
            'total_cost': round(total_cost, 2),
            'weighted_avg_cost_per_kg_roasted': round(weighted_avg_cost, 2),
            'by_bean_type': by_type[['green_bean_cost', 'roasting_cost', 'total_cost', 'weighted_avg_cost_per_kg']].to_dict()
        }

    def calculate_selling_price(self, cost_per_kg_roasted, profit_margin_percent=30):
        """
        Calculate the selling price based on cost and desired profit margin.

        Args:
            cost_per_kg_roasted (float): Cost per kg of roasted coffee
            profit_margin_percent (float): Desired profit margin percentage

        Returns:
            dict: Price breakdown including suggested selling price
        """
        profit = cost_per_kg_roasted * (profit_margin_percent / 100)
        selling_price = cost_per_kg_roasted + profit

        return {
            'cost_per_kg': round(cost_per_kg_roasted, 2),
            'profit_margin_percent': profit_margin_percent,
            'profit_per_kg': round(profit, 2),
            'suggested_selling_price_per_kg': round(selling_price, 2)
        }

    def export_to_csv(self, filepath_prefix='roastery_data'):
        """
        Export all data to CSV files.

        Args:
            filepath_prefix (str): Prefix for output file names
        """
        self.green_bean_inventory.to_csv(f'{filepath_prefix}_green_beans.csv', index=False)
        self.roasted_bean_inventory.to_csv(f'{filepath_prefix}_roasted_beans.csv', index=False)
        self.roasting_log.to_csv(f'{filepath_prefix}_roasting_log.csv', index=False)
        print(f"Data exported to {filepath_prefix}_*.csv files")


# --- Example Usage ---
if __name__ == "__main__":
    # Create a roastery instance
    roastery = CoffeeRoastery()

    print("=" * 60)
    print("COFFEE ROASTERY - COST, INVENTORY & WEIGHT LOSS MANAGEMENT")
    print("=" * 60)

    # --- Step 1: Add green beans to inventory ---
    print("\n--- STEP 1: Adding Green Beans to Inventory ---")

    # Add different types of green beans
    result = roastery.add_green_beans(
        bean_type='Ethiopian Yirgacheffe',
        quantity_kg=50,
        cost_per_kg=15.00,
        supplier='African Coffee Traders'
    )
    print(f"✓ {result['message']}")
    print(f"  Cost: ${result['total_cost']:.2f}")

    result = roastery.add_green_beans(
        bean_type='Colombian Supremo',
        quantity_kg=40,
        cost_per_kg=12.50,
        supplier='South American Imports'
    )
    print(f"✓ {result['message']}")
    print(f"  Cost: ${result['total_cost']:.2f}")

    result = roastery.add_green_beans(
        bean_type='Sumatra Mandheling',
        quantity_kg=30,
        cost_per_kg=14.00,
        supplier='Indonesian Beans Co'
    )
    print(f"✓ {result['message']}")
    print(f"  Cost: ${result['total_cost']:.2f}")

    # --- Step 2: Show green bean inventory ---
    print("\n--- STEP 2: Green Bean Inventory Summary ---")
    green_summary = roastery.get_green_bean_inventory_summary()
    print(green_summary.to_string(index=False))

    # --- Step 3: Estimate roasted weight ---
    print("\n--- STEP 3: Weight Loss Estimation ---")
    estimate = roastery.estimate_roasted_weight(green_bean_kg=10, weight_loss_percent=15)
    print(f"If roasting 10 kg of green beans with 15% weight loss:")
    print(f"  Expected roasted weight: {estimate['estimated_roasted_kg']} kg")
    print(f"  Expected weight loss: {estimate['expected_weight_loss_kg']} kg")

    # --- Step 4: Roast beans ---
    print("\n--- STEP 4: Roasting Batches ---")

    # Roast Ethiopian beans - Light roast (less weight loss)
    result = roastery.roast_beans(
        bean_type='Ethiopian Yirgacheffe',
        green_bean_kg=10,
        roasted_bean_kg=8.7,  # 13% weight loss for light roast
        roasting_cost=25.00,  # Labor, energy, etc.
        roast_level='light',
        duration_minutes=12
    )
    print(f"\n✓ Batch {result['batch_id']}:")
    print(f"  {result['message']}")
    print(f"  Green bean cost: ${result['green_bean_cost']}")
    print(f"  Roasting cost: ${result['roasting_cost']}")
    print(f"  TOTAL COST: ${result['total_cost']}")
    print(f"  Cost per kg roasted: ${result['cost_per_kg_roasted']}")

    # Roast Colombian beans - Medium roast
    result = roastery.roast_beans(
        bean_type='Colombian Supremo',
        green_bean_kg=15,
        roasted_bean_kg=12.75,  # 15% weight loss for medium roast
        roasting_cost=35.00,
        roast_level='medium',
        duration_minutes=14
    )
    print(f"\n✓ Batch {result['batch_id']}:")
    print(f"  {result['message']}")
    print(f"  Green bean cost: ${result['green_bean_cost']}")
    print(f"  Roasting cost: ${result['roasting_cost']}")
    print(f"  TOTAL COST: ${result['total_cost']}")
    print(f"  Cost per kg roasted: ${result['cost_per_kg_roasted']}")

    # Roast Sumatra beans - Dark roast (more weight loss)
    result = roastery.roast_beans(
        bean_type='Sumatra Mandheling',
        green_bean_kg=12,
        roasted_bean_kg=9.84,  # 18% weight loss for dark roast
        roasting_cost=30.00,
        roast_level='dark',
        duration_minutes=16
    )
    print(f"\n✓ Batch {result['batch_id']}:")
    print(f"  {result['message']}")
    print(f"  Green bean cost: ${result['green_bean_cost']}")
    print(f"  Roasting cost: ${result['roasting_cost']}")
    print(f"  TOTAL COST: ${result['total_cost']}")
    print(f"  Cost per kg roasted: ${result['cost_per_kg_roasted']}")

    # --- Step 5: Weight Loss Report ---
    print("\n--- STEP 5: Weight Loss Report ---")
    weight_report = roastery.get_weight_loss_report()
    print(f"Total batches roasted: {weight_report['total_batches']}")
    print(f"Total green beans used: {weight_report['total_green_beans_used_kg']} kg")
    print(f"Total roasted beans produced: {weight_report['total_roasted_beans_produced_kg']} kg")
    print(f"Total weight lost: {weight_report['total_weight_loss_kg']} kg")
    print(f"Average weight loss: {weight_report['average_weight_loss_percent']}%")
    print(f"\nWeight loss by roast level:")
    for level, loss in weight_report['by_roast_level'].items():
        print(f"  {level}: {loss:.2f}%")

    # --- Step 6: Cost Report ---
    print("\n--- STEP 6: Cost Report ---")
    cost_report = roastery.get_cost_report()
    print(f"Total green bean cost: ${cost_report['total_green_bean_cost']}")
    print(f"Total roasting cost: ${cost_report['total_roasting_cost']}")
    print(f"TOTAL COST: ${cost_report['total_cost']}")
    print(f"Weighted average cost per kg roasted: ${cost_report['weighted_avg_cost_per_kg_roasted']}")

    # --- Step 7: Calculate selling price ---
    print("\n--- STEP 7: Pricing Calculation ---")
    avg_cost = cost_report['weighted_avg_cost_per_kg_roasted']
    pricing = roastery.calculate_selling_price(avg_cost, profit_margin_percent=40)
    print(f"Cost per kg: ${pricing['cost_per_kg']}")
    print(f"Profit margin: {pricing['profit_margin_percent']}%")
    print(f"Profit per kg: ${pricing['profit_per_kg']}")
    print(f"Suggested selling price: ${pricing['suggested_selling_price_per_kg']} per kg")

    # --- Step 8: Updated inventory after roasting ---
    print("\n--- STEP 8: Updated Inventory Status ---")
    print("\nGreen Bean Inventory (after roasting):")
    green_summary = roastery.get_green_bean_inventory_summary()
    print(green_summary.to_string(index=False))

    print("\nRoasted Bean Inventory:")
    roasted_summary = roastery.get_roasted_bean_inventory_summary()
    print(roasted_summary.to_string(index=False))

    # --- Step 9: Export data ---
    print("\n--- STEP 9: Export Data ---")
    roastery.export_to_csv('coffee_roastery')

    print("\n" + "=" * 60)
    print("ROASTERY MANAGEMENT COMPLETE")
    print("=" * 60)
