#!/usr/bin/env python3
"""
Functions to compute orbital elements
"""

import numpy as np
import numpy.linalg as la
from numba import jit


@jit(nopython=True)
def get_inclination(state):
    """Function computes inclination in radians from a two-body state vector, in inertially frozen frame
    
    Args:
        state (np.array): array of cartesian state in inertially frozen frame
    Returns:
        (float): inclination in radians
    """

    # decompose state to position and velocity vector
    r = np.array([state[0], state[1], state[2]])
    v = np.array([state[3], state[4], state[5]])
    # angular momentum
    h = np.cross(r,v)
    # inclination
    inc = np.arccos(h[2] / la.norm(h))
    return inc


@jit(nopython=True)
def get_raan(state):
    """Function computes RAAN in radians from a two-body state vector, in inertially frozen frame
    
    Args:
        state (np.array): array of cartesian state in inertially frozen frame
    Returns:
        (float): RAAN in radians
    """
    
    # decompose state to position and velocity vector
    r = np.array([state[0], state[1], state[2]])
    v = np.array([state[3], state[4], state[5]])
    # angular momentum
    h = np.cross(r,v)
    # normal direction of xy-plane
    zdir = np.array([0, 0, 1])
    ndir = np.cross(zdir, h)
    # compute RAAN
    raan = np.arctan2(ndir[1], ndir[0])
    return raan
    
    
@jit(nopython=True)
def get_eccentricity(state, mu):
    """Function computes eccentricity vector from a two-body state vector, in inertially frozen frame
    
    Args:
        state (np.array): array of cartesian state in inertially frozen frame
        mu (float): two-body mass parameter
    Returns:
        (np.arr): eccentricity vector
    """
    
    # decompose state to position and velocity vector
    r = np.array([state[0], state[1], state[2]])
    v = np.array([state[3], state[4], state[5]])
    # angular momentum
    h = np.cross(r,v)
    # normal direction of xy-plane
    #zdir = np.array([0, 0, 1])
    #ndir = np.cross(zdir, h)
    # compute eccentricity vector
    ecc = (1/mu) * np.cross(v,h) - r/la.norm(r)
    return ecc


@jit(nopython=True)
def get_omega(state, mu):
    """Function computes argument of periapsis in radians from a two-body state vector, in inertially frozen frame
    
    Args:
        state (np.array): array of cartesian state in inertially frozen frame
        mu (float): two-body mass parameter
    Returns:
        (float): argument of periapsis in radians
    """
    
    # decompose state to position and velocity vector
    r = np.array([state[0], state[1], state[2]])
    v = np.array([state[3], state[4], state[5]])
    # angular momentum
    h = np.cross(r,v)
    # normal direction of xy-plane
    zdir = np.array([0, 0, 1])
    ndir = np.cross(zdir, h)
    # compute eccentricity vector
    ecc = (1/mu) * np.cross(v,h) - r/la.norm(r)
    # compute argument of periapsis
    omega = np.arccos( np.dot(ndir,ecc) / (la.norm(ndir)*la.norm(ecc)) )
    if ecc[2] < 0:
        omega = 2*np.pi - omega
    return omega


@jit(nopython=True)
def get_trueanom(state, mu):
    """Function computes argument of periapsis in radians from a two-body state vector, in inertially frozen frame
    
    Args:
        state (np.array): array of cartesian state in inertially frozen frame
        mu (float): two-body mass parameter
    Returns:
        (float): true anomaly in radians
    """
    # decompose state to position and velocity vector
    r = np.array([state[0], state[1], state[2]])
    v = np.array([state[3], state[4], state[5]])
    # angular momentum
    h = la.norm( np.cross(r,v) )
    # radial velocity
    vr = np.dot(v,r)/la.norm(r)
    theta = np.arctan2(h*vr, h**2/la.norm(r) - mu)
    return theta


@jit(nopython=True)
def get_semiMajorAxis(state, mu):
    """Function computes semi major axis of keplrian orbit
    
    Args:
        state (np.array): array of cartesian state in inertially frozen frame
        mu (float): two-body mass parameter
    Returns:
        (float): semi-major axis
    """
    # decompose state to position and velocity vector
    r = np.array([state[0], state[1], state[2]])
    v = np.array([state[3], state[4], state[5]])
    # angular momentum
    h = la.norm( np.cross(r,v) )
    # eccentricity
    e = la.norm( get_eccentricity(state, mu) )
    # semi-major axis
    a = h**2 / (mu*(1 - e**2))
    return a


@jit(nopython=True)
def get_period(state, mu):
    """Function computes period of keplerian orbit
    
    Args:
        state (np.array): array of cartesian state in inertially frozen frame
        mu (float): two-body mass parameter
    Returns:
        (float): period
    """
    a = get_semiMajorAxis(state, mu)
    if a < 0:
        period = -1
    else:
        period = 2*np.pi*np.sqrt(a**3/mu)
    return period



