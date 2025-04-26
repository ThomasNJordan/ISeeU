"""
Global knobs that describe your radio front-end, not the algorithm.
Tweak once; all other modules `import config`.
"""

# --- RF / hardware geometry --------------------------------------------------
CENTER_FREQUENCY  = 5_180_000_000     # Hz   (Channel 36 on 5 GHz)
ANTENNA_SPACING   = 0.05              # metres  (≈5 cm between WDR4300 antennas)
CHANNEL_BW        = 40e6              # Hz   (HT40 → 1/BW ≈ 25 ns delay bin)

# --- Physics constant --------------------------------------------------------
SPEED_OF_LIGHT    = 299_792_458       # m · s⁻¹
