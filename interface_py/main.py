import sys
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from sympy.calculus.util import continuous_domain
from PyQt6.QtWidgets import QApplication
from gui import MainWindow

# Symbole global SymPy
x = sp.Symbol('x')

def analyze_function(user_input, max_x):
    """Effectue toute l'analyse mathématique et retourne un dictionnaire de données."""
    if not user_input.strip():
        return None

    try:
        # Transformation syntaxique intelligente
        transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
        local_dict = {'e': sp.E, 'E': sp.E, 'pi': sp.pi, 'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'ln': sp.log, 'log': sp.log, 'sqrt': sp.sqrt}
        
        expr = parse_expr(user_input, local_dict=local_dict, transformations=transformations)

        # Analyse de la parité
        try:
            expr_neg_x = expr.subs(x, -x)
            if sp.simplify(expr_neg_x - expr) == 0:
                parity_txt = r"\text{Even (Symmetrical / y-axis)}"
            elif sp.simplify(expr_neg_x + expr) == 0:
                parity_txt = r"\text{Odd (Symmetrical / origin)}"
            else:
                parity_txt = r"\text{Neither Even nor Odd}"
        except:
            parity_txt = r"\text{Complex parity analysis}"

        # Prolongement par continuité
        extension_txt = r"\text{No singularities detected.}"
        try:
            denom = sp.denom(sp.cancel(expr))
            print("Expression :", expr)
            print("Denom :", denom)
            print("Roots :", roots)
            if denom != 1:
                singularities = sp.solve(denom, x)
                ext_points = []
                for sing in singularities:
                    if sing.is_Real:
                        try:
                            lim_values = sp.limit(expr, x, sing)
                            if lim_values.is_Real:
                                ext_points.append(f"x = {sp.latex(sing)} \\Rightarrow y = {sp.latex(lim_values)}")
                        except:
                            continue
                if ext_points:
                    extension_txt = r"\text{Singularities with potential extension: } " + r", ".join(ext_points)
                else:
                    extension_txt = r"\text{Asymptotic discontinuities (Non-removable)}"
        except:
            pass

        # Calcul des asymptotes
        asymptotes_list = []
        v_asymptotes_nums = []
        h_asymptotes_nums = []
        oblique_asymptotes = []

        try:
            denom = sp.denom(sp.cancel(expr))
            if denom != 1:
                roots = sp.solve(denom, x)
                print("Roots =", roots)
                for r in roots:
                    print("r =", r)
                    if r.is_Real:
                        left_lim = sp.limit(expr, x, r, dir='-')
                        right_lim = sp.limit(expr, x, r, dir='+')
                        if left_lim in (sp.oo, -sp.oo) or right_lim in (sp.oo, -sp.oo):
                            asymptotes_list.append(f"x = {sp.latex(r)}")
                            v_asymptotes_nums.append(float(r))

            lim_inf_pos = sp.limit(expr, x, sp.oo)
            if lim_inf_pos.is_Real:
                asymptotes_list.append(f"y = {sp.latex(lim_inf_pos)}")
                h_asymptotes_nums.append(float(lim_inf_pos))

            for direction in [sp.oo, -sp.oo]:
                a_lim = sp.limit(expr / x, x, direction)
                if a_lim.is_Real and a_lim != 0:
                    b_lim = sp.limit(expr - a_lim * x, x, direction)
                    if b_lim.is_Real:
                        asymptotes_list.append(f"y = {sp.latex(a_lim * x + b_lim)}")
                        oblique_asymptotes.append((float(a_lim), float(b_lim)))

            lim_inf_neg = sp.limit(expr, x, -sp.oo)
            if lim_inf_neg.is_Real and lim_inf_neg != lim_inf_pos:
                asymptotes_list.append(f"y = {sp.latex(lim_inf_neg)}")
                h_asymptotes_nums.append(float(lim_inf_neg))
        except:
            pass

        asymptote_txt = r"\text{" + ", ".join(list(set(asymptotes_list))) + "}" if asymptotes_list else r"\text{No asymptotes detected.}"

        # Éléments d'Analyse Symbolique
        math_preview = sp.latex(expr)
        df = continuous_domain(expr, x, sp.S.Reals)
        domain_text = f"Df = {sp.latex(df)}"

        try:
            lim_inf_neg = sp.limit(expr, x, -sp.oo)
            lim_inf_pos = sp.limit(expr, x, sp.oo)
            limits_text = (
                f"\\lim_{{x \\to -\\infty}} f(x) = {sp.latex(lim_inf_neg)}"
                f" \\quad | \\quad "
                f"\\lim_{{x \\to +\\infty}} f(x) = {sp.latex(lim_inf_pos)}"
            )
        except Exception as e:
            print(f"Erreur lors du calcul des limites : {e}")
            limits_text = "\\text{Could not compute limits cleanly.}"

        derivative_text = sp.latex(sp.diff(expr, x))

        try:
            primitive_expr = sp.integrate(expr, x)
            primitive_text = f"{sp.latex(primitive_expr)} + C"
        except sp.IntegralError:
            primitive_text = "\\text{Primitive has no closed-form expression.}"

        # Préparation des données numériques pour le graphique
        f_numeric = sp.lambdify(x, expr, modules=["numpy"])
        min_x = -float(max_x)
        x_data = np.linspace(min_x, max_x, 1000, dtype=np.float32)

        try:
            y_data = f_numeric(x_data)
        except Exception as e:
            print(f"Erreur lors du calcul des données numériques : {e}")
            y_data = np.zeros_like(x_data)

        y_data = np.asarray(y_data, dtype=np.float32)
        if y_data.ndim == 0:
            y_data = np.full_like(x_data, y_data)

        y_data[np.isinf(y_data)] = np.nan

        # Nettoyage des sauts d'asymptotes verticales
        jump_threshold = 1000
        for i in range(1, len(y_data)):
            if not np.isnan(y_data[i]) and not np.isnan(y_data[i-1]):
                if abs(y_data[i] - y_data[i-1]) > jump_threshold:
                    y_data[i] = np.nan

        print("Verticales :", v_asymptotes_nums)
        print("Horizontales :", h_asymptotes_nums)
        print("Obliques :", oblique_asymptotes)
        print("Texte :", asymptote_txt)           

        # On renvoie un paquet de données propre à l'IHM
        return {
            "math_preview": math_preview,
            "domain_text": domain_text,
            "limits_text": limits_text,
            "derivative_text": derivative_text,
            "primitive_text": primitive_text,
            "parity_txt": parity_txt,
            "extension_txt": extension_txt,
            "asymptote_txt": asymptote_txt,
            "x_data": x_data,
            "y_data": y_data,
            "v_lines": v_asymptotes_nums,
            "h_lines": h_asymptotes_nums,
            "oblique_lines": oblique_asymptotes
        }

    except Exception as e:
        print(f"Erreur d'analyse : {e}")  # Visible dans la console pour debugger !
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(analyze_function)
    window.on_inputs_changed()
    window.show()
    sys.exit(app.exec())