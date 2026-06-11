import ctypes
import os
import numpy as np

# Load the DLL
dll_name = 'libMathEngine.dll'
dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'build', dll_name))
math_engine = ctypes.CDLL(dll_path)

# --- Define C Function Signatures in Python ---

# matrix_multiply(float* A, float* B, float* C, int rowsA, int colsA, int colsB)
math_engine.matrix_multiply.argtypes = [
    ctypes.POINTER(ctypes.c_float), 
    ctypes.POINTER(ctypes.c_float), 
    ctypes.POINTER(ctypes.c_float), 
    ctypes.c_int, ctypes.c_int, ctypes.c_int
]
math_engine.matrix_multiply.restype = None

# integrate_trapezoidal(int func_id, float a, float b, int intervals)
math_engine.integrate_trapezoidal.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_int]
math_engine.integrate_trapezoidal.restype = ctypes.c_float

# evaluate_function(int func_id, float x)
math_engine.evaluate_function.argtypes = [ctypes.c_int, ctypes.c_float]
math_engine.evaluate_function.restype = ctypes.c_float


# --- Test Functions ---

def test_matrix():
    print("\n--- Testing Matrix Multiplication ---")
    # Define a 2x3 Matrix A and a 3x2 Matrix B using NumPy (floats)
    A = np.array([[1.0, 2.0, 3.0], 
                  [4.0, 5.0, 6.0]], dtype=np.float32)
    
    B = np.array([[7.0, 8.0], 
                  [9.0, 1.0], 
                  [2.0, 3.0]], dtype=np.float32)
    
    # Placeholder for the 2x2 output Matrix C
    C = np.zeros((2, 2), dtype=np.float32)
    
    # Convert NumPy arrays to raw C pointers and call the C engine
    math_engine.matrix_multiply(
        A.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        B.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        C.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        2, 3, 2
    )
    print("Result Matrix C from C Engine:\n", C)

def test_calculus():
    print("\n--- Testing Numerical Integration ---")
    # Function ID 2 is exp(x). Let's integrate e^x from 0 to 1
    # Analytical answer is e^1 - e^0 approx 1.71828
    result = math_engine.integrate_trapezoidal(2, 0.0, 1.0, 1000)
    print(f"Integral of e^x from 0 to 1: {result:.5f}")

if __name__ == "__main__":
    test_matrix()
    test_calculus()