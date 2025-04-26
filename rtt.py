import numpy as np
from config import SPEED_OF_LIGHT

def ftm_distance(t1, t2, t3, t4):
    """
    IEEE 802.11mc two-way timing:
        STA sends FTM Req at t1, AP receives at t2.
        AP responds at t3, STA receives at t4.
    Propagation time = ((t2-t1) + (t4-t3) – (t3-t2) – (t1-t4)) / 2
    But spec defines Δt  = (t4-t1) – (t3-t2), so
        d = c * Δt / 2
    All timestamps in nanoseconds.
    """
    delta = (t4 - t1) - (t3 - t2)
    return 0.5 * SPEED_OF_LIGHT * (delta * 1e-9)   # metres
