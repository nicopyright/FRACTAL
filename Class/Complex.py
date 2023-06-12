# Complex class file.
# we need to use complexes for the Julia set of fractals
from math import cos, sin, cosh, sinh, exp


class Complex:
    def __init__(self,
                 r: float = 0.0,
                 i: float = 0.0) -> None:
        """
        :param r: reel part of the complex
        :param i: imaginary part of the complex
        """
        self.re = r
        self.im = i

    def __repr__(self) -> str:
        """
        :return: "Re(z) + i*Im(z)"
        """
        return "{} +i{}".format(self.re, self.im)

    def __add__(self, other) -> "Complex":
        """
        :return: addition of two complexes result
        """
        return Complex(self.re + other.re, self.im + other.im)

    def __sub__(self, other) -> "Complex":
        """
        :return: subtraction of two complexes result
        """
        return Complex(self.re - other.re, self.im - other.im)

    def __mul__(self, other) -> "Complex":
        """
        :return: multiplication of two complexes result
        """
        return Complex(self.re * other.re - self.im * other.im, self.re * other.im + other.re * self.im)

    def __abs__(self) -> float:
        """
        :return: Modulus of the complex z
        """
        return (self.re ** 2 + self.im ** 2) ** (1 / 2)

    def coord(self) -> tuple:
        """
        :return: Coordinates with a Tuple
        """
        return self.re, self.im

    def cos(self):
        return Complex(cos(self.re)*cosh(self.im), -sin(self.re)*sinh(self.im))

    def exp(self):
        return Complex(exp(self.re)*cos(self.im), exp(self.re)*sin(self.im))
