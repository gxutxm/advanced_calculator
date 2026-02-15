# Advanced Calculator

A command-line calculator built with Python demonstrating OOP principles, design patterns, and 100% test coverage.

## Features

- Four basic operations: add, subtract, multiply, divide
- Calculation history tracking
- Interactive REPL interface
- Special commands (help, history, clear, exit)
- Comprehensive error handling
- 100% test coverage with pytest
- Factory and Singleton design patterns
- GitHub Actions CI/CD pipeline

## Quick Start

```bash
# Clone and setup
git clone https://github.com/YOUR-USERNAME/calculator-advanced.git
cd calculator-advanced
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run calculator
python -m app.calculator

# Run tests
pytest --cov=app
```

## Usage Example

```
Enter operation or command: add
Enter first number: 5
Enter second number: 3
Result: 5.0 + 3.0 = 8.0

Enter operation or command: history
Calculation History (1 calculations):
1. 5.0 + 3.0 = 8.0

Enter operation or command: exit
Thank you for using the calculator. Goodbye!
```

## Project Structure

```
calculator-advanced/
├── app/
│   ├── calculator/      # REPL interface
│   ├── calculation/     # Calculation classes (Factory, History, Calculation)
│   └── operation/       # Arithmetic operations
├── tests/               # Comprehensive test suite
├── .gitignore
├── README.md
└── requirements.txt
```

## Design Patterns

**Factory Pattern** - `CalculationFactory` creates calculation instances
```python
calc = CalculationFactory.create('add', 5, 3)
result = calc.execute()
```

**Singleton Pattern** - `CalculationHistory` maintains single history instance across application

## Error Handling

**LBYL (Look Before You Leap)** - Used in operations
```python
if b == 0:
    raise ValueError("Cannot divide by zero")
return a / b
```

**EAFP (Easier to Ask Forgiveness than Permission)** - Used in calculation execution
```python
try:
    return self.operation_func(a, b)
except (ValueError, ZeroDivisionError) as e:
    raise ValueError(f"Calculation failed: {e}")
```

## Testing

```bash
# Run all tests
pytest -v

# Check coverage (must be 100%)
pytest --cov=app --cov-report=term-missing

# Generate HTML report
pytest --cov=app --cov-report=html
```

## Requirements

- Python 3.8+
- pytest 7.4.3
- pytest-cov 4.1.0

## Author

**Gautam Govindarasan** 

