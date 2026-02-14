"""
Unit tests for CalculatorREPL.

This module tests the REPL interface including user interaction,
special commands, and history management.
"""

import pytest
from unittest.mock import patch
from app.calculator import CalculatorREPL
from app.calculation import CalculationHistory


class TestCalculatorREPL:
    """Test cases for CalculatorREPL class."""
    
    def setup_method(self):
        """Clear history before each test."""
        history = CalculationHistory()
        history.clear_history()
    
    @pytest.fixture
    def repl(self):
        """Fixture to provide a fresh CalculatorREPL instance."""
        return CalculatorREPL()
    
    def test_repl_initialization(self, repl):
        """Test that REPL initializes correctly."""
        assert hasattr(repl, 'history')
        assert repl.running is False
    
    def test_display_welcome(self, repl, capsys):
        """Test welcome message display."""
        repl.display_welcome()
        captured = capsys.readouterr()
        assert "Advanced Calculator" in captured.out
        assert "Available operations:" in captured.out
    
    def test_display_help(self, repl, capsys):
        """Test help message display."""
        repl.display_help()
        captured = capsys.readouterr()
        assert "HELP" in captured.out
        assert "Special Commands:" in captured.out
    
    def test_display_history_empty(self, repl, capsys):
        """Test displaying empty history."""
        repl.display_history()
        captured = capsys.readouterr()
        assert "No calculations in history" in captured.out
    
    def test_display_history_with_calculations(self, repl, capsys):
        """Test displaying history with calculations."""
        # Perform a calculation to add to history
        with patch('builtins.input', side_effect=['5', '3']):
            repl.perform_calculation('add')
        
        repl.display_history()
        captured = capsys.readouterr()
        assert "Calculation History" in captured.out
        assert "5 + 3 = 8" in captured.out or "5.0 + 3.0 = 8.0" in captured.out
    
    def test_clear_history(self, repl, capsys):
        """Test clearing history."""
        # Add a calculation
        with patch('builtins.input', side_effect=['5', '3']):
            repl.perform_calculation('add')
        
        assert len(repl.history) == 1
        repl.clear_history()
        assert len(repl.history) == 0
        
        captured = capsys.readouterr()
        assert "cleared" in captured.out.lower()
    
    @patch('builtins.input', side_effect=['add'])
    def test_get_operation_valid(self, mock_input, repl):
        """Test getting a valid operation."""
        operation = repl.get_operation()
        assert operation == 'add'
    
    @patch('builtins.input', side_effect=['exit'])
    def test_get_operation_exit(self, mock_input, repl):
        """Test exit command."""
        operation = repl.get_operation()
        assert operation == 'exit'
    
    @patch('builtins.input', side_effect=['quit'])
    def test_get_operation_quit(self, mock_input, repl):
        """Test quit command."""
        operation = repl.get_operation()
        assert operation == 'exit'
    
    @patch('builtins.input', side_effect=['help'])
    def test_get_operation_help(self, mock_input, repl):
        """Test help command."""
        operation = repl.get_operation()
        assert operation == 'help'
    
    @patch('builtins.input', side_effect=['history'])
    def test_get_operation_history(self, mock_input, repl):
        """Test history command."""
        operation = repl.get_operation()
        assert operation == 'history'
    
    @patch('builtins.input', side_effect=['invalid', 'add'])
    def test_get_operation_invalid_then_valid(self, mock_input, repl, capsys):
        """Test handling invalid operation then valid."""
        operation = repl.get_operation()
        assert operation == 'add'
        captured = capsys.readouterr()
        assert "Invalid input" in captured.out
    
    @patch('builtins.input', side_effect=['5.5'])
    def test_get_number_valid(self, mock_input, repl):
        """Test getting a valid number."""
        number = repl.get_number("Enter number: ")
        assert number == 5.5
    
    @patch('builtins.input', side_effect=['abc', '10'])
    def test_get_number_invalid_then_valid(self, mock_input, repl, capsys):
        """Test handling invalid number then valid."""
        number = repl.get_number("Enter number: ")
        assert number == 10.0
        captured = capsys.readouterr()
        assert "Invalid number" in captured.out
    
    @patch('builtins.input', side_effect=['5', '3'])
    def test_perform_calculation_add(self, mock_input, repl, capsys):
        """Test performing addition calculation."""
        repl.perform_calculation('add')
        captured = capsys.readouterr()
        assert "Result:" in captured.out
        assert "8" in captured.out
        assert len(repl.history) == 1
    
    @patch('builtins.input', side_effect=['10', '0'])
    def test_perform_calculation_division_by_zero(self, mock_input, repl, capsys):
        """Test handling division by zero."""
        repl.perform_calculation('divide')
        captured = capsys.readouterr()
        assert "Error:" in captured.out
    
    @patch('builtins.input', side_effect=['add', '5', '3', 'exit'])
    def test_run_single_calculation(self, mock_input, repl, capsys):
        """Test running REPL with one calculation."""
        repl.run()
        captured = capsys.readouterr()
        assert "Advanced Calculator" in captured.out
        assert "Result:" in captured.out
        assert "Goodbye" in captured.out
    
    @patch('builtins.input', side_effect=['exit'])
    def test_run_immediate_exit(self, mock_input, repl, capsys):
        """Test exiting immediately."""
        repl.run()
        captured = capsys.readouterr()
        assert "Advanced Calculator" in captured.out
        assert "Goodbye" in captured.out
    
    @patch('builtins.input', side_effect=['help', 'exit'])
    def test_run_help_command(self, mock_input, repl, capsys):
        """Test help command in REPL."""
        repl.run()
        captured = capsys.readouterr()
        assert "HELP" in captured.out
    
    @patch('builtins.input', side_effect=['add', '5', '3', 'history', 'exit'])
    def test_run_history_command(self, mock_input, repl, capsys):
        """Test history command in REPL."""
        repl.run()
        captured = capsys.readouterr()
        assert "Calculation History" in captured.out
    
    @patch('builtins.input', side_effect=['add', '5', '3', 'clear', 'exit'])
    def test_run_clear_command(self, mock_input, repl, capsys):
        """Test clear command in REPL."""
        repl.run()
        captured = capsys.readouterr()
        assert "cleared" in captured.out.lower()
    
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_run_keyboard_interrupt(self, mock_input, repl, capsys):
        """Test handling Ctrl+C."""
        repl.run()
        captured = capsys.readouterr()
        assert "interrupted" in captured.out.lower() or "Goodbye" in captured.out
