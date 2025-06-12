import math
import random

import pytest

from Lb_3.coords.conversion import (Point2D, Point3D, PointPolar,
                                    PointSpherical, polar_to_cart,
                                    spherical_to_cart)
from Lb_3.coords.distance import (distance_cartesian_2d, distance_cartesian_3d,
                                  distance_polar, distance_spherical_direct,
                                  distance_spherical_surface)


@pytest.mark.parametrize("_", range(1000))
def test_distance_polar(_):
    p1 = PointPolar(random.uniform(0, 100), random.uniform(-math.pi, math.pi))
    p2 = PointPolar(random.uniform(0, 100), random.uniform(-math.pi, math.pi))
    d_polar = distance_polar(p1, p2)
    c1 = Point2D(*polar_to_cart(p1.r, p1.theta))
    c2 = Point2D(*polar_to_cart(p2.r, p2.theta))
    d_cart = distance_cartesian_2d(c1, c2)
    assert math.isclose(d_polar, d_cart, rel_tol=1e-6)


@pytest.mark.parametrize("_", range(1000))
def test_distance_spherical_direct(_):
    p1 = PointSpherical(
        random.uniform(0, 100),
        random.uniform(-math.pi, math.pi),
        random.uniform(-math.pi / 2, math.pi / 2),
    )
    p2 = PointSpherical(
        random.uniform(0, 100),
        random.uniform(-math.pi, math.pi),
        random.uniform(-math.pi / 2, math.pi / 2),
    )
    d_sph = distance_spherical_direct(p1, p2)
    c1 = Point3D(*spherical_to_cart(p1.r, p1.theta, p1.phi))
    c2 = Point3D(*spherical_to_cart(p2.r, p2.theta, p2.phi))
    d_cart = distance_cartesian_3d(c1, c2)
    assert math.isclose(d_sph, d_cart, rel_tol=1e-6)


@pytest.mark.parametrize("_", range(1000))
def test_distance_spherical_surface(_):
    p1 = PointSpherical(
        random.uniform(1, 100),
        random.uniform(-math.pi, math.pi),
        random.uniform(-math.pi / 2, math.pi / 2),
    )
    p2 = PointSpherical(
        random.uniform(1, 100),
        random.uniform(-math.pi, math.pi),
        random.uniform(-math.pi / 2, math.pi / 2),
    )
    r = (p1.r + p2.r) / 2
    d_surface = distance_spherical_surface(p1, p2, radius=r)
    c1 = Point3D(*spherical_to_cart(r, p1.theta, p1.phi))
    c2 = Point3D(*spherical_to_cart(r, p2.theta, p2.phi))
    chord = distance_cartesian_3d(c1, c2)
    angle = 2 * math.asin(chord / (2 * r))
    expected = r * angle
    assert math.isclose(d_surface, expected, rel_tol=1e-6)
