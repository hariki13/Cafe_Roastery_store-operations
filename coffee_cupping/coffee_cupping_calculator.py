#!/usr/bin/env python3
"""
Coffee Cupping Score Calculator

This module implements a comprehensive calculator for specialty coffee cupping scores
based on the standard formula: S = 0.65625 × Σ(h_i) + 52.75 - 2u - 4d

Author: Cafe Roastery Store Operations Team
"""

from typing import Dict, List, Optional, Tuple


class CuppingCalculator:
    """
    A calculator for specialty coffee cupping scores following the standard formula.
    
    The formula calculates a cupping score based on 8 affective sections, 
    non-uniform cups, and defective cups:
    S = 0.65625 × Σ(h_i) + 52.75 - 2u - 4d
    
    Attributes:
        COEFFICIENT (float): Multiplier for sum of section scores (0.65625)
        BASE_SCORE (float): Base value added to calculation (52.75)
        NON_UNIFORM_PENALTY (int): Penalty per non-uniform cup (2)
        DEFECT_PENALTY (int): Penalty per defective cup (4)
        SECTIONS (list): Valid section names for scoring
    """
    
    # Formula constants
    COEFFICIENT = 0.65625
    BASE_SCORE = 52.75
    NON_UNIFORM_PENALTY = 2
    DEFECT_PENALTY = 4
    
    # Valid cupping sections (8 affective sections)
    SECTIONS = [
        'fragrance',
        'aroma',
        'flavor',
        'aftertaste',
        'acidity',
        'body',
        'balance',
        'overall'
    ]
    
    def __init__(self):
        """Initialize the cupping calculator with zero scores."""
        self.scores: Dict[str, float] = {section: 0.0 for section in self.SECTIONS}
        self.non_uniform_cups: int = 0
        self.defective_cups: int = 0
    
    def set_score(self, section: str, score: float) -> None:
        """
        Set the score for a specific cupping section.
        
        Args:
            section (str): The section name (case-insensitive)
            score (float): The score value (0-10 scale)
            
        Raises:
            ValueError: If section name is invalid or score is out of range
        """
        section_lower = section.lower()
        
        if section_lower not in self.SECTIONS:
            raise ValueError(
                f"Invalid section '{section}'. Must be one of: {', '.join(self.SECTIONS)}"
            )
        
        if not (0 <= score <= 10):
            raise ValueError(
                f"Score must be between 0 and 10, got {score}"
            )
        
        self.scores[section_lower] = float(score)
    
    def set_all_scores(self, scores_dict: Dict[str, float]) -> None:
        """
        Batch set all section scores at once.
        
        Args:
            scores_dict (dict): Dictionary mapping section names to scores
            
        Raises:
            ValueError: If any section name is invalid or score is out of range
        """
        for section, score in scores_dict.items():
            self.set_score(section, score)
    
    def set_cups_info(self, non_uniform: int, defective: int) -> None:
        """
        Set the cup quality information.
        
        Args:
            non_uniform (int): Number of non-uniform cups
            defective (int): Number of defective cups
            
        Raises:
            ValueError: If counts are negative
        """
        if non_uniform < 0:
            raise ValueError(
                f"Non-uniform cups count must be non-negative, got {non_uniform}"
            )
        
        if defective < 0:
            raise ValueError(
                f"Defective cups count must be non-negative, got {defective}"
            )
        
        self.non_uniform_cups = int(non_uniform)
        self.defective_cups = int(defective)
    
    def calculate(self) -> float:
        """
        Calculate the final cupping score using the standard formula.
        
        Formula: S = 0.65625 × Σ(h_i) + 52.75 - 2u - 4d
        
        Returns:
            float: The calculated cupping score (unrounded)
        """
        sum_of_sections = sum(self.scores.values())
        
        score = (
            self.COEFFICIENT * sum_of_sections +
            self.BASE_SCORE -
            self.NON_UNIFORM_PENALTY * self.non_uniform_cups -
            self.DEFECT_PENALTY * self.defective_cups
        )
        
        return score
    
    def calculate_rounded(self, decimals: int = 2) -> float:
        """
        Calculate and round the cupping score.
        
        Args:
            decimals (int): Number of decimal places (default: 2)
            
        Returns:
            float: The calculated score rounded to specified decimals
        """
        return round(self.calculate(), decimals)
    
    def get_breakdown(self) -> Dict[str, any]:
        """
        Return a detailed breakdown of the calculation.
        
        Returns:
            dict: Dictionary containing:
                - section_scores: Dict of individual section scores
                - sum_of_sections: Sum of all section scores
                - base_contribution: Coefficient × sum + base score
                - non_uniform_penalty: Penalty from non-uniform cups
                - defect_penalty: Penalty from defective cups
                - final_score: The calculated final score
        """
        sum_of_sections = sum(self.scores.values())
        base_contribution = self.COEFFICIENT * sum_of_sections + self.BASE_SCORE
        non_uniform_penalty = self.NON_UNIFORM_PENALTY * self.non_uniform_cups
        defect_penalty = self.DEFECT_PENALTY * self.defective_cups
        final_score = self.calculate()
        
        return {
            'section_scores': self.scores.copy(),
            'sum_of_sections': sum_of_sections,
            'base_contribution': base_contribution,
            'non_uniform_penalty': non_uniform_penalty,
            'defect_penalty': defect_penalty,
            'final_score': final_score
        }
    
    def reset(self) -> None:
        """Reset all scores and cup information to zero."""
        self.scores = {section: 0.0 for section in self.SECTIONS}
        self.non_uniform_cups = 0
        self.defective_cups = 0
    
    def display_results(self) -> None:
        """Display formatted calculation results to console."""
        breakdown = self.get_breakdown()
        
        print("\n" + "=" * 60)
        print("COFFEE CUPPING SCORE - RESULTS")
        print("=" * 60)
        print("\nSection Scores:")
        
        for section in self.SECTIONS:
            score = breakdown['section_scores'][section]
            print(f"  {section.capitalize():15s} {score:5.2f}")
        
        print(f"\nSum of sections: {breakdown['sum_of_sections']:.2f}")
        print(f"Base contribution: {breakdown['base_contribution']:.2f}")
        print(f"Non-uniform penalty: -{breakdown['non_uniform_penalty']:.2f}")
        print(f"Defect penalty: -{breakdown['defect_penalty']:.2f}")
        
        print("\n" + "=" * 60)
        print(f"FINAL SCORE: {breakdown['final_score']:.2f}")
        print("=" * 60 + "\n")


