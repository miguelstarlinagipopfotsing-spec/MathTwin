#include "../include/calculus.h"
#include <math.h>
#include <stdio.h> // Needed for printf

__declspec(dllexport) float evaluate_function(int func_id, float x) {
    switch(func_id) {
        case 1: return log(x);       // Ln(x)
        case 2: return exp(x);       // e^x
        case 3: return sin(x);       // Sin(x)
        case 4: return cos(x);       // Cos(x)
        case 5: return sqrt(x);      // Sqrt(x)
        case 6: return tan(x);       // Tan(x)
        default: return 0.0f;
    }
}

__declspec(dllexport) float integrate_trapezoidal(int func_id, float a, float b, int intervals) {
    // This print will tell us if the parameters are corrupted
    printf("[C Engine] integrate_trapezoidal called! func_id=%d, a=%.2f, b=%.2f, intervals=%d\n", func_id, a, b, intervals);
    
    float h = (b - a) / intervals;
    float sum = 0.5f * (evaluate_function(func_id, a) + evaluate_function(func_id, b));
    
    for (int i = 1; i < intervals; i++) {
        float x = a + i * h;
        sum += evaluate_function(func_id, x);
    }
    
    return sum * h;
}