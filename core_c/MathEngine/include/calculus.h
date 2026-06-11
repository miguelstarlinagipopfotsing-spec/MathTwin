#ifndef CALCULUS_H
#define CALCULUS_H

#ifdef __cplusplus
extern "C" {
#endif

__declspec(dllexport) float evaluate_function(int func_id, float x);
__declspec(dllexport) float integrate_trapezoidal(int func_id, float a, float b, int intervals);

#ifdef __cplusplus
}
#endif

#endif 