def interactive_cli():
    """
    Run an interactive command-line interface for cupping score calculation.
    
    Prompts the user for section scores and cup information,
    then displays the calculated results.
    """
    print("=" * 60)
    print("COFFEE CUPPING SCORE CALCULATOR")
    print("=" * 60)
    print("\nThis calculator uses the standard cupping formula:")
    print("S = 0.65625 × Σ(h_i) + 52.75 - 2u - 4d")
    print("\nWhere:")
    print("  - h_i: 9-point score for each of 8 sections (0-10 scale)")
    print("  - u: Number of non-uniform cups")
    print("  - d: Number of defective cups")
    print("\n" + "=" * 60)
    
    calculator = CuppingCalculator()
    
    print("\nEnter scores for each section (0-10 scale):\n")
    
    # Collect section scores
    for section in CuppingCalculator.SECTIONS:
        while True:
            try:
                score = float(input(f"  {section.capitalize():15s}: "))
                calculator.set_score(section, score)
                break
            except ValueError as e:
                print(f"    Error: {e}. Please try again.")
    
    # Collect cup quality information
    print("\nEnter cup quality information:\n")
    
    while True:
        try:
            non_uniform = int(input("  Non-uniform cups: "))
            defective = int(input("  Defective cups: "))
            calculator.set_cups_info(non_uniform, defective)
            break
        except ValueError as e:
            print(f"    Error: {e}. Please try again.")
    
    # Display results
    calculator.display_results()
    
    # Display breakdown details
    breakdown = calculator.get_breakdown()
    print("\nCalculation Details:")
    print(f"  Sum of sections (Σh_i) = {breakdown['sum_of_sections']:.2f}")
    print(f"  0.65625 × {breakdown['sum_of_sections']:.2f} + 52.75 = {breakdown['base_contribution']:.2f}")
    print(f"  Non-uniform penalty (2 × {calculator.non_uniform_cups}) = {breakdown['non_uniform_penalty']:.2f}")
    print(f"  Defect penalty (4 × {calculator.defective_cups}) = {breakdown['defect_penalty']:.2f}")
    print(f"  Final Score = {breakdown['final_score']:.2f}")
    print()


if __name__ == "__main__":
    interactive_cli()
