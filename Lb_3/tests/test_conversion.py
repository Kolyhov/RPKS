import math
import random

import pytest

from Lb_3.coords.conversion import (cart_to_polar, cart_to_spherical,
                                    polar_to_cart, spherical_to_cart)


@pytest.mark.parametrize("_", range(100))
def test_polar_roundtrip(_):
    r = random.uniform(0, 100)
    theta = random.uniform(-math.pi, math.pi)
    x, y = polar_to_cart(r, theta)
    r2, theta2 = cart_to_polar(x, y)
    assert math.isclose(r, r2, rel_tol=1e-6)
    assert math.isclose(theta, theta2, rel_tol=1e-6)


@pytest.mark.parametrize("_", range(100))
def test_spherical_roundtrip(_):
    r = random.uniform(0, 100)
    theta = random.uniform(-math.pi, math.pi)
    phi = random.uniform(-math.pi / 2, math.pi / 2)
    x, y, z = spherical_to_cart(r, theta, phi)
    r2, theta2, phi2 = cart_to_spherical(x, y, z)
    assert math.isclose(r, r2, rel_tol=1e-6)
    assert math.isclose(theta, theta2, rel_tol=1e-6)
    assert math.isclose(phi, phi2, rel_tol=1e-6)
