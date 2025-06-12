"""Distance calculation utilities."""

from __future__ import annotations

import math
from typing import Optional

from .conversion import (Point2D, Point3D, PointPolar, PointSpherical,
                         spherical_to_cart)


def distance_cartesian_2d(p1: Point2D, p2: Point2D) -> float:
    """Euclidean distance in 2-D Cartesian system."""
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.hypot(dx, dy)


def distance_cartesian_3d(p1: Point3D, p2: Point3D) -> float:
    """Euclidean distance in 3-D Cartesian system."""
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dz = p2.z - p1.z
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def distance_polar(p1: PointPolar, p2: PointPolar) -> float:
    """Distance between two points given in polar coordinates."""
    return math.sqrt(
        p1.r**2 + p2.r**2 - 2 * p1.r * p2.r * math.cos(p1.theta - p2.theta)
    )


def distance_spherical_direct(p1: PointSpherical, p2: PointSpherical) -> float:
    """Straight-line distance between points in spherical coordinates."""
    c1 = Point3D(*spherical_to_cart(p1.r, p1.theta, p1.phi))
    c2 = Point3D(*spherical_to_cart(p2.r, p2.theta, p2.phi))
    return distance_cartesian_3d(c1, c2)


def distance_spherical_surface(
    p1: PointSpherical, p2: PointSpherical, radius: Optional[float] = None
) -> float:
    """Great-circle distance between two spherical points.

    Args:
        p1: First point.
        p2: Second point.
        radius: Sphere radius. If ``None``, uses mean radius of ``p1`` and ``p2``.

    Returns:
        Distance along the sphere's surface.
    """
    r = radius if radius is not None else (p1.r + p2.r) / 2
    angle = math.acos(
        math.sin(p1.phi) * math.sin(p2.phi)
        + math.cos(p1.phi) * math.cos(p2.phi) * math.cos(p1.theta - p2.theta)
    )
    return r * angle
