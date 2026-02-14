"""
Calculator REPL interface.

This module provides an interactive Read-Eval-Print Loop for the calculator,
including history management and special commands.
"""

from app.calculation import CalculationFactory, CalculationHistory


class CalculatorREPL:
    
    def __init__(self):
        self.history = CalculationHistory()
        self.running = False
    
    def display_welcome(self) -> None:
        print("Advanced Calculator")
        print("\nAvailable operations:")
        for op in CalculationFactory.get_available_operations():
            print(f"  • {op}")
        print("\nSpecial commands:")
        print("  • help    - Show this help message")
        print("  • history - View calculation history")
        print("  • clear   - Clear calculation history")
        print("  • exit    - Exit the calculator")
    
    def display_help(self) -> None:
        print("HELP - Calculator Usage")
        print("\nTo perform a calculation:")
        print("  1. Enter operation name (add, subtract, multiply, divide)")
        print("  2. Enter first number")
        print("  3. Enter second number")
        print("\nSpecial Commands:")
        print("  help    - Display this help message")
        print("  history - Show all calculations from this session")
        print("  clear   - Clear the calculation history")
        print("  exit    - Exit the calculator (also: quit, q)")
    
    def display_history(self) -> None:
        if len(self.history) == 0:
            print("No calculations in history yet.")
        else:
            print(f"Calculation History ({len(self.history)} calculations):")
            for i, calc in enumerate(self.history.get_history(), 1):
                print(f"{i}. {calc}")
    
    def clear_history(self) -> None:
        self.history.clear_history()
        print("\n History cleared.\n")
    
    def get_operation(self) -> str:
        while True:
            user_input = input("Enter operation or command: ").strip().lower()
            
            # Check for exit commands
            if user_input in ['exit', 'quit', 'q']:
                return 'exit'
            
            # Check for special commands
            if user_input in ['help', 'history', 'clear']:
                return user_input
            
            # Check for valid operations
            if user_input in CalculationFactory.get_available_operations():
                return user_input
            
            print(f"Invalid input '{user_input}'. Type 'help' for instructions.\n")
    
    def get_number(self, prompt: str) -> float:
        
        while True:
            # EAFP approach - Try to convert, handle exception if it fails
            try:
                value = input(prompt).strip()
                return float(value)
            except ValueError:
                print(f"Invalid number '{value}'. Please enter a valid number.\n")
    
    def perform_calculation(self, operation: str) -> None:
        try:
            a = self.get_number("Enter first number: ")
            b = self.get_number("Enter second number: ")
            
            # Create calculation using factory
            calculation = CalculationFactory.create(operation, a, b)
            
            # Execute calculation
            result = calculation.execute()
            
            # Add to history
            self.history.add_calculation(calculation)
            
            # Display result
            print(f"\n Result: {calculation}\n")
            
        except ValueError as e:
            # Handle calculation errors (e.g., division by zero)
            print(f"\nError: {e}\n")
        except Exception as e:  # pragma: no cover
            # Catch any unexpected errors
            print(f"\nUnexpected error: {e}\n")
    
    def run(self) -> None:
        self.running = True
        self.display_welcome()
        
        try:
            while self.running:
                # Get operation or command from user
                choice = self.get_operation()
                
                # Handle special commands
                if choice == 'exit':
                    self.running = False
                    print("\nThank you for using the calculator. Goodbye!\n")
                    break
                elif choice == 'help':
                    self.display_help()
                    continue
                elif choice == 'history':
                    self.display_history()
                    continue
                elif choice == 'clear':
                    self.clear_history()
                    continue
                
                # Perform calculation
                self.perform_calculation(choice)
                
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\nCalculator interrupted. Goodbye!\n")
        except Exception as e:  # pragma: no cover
            # Catch any other unexpected errors
            print(f"\nFatal error: {e}\n")


def main():  # pragma: no cover
    """Entry point for the calculator application."""
    repl = CalculatorREPL()
    repl.run()


if __name__ == "__main__":  # pragma: no cover
    main()