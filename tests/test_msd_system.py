import pytest
from src.msd_system import System


def test_system_underdamped():
    m = 1.0
    c = 0.5
    k = 10.0
    x0 = 0.5
    system = System(m, c, k, x0)
    system.solve()

    assert system.name() == "Underdamped System"
    assert system.displacement(1.0) is not None
    assert system.velocity(1.0) is not None


def test_system_overdamped():
    m = 1.0
    c = 10.0
    k = 10.0
    x0 = 0.5
    system = System(m, c, k, x0)
    system.solve()

    assert system.name() == "Overdamped System"
    assert system.displacement(1.0) is not None
    assert system.velocity(1.0) is not None


def test_system_critically_damped():
    m = 1.0
    c = 4.0
    k = 4.0
    x0 = 0.5
    system = System(m, c, k, x0)
    system.solve()

    assert system.name() == "Critically Damped System"
    assert system.displacement(1.0) is not None
    assert system.velocity(1.0) is not None
