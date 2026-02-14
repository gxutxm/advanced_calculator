"""
Unit tests for arithmetic operations.

This module tests the basic operations with comprehensive scenarios
including edge cases and error conditions.
"""

import pytest
from app.operation import add, subtract, multiply, divide


class TestAdd:
    """Test cases for the add function."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert add(-2, -3) == -5
    
    def test_add_mixed_signs(self):
        """Test adding positive and negative numbers."""
        assert add(5, -3) == 2
        assert add(-5, 3) == -2
    
    def test_add_with_zero(self):
        """Test adding zero."""
        assert add(5, 0) == 5
        assert add(0, 5) == 5
        assert add(0, 0) == 0
    
    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert add(2.5, 3.7) == 6.2
        assert add(0.1, 0.2) == pytest.approx(0.3)


class TestSubtract:
    """Test cases for the subtract function."""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        assert subtract(5, 3) == 2
    
    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers."""
        assert subtract(-5, -3) == -2
    
    def test_subtract_mixed_signs(self):
        """Test subtracting with mixed signs."""
        assert subtract(5, -3) == 8
        assert subtract(-5, 3) == -8
    
    def test_subtract_with_zero(self):
        """Test subtracting zero."""
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5
    
    def test_subtract_same_numbers(self):
        """Test subtracting same numbers."""
        assert subtract(5, 5) == 0


class TestMultiply:
    """Test cases for the multiply function."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        assert multiply(3, 4) == 12
    
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        assert multiply(-3, -4) == 12
    
    def test_multiply_mixed_signs(self):
        """Test multiplying with mixed signs."""
        assert multiply(3, -4) == -12
        assert multiply(-3, 4) == -12
    
    def test_multiply_with_zero(self):
        """Test multiplying by zero."""
        assert multiply(5, 0) == 0
        assert multiply(0, 5) == 0
    
    def test_multiply_with_one(self):
        """Test multiplying by one."""
        assert multiply(5, 1) == 5
        assert multiply(1, 5) == 5


class TestDivide:
    """Test cases for the divide function."""
    
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        assert divide(10, 2) == 5
    
    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        assert divide(-10, -2) == 5
    
    def test_divide_mixed_signs(self):
        """Test dividing with mixed signs."""
        assert divide(10, -2) == -5
        assert divide(-10, 2) == -5
    
    def test_divide_by_one(self):
        """Test dividing by one."""
        assert divide(5, 1) == 5
    
    def test_divide_zero_numerator(self):
        """Test dividing zero."""
        assert divide(0, 5) == 0
    
    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError (LBYL)."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)
    
    def test_divide_results_in_float(self):
        """Test division resulting in float."""
        assert divide(7, 2) == 3.5
        assert divide(1, 3) == pytest.approx(0.333333, rel=1e-5)


class TestOperationsParameterized:
    """Parameterized tests for operations."""
    
    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 5),
        (-2, -3, -5),
        (0, 0, 0),
        (5, -3, 2),
        (-5, 3, -2),
        (2.5, 3.5, 6.0),
        (100, 200, 300),
        (0.1, 0.2, 0.3),
    ])
    def test_add_parameterized(self, a, b, expected):
        """Test add function with multiple parameter sets."""
        result = add(a, b)
        if isinstance(expected, float) and expected < 1:
            assert result == pytest.approx(expected)
        else:
            assert result == expected
    
    @pytest.mark.parametrize("a, b, expected", [
        (5, 3, 2),
        (3, 5, -2),
        (0, 5, -5),
        (5, 0, 5),
        (-5, -3, -2),
        (10.5, 3.2, 7.3),
    ])
    def test_subtract_parameterized(self, a, b, expected):
        """Test subtract function with multiple parameter sets."""
        assert subtract(a, b) == pytest.approx(expected)
    
    @pytest.mark.parametrize("a, b, expected", [
        (3, 4, 12),
        (-3, -4, 12),
        (3, -4, -12),
        (0, 5, 0),
        (5, 0, 0),
        (2.5, 4, 10.0),
    ])
    def test_multiply_parameterized(self, a, b, expected):
        """Test multiply function with multiple parameter sets."""
        assert multiply(a, b) == expected
    
    @pytest.mark.parametrize("a, b, expected", [
        (10, 2, 5),
        (7, 2, 3.5),
        (-10, 2, -5),
        (10, -2, -5),
        (0, 5, 0),
        (1, 3, 0.333333),
    ])
    def test_divide_parameterized(self, a, b, expected):
        """Test divide function with multiple parameter sets."""
        assert divide(a, b) == pytest.approx(expected, rel=1e-5)
    
    @pytest.mark.parametrize("a, b", [
        (10, 0),
        (-10, 0),
        (0, 0),
        (0.5, 0),
    ])
    def test_divide_by_zero_parameterized(self, a, b):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(a, b)