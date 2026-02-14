"""
Unit tests for Calculation, CalculationHistory, and CalculationFactory.

This module tests the calculation management classes including
the Factory pattern and history management.
"""

import pytest
from app.calculation import Calculation, CalculationHistory, CalculationFactory
from app.operation import add, subtract, multiply, divide


class TestCalculation:
    """Test cases for the Calculation class."""
    
    def test_calculation_initialization(self):
        """Test that Calculation initializes correctly."""
        calc = Calculation('add', 5, 3, add)
        assert calc.operation_name == 'add'
        assert calc.operand_a == 5
        assert calc.operand_b == 3
        assert calc.operation_func == add
        assert calc.get_result() is None
    
    def test_calculation_execute_add(self):
        """Test executing an addition calculation."""
        calc = Calculation('add', 5, 3, add)
        result = calc.execute()
        assert result == 8
        assert calc.get_result() == 8
    
    def test_calculation_execute_subtract(self):
        """Test executing a subtraction calculation."""
        calc = Calculation('subtract', 10, 4, subtract)
        result = calc.execute()
        assert result == 6
    
    def test_calculation_execute_multiply(self):
        """Test executing a multiplication calculation."""
        calc = Calculation('multiply', 3, 7, multiply)
        result = calc.execute()
        assert result == 21
    
    def test_calculation_execute_divide(self):
        """Test executing a division calculation."""
        calc = Calculation('divide', 20, 4, divide)
        result = calc.execute()
        assert result == 5
    
    def test_calculation_divide_by_zero(self):
        """Test that division by zero raises error."""
        calc = Calculation('divide', 10, 0, divide)
        with pytest.raises(ValueError, match="Calculation failed"):
            calc.execute()
    
    def test_calculation_str_without_execution(self):
        """Test string representation before execution."""
        calc = Calculation('add', 5, 3, add)
        assert str(calc) == "5 + 3"
    
    def test_calculation_str_after_execution(self):
        """Test string representation after execution."""
        calc = Calculation('add', 5, 3, add)
        calc.execute()
        assert str(calc) == "5 + 3 = 8"
    
    def test_calculation_repr(self):
        """Test developer representation."""
        calc = Calculation('multiply', 4, 5, multiply)
        assert repr(calc) == "Calculation(multiply, 4, 5)"
    
    @pytest.mark.parametrize("operation, a, b, expected", [
        ('add', 5, 3, 8),
        ('subtract', 10, 3, 7),
        ('multiply', 4, 5, 20),
        ('divide', 20, 4, 5),
    ])
    def test_calculation_execute_parameterized(self, operation, a, b, expected):
        """Test calculation execution with various operations."""
        operations_map = {
            'add': add,
            'subtract': subtract,
            'multiply': multiply,
            'divide': divide
        }
        calc = Calculation(operation, a, b, operations_map[operation])
        result = calc.execute()
        assert result == expected


