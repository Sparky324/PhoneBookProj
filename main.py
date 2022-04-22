import math_func

a = float(input("Укажите, чему равно ребро куба "))
print("Объем куба равен ", math_func.cube(a))

a, b = input("Укажите катеты прямоуг. треуг. через пробел ").strip().split()
print("Гипотенуза ", math_func.hipot(float(a), float(b)))




