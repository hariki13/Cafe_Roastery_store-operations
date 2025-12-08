#!/usr/bin/env python3
"""
Coffee Cupping Calculator - Example Usage

This script demonstrates various ways to use the CuppingCalculator class,
including basic usage, batch processing, and detailed breakdowns.

Author: Cafe Roastery Store Operations Team
"""

from coffee_cupping_calculator import CuppingCalculator


def example_1_basic_usage():
    """
    Example 1: Basic Usage
    
    Demonstrates simple calculation with preset values for a single coffee sample.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 1: BASIC USAGE")
    print("=" * 60)
    
    # Create calculator instance
    calculator = CuppingCalculator()
    
    # Set individual section scores
    calculator.set_score('fragrance', 8.5)
    calculator.set_score('aroma', 8.25)
    calculator.set_score('flavor', 8.75)
    calculator.set_score('aftertaste', 8.5)
    calculator.set_score('acidity', 8.5)
    calculator.set_score('body', 8.25)
    calculator.set_score('balance', 8.5)
    calculator.set_score('overall', 8.75)
    
    # Set cup quality information
    calculator.set_cups_info(non_uniform=0, defective=0)
    
    # Calculate and display
    calculator.display_results()


def example_2_batch_processing():
    """
    Example 2: Batch Processing
    
    Demonstrates processing multiple coffee samples and ranking them.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: BATCH PROCESSING - MULTIPLE SAMPLES")
    print("=" * 60)
    
    # Sample data for different coffee types
    coffee_samples = [
        {
            'name': 'Ethiopian Yirgacheffe',
            'origin': 'Ethiopia',
            'grade': 'Specialty Grade',
            'scores': {
                'fragrance': 9.0,
                'aroma': 9.25,
                'flavor': 9.5,
                'aftertaste': 9.0,
                'acidity': 9.25,
                'body': 8.5,
                'balance': 9.0,
                'overall': 9.25
            },
            'non_uniform': 0,
            'defective': 0
        },
        {
            'name': 'Colombian Supremo',
            'origin': 'Colombia',
            'grade': 'Premium Grade',
            'scores': {
                'fragrance': 8.0,
                'aroma': 8.25,
                'flavor': 8.5,
                'aftertaste': 8.0,
                'acidity': 8.25,
                'body': 8.5,
                'balance': 8.25,
                'overall': 8.5
            },
            'non_uniform': 1,
            'defective': 0
        },
        {
            'name': 'Brazilian Santos',
            'origin': 'Brazil',
            'grade': 'Good Grade',
            'scores': {
                'fragrance': 7.5,
                'aroma': 7.75,
                'flavor': 8.0,
                'aftertaste': 7.5,
                'acidity': 7.75,
                'body': 8.25,
                'balance': 7.75,
                'overall': 8.0
            },
            'non_uniform': 0,
            'defective': 1
        }
    ]
    
    # Process all samples and collect results
    results = []
    
    for sample in coffee_samples:
        calculator = CuppingCalculator()
        
        # Use batch set method for all scores
        calculator.set_all_scores(sample['scores'])
        calculator.set_cups_info(sample['non_uniform'], sample['defective'])
        
        # Calculate score
        score = calculator.calculate_rounded(2)
        
        results.append({
            'name': sample['name'],
            'origin': sample['origin'],
            'grade': sample['grade'],
            'score': score,
            'non_uniform': sample['non_uniform'],
            'defective': sample['defective']
        })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Display ranking
    print("\n" + "-" * 60)
    print("CUPPING RESULTS RANKING")
    print("-" * 60)
    
    for rank, result in enumerate(results, 1):
        print(f"\n#{rank} - {result['name']}")
        print(f"     Origin: {result['origin']}")
        print(f"     Grade: {result['grade']}")
        print(f"     Score: {result['score']:.2f}")
        print(f"     Non-uniform cups: {result['non_uniform']}")
        print(f"     Defective cups: {result['defective']}")
    
    print("\n" + "-" * 60)
    print(f"\nHighest Score: {results[0]['name']} - {results[0]['score']:.2f}")
    print(f"Lowest Score: {results[-1]['name']} - {results[-1]['score']:.2f}")
    print(f"Score Range: {results[0]['score'] - results[-1]['score']:.2f} points")
    print()


