#ifndef MATRIX_H_INCLUDED
#define MATRIX_H_INCLUDED


// Macros to easily access a 2D stored as a flat 1D array
#define MAT_INDEX(r, c, num_cols) ((r) * (num_cols) + (c))

#ifdef __cplusplus
extern "C" {
#endif // MATRIX_H_INCLUDED
// __declspec(dllexport) makes sure Python can see these functions
__declspec(dllexport) void matrix_add(float* A, float* B, float* C, int rowsA, int colsA, int colsB);

#ifdef __cplusplus
}
#endif // __cplusplus

#endif 