class TestCalculationHistory:
    """Test cases for CalculationHistory class."""
    
    def setup_method(self):
        """Clear history before each test."""
        history = CalculationHistory()
        history.clear_history()
    
    def test_history_singleton(self):
        """Test that CalculationHistory is a singleton."""
        history1 = CalculationHistory()
        history2 = CalculationHistory()
        assert history1 is history2
    
    def test_history_starts_empty(self):
        """Test that history starts empty."""
        history = CalculationHistory()
        assert len(history) == 0
        assert history.get_history() == []
    
    def test_add_calculation_to_history(self):
        """Test adding a calculation to history."""
        history = CalculationHistory()
        calc = Calculation('add', 5, 3, add)
        calc.execute()
        
        history.add_calculation(calc)
        assert len(history) == 1
        assert history.get_history()[0] == calc
    
    def test_add_multiple_calculations(self):
        """Test adding multiple calculations."""
        history = CalculationHistory()
        
        calc1 = Calculation('add', 5, 3, add)
        calc1.execute()
        calc2 = Calculation('subtract', 10, 4, subtract)
        calc2.execute()
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        assert len(history) == 2
        assert history.get_history()[0] == calc1
        assert history.get_history()[1] == calc2
    
    def test_get_last_calculation(self):
        """Test getting the last calculation."""
        history = CalculationHistory()
        
        calc1 = Calculation('add', 5, 3, add)
        calc1.execute()
        calc2 = Calculation('multiply', 4, 5, multiply)
        calc2.execute()
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        last_calc = history.get_last_calculation()
        assert last_calc == calc2
    
    def test_get_last_calculation_empty_history(self):
        """Test getting last calculation from empty history raises error."""
        history = CalculationHistory()
        with pytest.raises(IndexError, match="No calculations in history"):
            history.get_last_calculation()
    
    def test_clear_history(self):
        """Test clearing history."""
        history = CalculationHistory()
        
        calc = Calculation('add', 5, 3, add)
        calc.execute()
        history.add_calculation(calc)
        
        assert len(history) == 1
        history.clear_history()
        assert len(history) == 0
    
    def test_history_str_empty(self):
        """Test string representation of empty history."""
        history = CalculationHistory()
        assert str(history) == "No calculations in history"
    
    def test_history_str_with_calculations(self):
        """Test string representation with calculations."""
        history = CalculationHistory()
        
        calc1 = Calculation('add', 5, 3, add)
        calc1.execute()
        calc2 = Calculation('multiply', 4, 5, multiply)
        calc2.execute()
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        result = str(history)
        assert "Calculation History:" in result
        assert "1. 5 + 3 = 8" in result
        assert "2. 4 × 5 = 20" in result


class TestCalculationFactory:
    """Test cases for CalculationFactory class."""
    
    def test_factory_create_add(self):
        """Test factory creates addition calculation."""
        calc = CalculationFactory.create('add', 5, 3)
        assert calc.operation_name == 'add'
        assert calc.operand_a == 5
        assert calc.operand_b == 3
        result = calc.execute()
        assert result == 8
    
    def test_factory_create_subtract(self):
        """Test factory creates subtraction calculation."""
        calc = CalculationFactory.create('subtract', 10, 4)
        result = calc.execute()
        assert result == 6
    
    def test_factory_create_multiply(self):
        """Test factory creates multiplication calculation."""
        calc = CalculationFactory.create('multiply', 3, 7)
        result = calc.execute()
        assert result == 21
    
    def test_factory_create_divide(self):
        """Test factory creates division calculation."""
        calc = CalculationFactory.create('divide', 20, 4)
        result = calc.execute()
        assert result == 5
    
    def test_factory_unknown_operation(self):
        """Test factory raises error for unknown operation."""
        with pytest.raises(ValueError, match="Unknown operation: power"):
            CalculationFactory.create('power', 2, 3)
    
    def test_factory_get_available_operations(self):
        """Test getting available operations."""
        operations = CalculationFactory.get_available_operations()
        assert 'add' in operations
        assert 'subtract' in operations
        assert 'multiply' in operations
        assert 'divide' in operations
        assert len(operations) == 4
    
    @pytest.mark.parametrize("operation, a, b, expected", [
        ('add', 5, 3, 8),
        ('subtract', 10, 3, 7),
        ('multiply', 4, 5, 20),
        ('divide', 20, 4, 5),
        ('add', -5, -3, -8),
        ('divide', 7, 2, 3.5),
    ])
    def test_factory_create_parameterized(self, operation, a, b, expected):
        """Test factory with various operations and inputs."""
        calc = CalculationFactory.create(operation, a, b)
        result = calc.execute()
        assert result == pytest.approx(expected)
    
    def test_factory_register_operation(self):
        """Test registering a new operation."""
        def power(a: float, b: float) -> float:
            return a ** b
        
        # Register new operation
        CalculationFactory.register_operation('power', power)
        
        # Create calculation with new operation
        calc = CalculationFactory.create('power', 2, 3)
        result = calc.execute()
        assert result == 8
        
        # Clean up - remove the operation
        del CalculationFactory._operations['power']