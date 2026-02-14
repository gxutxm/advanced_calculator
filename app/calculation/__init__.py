"""
Calculation module.

This module implements the Calculation class, CalculationHistory, and CalculationFactory.
Demonstrates the Factory design pattern, Singleton pattern, and history management.
"""

from typing import Callable, List, Optional
from app.operation import add, subtract, multiply, divide


class Calculation:
    def __init__(self, operation_name: str, operand_a: float, operand_b: float, 
                 operation_func: Callable[[float, float], float]):
        self.operation_name = operation_name
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.operation_func = operation_func
        self._result: Optional[float] = None
    
    def execute(self) -> float:
        # EAFP approach - Easier to Ask Forgiveness than Permission
        try:
            self._result = self.operation_func(self.operand_a, self.operand_b)
            return self._result
        except (ValueError, ZeroDivisionError) as e:
            raise ValueError(f"Calculation failed: {e}")
    
    def get_result(self) -> Optional[float]:
        return self._result
    
    def __str__(self) -> str:
        symbols = {
            'add': '+',
            'subtract': '-',
            'multiply': '×',
            'divide': '÷'
        }
        symbol = symbols.get(self.operation_name, self.operation_name)
        
        if self._result is not None:
            return f"{self.operand_a} {symbol} {self.operand_b} = {self._result}"
        return f"{self.operand_a} {symbol} {self.operand_b}"
    
    def __repr__(self) -> str:
        return f"Calculation({self.operation_name}, {self.operand_a}, {self.operand_b})"


class CalculationHistory:
    
    _instance: Optional['CalculationHistory'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.history: List[Calculation] = [] # type: ignore
        return cls._instance
    
    def add_calculation(self, calculation: Calculation) -> None:
        self.history.append(calculation)
    
    def get_history(self) -> List[Calculation]:
        return self.history.copy()
    
    def clear_history(self) -> None:
        self.history.clear()
    
    def get_last_calculation(self) -> Calculation:
        if not self.history:
            raise IndexError("No calculations in history")
        return self.history[-1]
    
    def __len__(self) -> int:
        return len(self.history)
    
    def __str__(self) -> str:
        if not self.history:
            return "No calculations in history"
        
        lines = ["Calculation History:"]
        for i, calc in enumerate(self.history, 1):
            lines.append(f"{i}. {calc}")
        return "\n".join(lines)


class CalculationFactory:    
    _operations = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
    }
    
    @classmethod
    def create(cls, operation_name: str, a: float, b: float) -> Calculation:
        if operation_name not in cls._operations:
            raise ValueError(
                f"Unknown operation: {operation_name}. "
                f"Available: {', '.join(cls._operations.keys())}"
            )
        
        operation_func = cls._operations[operation_name]
        return Calculation(operation_name, a, b, operation_func)
    
    @classmethod
    def get_available_operations(cls) -> List[str]:
        
        return list(cls._operations.keys())
    
    @classmethod
    def register_operation(cls, name: str, func: Callable[[float, float], float]) -> None:
        
        cls._operations[name] = func