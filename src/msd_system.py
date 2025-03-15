from abc import ABCMeta, abstractmethod
import numpy as np
import sympy as sp

import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO)


class System():
    def __init__(self, m, c, k, x0=0):
        self._m = m
        self._c = c
        self._k = k
        self._x0 = x0

    def solve(self):
        """"
        Solve general solution of the system
        """
        # _lambda = sp.symbols('lambda')
        # expr = _lambda**2 - (self.c/self.m)*_lambda + (self.k/self.m)
        # solutions = sp.solve(expr, _lambda)
        # logging.debug(f"num of solutions: {len(solutions)}")
        # real_part, imag_part = solutions[0].as_real_imag()
        # logging.debug(f"solution: {real_part=}, {imag_part=}")

        gamma = self._c / (2 * self._m)
        omega = sp.sqrt(self._k/self._m)
        logging.info(f"solution: {gamma =}, {omega=}")

        discriminant = self._c**2 - 4 * self._m * self._k

        if discriminant > 0:
            # Overdamped (real and distinct roots)
            self.solusion = _OverdampedSystem(gamma, omega)
            self.solusion.solve(self._x0)
        elif discriminant == 0:
            # Critically Damped (repeated real root)
            self.solusion = _CriticallyDampedSystem(gamma, omega)
            self.solusion.solve(self._x0)
        else:
            # Underdamped (complex roots)
            self.solusion = _UnderdampedSystem(gamma, omega)
            self.solusion.solve(self._x0)

        logging.info(f"solved system: {self.name()}")

    def name(self):
        if self.solusion == None:
            return None
        return self.solusion.name()

    def displacement(self, t):
        if self.solusion == None:
            return None
        return self.solusion.displacement(t)

    def velocity(self, t):
        if self.solusion == None:
            return None
        return self.solusion.velocity(t)


class _Interface(metaclass=ABCMeta):
    """
    Abstract base class for MSD System
    """
    @abstractmethod
    def __init__(self, gamma, omega):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def solve(self, x0):
        pass

    @abstractmethod
    def displacement(self, t):
        pass

    @abstractmethod
    def velocity(self, t):
        pass


class _OverdampedSystem(_Interface):
    """
    Solution of Overdamped System
    """

    def __init__(self, gamma, omega):
        gamma = np.float64(gamma)
        omega = np.float64(omega)
        discriminant = np.sqrt(gamma**2 - omega**2)
        self._l_1 = np.float64(-gamma+discriminant)
        self._l_2 = np.float64(-gamma-discriminant)
        logging.info(f"solution: {self._l_1 =}, {self._l_2=}")

    def name(self):
        return "Overdamped System"

    def solve(self, x0):
        """
        Solve the system constants
        """
        self._C1 = (-x0 * self._l_2) / (self._l_1 - self._l_2)
        self._C2 = (-x0 * self._l_1) / (self._l_2 - self._l_1)
        logging.info(f"constants: {self._C1=}, {self._C2=}")

    def displacement(self, t):
        return self._C1 * np.exp(self._l_1*t) + self._C2 * np.exp(self._l_2*t)

    def velocity(self, t):
        return self._C1 * self._l_1 * np.exp(self._l_1*t) + self._C2 * self._l_2 * - np.exp(self._l_2*t)


class _UnderdampedSystem(_Interface):
    """
    Solution of Underdamped System
    """

    def __init__(self, gamma, omega):
        self._gamma = np.float64(gamma)
        self._omega = np.float64(omega)

    def name(self):
        return "Underdamped System"

    def solve(self, x0):
        """
        Solve the system constants
        """
        self._A = x0
        self._B = (self._gamma * x0) / self._omega
        logging.info(f"constants: {self._A =}, {self._B=}")

    def displacement(self, t):
        return np.exp(-self._gamma * t) * (self._A * np.cos(self._omega * t) + self._B * np.sin(self._omega * t))

    def velocity(self, t):
        exp_term = np.exp(-self._gamma * t)
        cos_omega_t = np.cos(self._omega * t)
        sin_omega_t = np.sin(self._omega * t)

        return -exp_term * (self._A * self._gamma * cos_omega_t + self._B * self._gamma * sin_omega_t + self._A * self._omega * sin_omega_t - self._B * self._omega * cos_omega_t)


class _CriticallyDampedSystem(_Interface):
    """
    Solution of Critically Damped System
    """

    def __init__(self, gamma, omega):
        self._gamma = np.float64(gamma)

    def name(self):
        return "Critically Damped System"

    def solve(self, x0):
        """
        Solve the system constant with following simultaneous equations
        """
        self._A = self._gamma * x0
        self._B = x0
        logging.info(f"constants: {self._A=}, {self._B=}")

    def displacement(self, t):
        return (self._A * t + self._B) * np.exp(-self._gamma * t)

    def velocity(self, t):
        return self._A * np.exp(-self._gamma * t) \
            - self._gamma * (self._B + self._A * t) * np.exp(-self._gamma * t)
