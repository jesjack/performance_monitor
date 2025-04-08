from src.performance_monitor_jesjack import timeit, show_graph
from src.performance_monitor_jesjack.graphing import ExecutionGraphing


@timeit.show
def fibonacci(n):
    """
    Calcula el n-ésimo número de Fibonacci de manera recursiva.
    :param n: La posición en la secuencia de Fibonacci.
    :return: El n-ésimo número de Fibonacci.
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@timeit
def factorial(n):
    """
    Calcula el factorial de n de manera recursiva.
    :param n: Número entero no negativo.
    :return: n!
    """
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


@timeit
def sum_digits(n):
    """
    Suma los dígitos de un número de forma recursiva.
    :param n: Número entero no negativo.
    :return: Suma de sus dígitos.
    """
    if n < 10:
        return n
    else:
        return n % 10 + sum_digits(n // 10)


@timeit
def gcd(a, b):
    """
    Calcula el máximo común divisor (GCD) de dos números usando el algoritmo de Euclides recursivamente.
    :param a: Primer número.
    :param b: Segundo número.
    :return: El GCD de a y b.
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


@timeit
def power(base, exp):
    """
    Calcula base elevado a exp de manera recursiva.
    :param base: Número base.
    :param exp: Exponente no negativo.
    :return: base ** exp
    """
    if exp == 0:
        return 1
    else:
        return base * power(base, exp - 1)


@timeit
def reverse_string(s):
    """
    Invierte una cadena de texto de manera recursiva.
    :param s: Cadena a invertir.
    :return: Cadena invertida.
    """
    if len(s) <= 1:
        return s
    else:
        return reverse_string(s[1:]) + s[0]


if __name__ == "__main__":
    show_graph.on_exit()
    # Ejemplos de uso
    print(f"Fibonacci(10) = {fibonacci(10)}")
    print(f"Factorial(5) = {factorial(5)}")
    print(f"Suma de dígitos de 12345 = {sum_digits(12345)}")
    print(f"GCD(48, 18) = {gcd(48, 18)}")
    print(f"2^10 = {power(2, 10)}")
    print(f"Reverse of 'recursion' = {reverse_string('recursion')}")

    # Mostrar gráficas de tiempos
    # ExecutionGraphing.plot_graph()
