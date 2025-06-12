"""Coordinate conversion utilities."""

from __future__ import annotations

import math
from dataclasses import dataclass


def _normalize_angle(angle: float) -> float:
    """Normalize angle to [-pi, pi)."""
    twopi = 2 * math.pi
    return (angle + math.pi) % twopi - math.pi


@dataclass
class Point2D:
    x: float
    y: float


@dataclass
class PointPolar:
    r: float
    theta: float


@dataclass
class Point3D:
    x: float
    y: float
    z: float


@dataclass
class PointSpherical:
    r: float
    theta: float
    phi: float


def polar_to_cart(r: float, theta: float) -> tuple[float, float]:
    """Convert polar to Cartesian coordinates.

    Args:
        r: Radius.
        theta: Angle in radians.

    Returns:
        Tuple of ``(x, y)``.
    """
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


def cart_to_polar(x: float, y: float) -> tuple[float, float]:
    """Convert Cartesian to polar coordinates.

    Args:
        x: X coordinate.
        y: Y coordinate.

    Returns:
        Tuple of ``(r, theta)`` where ``theta`` is normalized to ``[-pi, pi)``.
    """
    r = math.hypot(x, y)
    theta = math.atan2(y, x)
    return r, _normalize_angle(theta)


def spherical_to_cart(r: float, theta: float, phi: float) -> tuple[float, float, float]:
    """Convert spherical to Cartesian coordinates.

    Args:
        r: Radius.
        theta: Azimuthal angle in radians.
        phi: Elevation angle from the XY-plane in radians.

    Returns:
        Tuple of ``(x, y, z)``.
    """
    x = r * math.cos(phi) * math.cos(theta)
    y = r * math.cos(phi) * math.sin(theta)
    z = r * math.sin(phi)
    return x, y, z


def cart_to_spherical(x: float, y: float, z: float) -> tuple[float, float, float]:
    """Convert Cartesian to spherical coordinates.

    Args:
        x: X coordinate.
        y: Y coordinate.
        z: Z coordinate.

    Returns:
        Tuple of ``(r, theta, phi)`` with angles normalized to ``[-pi, pi)``.
    """
    r = math.sqrt(x * x + y * y + z * z)
    theta = math.atan2(y, x)
    phi = math.atan2(z, math.hypot(x, y))
    return r, _normalize_angle(theta), _normalize_angle(phi)
