#include "../include/matrix.h"
#include <stdio.h> // Needed for printf

__declspec(dllexport) void matrix_multiply(float* A, float* B, float* C, int rowsA, int colsA, int colsB) {
    // This print will tell us if C receives the correct dimensions
    printf("\n[C Engine] matrix_multiply called! rowsA=%d, colsA=%d, colsB=%d\n", rowsA, colsA, colsB);
    
    for (int i = 0; i < rowsA; i++) {
        for (int j = 0; j < colsB; j++) {
            float sum = 0.0f;
            for (int k = 0; k < colsA; k++) {
                sum += A[MAT_INDEX(i, k, colsA)] * B[MAT_INDEX(k, j, colsB)];
            }
            C[MAT_INDEX(i, j, colsB)] = sum;
        }
    }
}