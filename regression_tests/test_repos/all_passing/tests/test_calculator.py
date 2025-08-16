import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    
def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5
    
def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    
def test_divide():
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