def example_3_detailed_breakdown():
    """
    Example 3: Detailed Breakdown
    
    Demonstrates step-by-step calculation breakdown for educational purposes.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: DETAILED BREAKDOWN")
    print("=" * 60)
    print("\nSample: Ethiopian Yirgacheffe (High Quality Specialty Coffee)")
    
    calculator = CuppingCalculator()
    
    # Set scores using dictionary
    scores = {
        'fragrance': 9.0,
        'aroma': 9.25,
        'flavor': 9.5,
        'aftertaste': 9.0,
        'acidity': 9.25,
        'body': 8.5,
        'balance': 9.0,
        'overall': 9.25
    }
    
    calculator.set_all_scores(scores)
    calculator.set_cups_info(non_uniform=0, defective=0)
    
    # Get detailed breakdown
    breakdown = calculator.get_breakdown()
    
    print("\n" + "-" * 60)
    print("STEP-BY-STEP CALCULATION")
    print("-" * 60)
    
    print("\nStep 1: Section Scores (0-10 scale)")
    for section, score in breakdown['section_scores'].items():
        print(f"  {section.capitalize():15s} = {score:.2f}")
    
    print(f"\nStep 2: Sum of all sections (Σh_i)")
    print(f"  {breakdown['sum_of_sections']:.2f}")
    
    print(f"\nStep 3: Apply coefficient and add base score")
    print(f"  0.65625 × {breakdown['sum_of_sections']:.2f} + 52.75")
    print(f"  = {calculator.COEFFICIENT * breakdown['sum_of_sections']:.2f} + 52.75")
    print(f"  = {breakdown['base_contribution']:.2f}")
    
    print(f"\nStep 4: Apply penalties")
    print(f"  Non-uniform cups: {calculator.non_uniform_cups} × 2 = {breakdown['non_uniform_penalty']:.2f}")
    print(f"  Defective cups: {calculator.defective_cups} × 4 = {breakdown['defect_penalty']:.2f}")
    
    print(f"\nStep 5: Calculate final score")
    print(f"  {breakdown['base_contribution']:.2f} - {breakdown['non_uniform_penalty']:.2f} - {breakdown['defect_penalty']:.2f}")
    print(f"  = {breakdown['final_score']:.2f}")
    
    print("\n" + "-" * 60)
    print("FINAL RESULT")
    print("-" * 60)
    print(f"\nCupping Score: {breakdown['final_score']:.2f}")
    print(f"Rounded (2 decimals): {calculator.calculate_rounded(2):.2f}")
    
    # Grade classification
    score = breakdown['final_score']
    if score >= 90:
        grade = "Outstanding (Specialty Grade)"
    elif score >= 85:
        grade = "Excellent (Specialty Grade)"
    elif score >= 80:
        grade = "Very Good (Specialty Grade)"
    elif score >= 75:
        grade = "Good (Premium Grade)"
    elif score >= 70:
        grade = "Fair (Exchange Grade)"
    else:
        grade = "Below Standard"
    
    print(f"Classification: {grade}")
    print()


def example_4_edge_cases():
    """
    Example 4: Edge Cases and Testing
    
    Demonstrates various edge cases and validation scenarios.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: EDGE CASES AND TESTING")
    print("=" * 60)
    
    # Test Case 1: Perfect Score
    print("\n" + "-" * 60)
    print("Test Case 1: Perfect Score (All 10s, No Defects)")
    print("-" * 60)
    
    calculator = CuppingCalculator()
    perfect_scores = {section: 10.0 for section in CuppingCalculator.SECTIONS}
    calculator.set_all_scores(perfect_scores)
    calculator.set_cups_info(0, 0)
    
    print(f"Sum of sections: {sum(perfect_scores.values()):.2f}")
    print(f"Final Score: {calculator.calculate_rounded(2):.2f}")
    
    # Test Case 2: Maximum Penalties
    print("\n" + "-" * 60)
    print("Test Case 2: Good Coffee with Maximum Penalties")
    print("-" * 60)
    
    calculator.reset()
    good_scores = {section: 8.0 for section in CuppingCalculator.SECTIONS}
    calculator.set_all_scores(good_scores)
    calculator.set_cups_info(non_uniform=3, defective=2)
    
    breakdown = calculator.get_breakdown()
    print(f"Sum of sections: {breakdown['sum_of_sections']:.2f}")
    print(f"Non-uniform penalty: -{breakdown['non_uniform_penalty']:.2f}")
    print(f"Defect penalty: -{breakdown['defect_penalty']:.2f}")
    print(f"Final Score: {calculator.calculate_rounded(2):.2f}")
    
    # Test Case 3: Minimum Score
    print("\n" + "-" * 60)
    print("Test Case 3: Minimum Score (All 0s)")
    print("-" * 60)
    
    calculator.reset()
    # No need to set scores, they're already 0
    print(f"Sum of sections: {sum(calculator.scores.values()):.2f}")
    print(f"Final Score: {calculator.calculate_rounded(2):.2f}")
    
    # Test Case 4: Average Score
    print("\n" + "-" * 60)
    print("Test Case 4: Average Commercial Coffee")
    print("-" * 60)
    
    calculator.reset()
    avg_scores = {section: 7.0 for section in CuppingCalculator.SECTIONS}
    calculator.set_all_scores(avg_scores)
    calculator.set_cups_info(non_uniform=1, defective=0)
    
    breakdown = calculator.get_breakdown()
    print(f"Sum of sections: {breakdown['sum_of_sections']:.2f}")
    print(f"Non-uniform penalty: -{breakdown['non_uniform_penalty']:.2f}")
    print(f"Final Score: {calculator.calculate_rounded(2):.2f}")
    
    print()


def main():
    """
    Main function to run all examples.
    """
    print("\n" + "=" * 60)
    print("COFFEE CUPPING CALCULATOR - USAGE EXAMPLES")
    print("=" * 60)
    print("\nThis script demonstrates various features of the")
    print("Coffee Cupping Score Calculator system.")
    
    # Run all examples
    example_1_basic_usage()
    example_2_batch_processing()
    example_3_detailed_breakdown()
    example_4_edge_cases()
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)
    print("\nFor interactive mode, run:")
    print("  python3 coffee_cupping_calculator.py")
    print("\nFor integration into your own code, import:")
    print("  from coffee_cupping_calculator import CuppingCalculator")
    print()


if __name__ == "__main__":
    main()
