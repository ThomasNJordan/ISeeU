# Radio / environment settings
CHANNEL          = 36          # 5 GHz band gives 80 MHz BW for finer delay resolution
CENTER_FREQUENCY = 5_180_000_000  # Hz
SAMPLE_DURATION  = 10          # seconds

# FTM parameters (IEEE 802.11-2016, Table 11-10ai)
FTM_TX_RATE      = 10          # Hz
FTM_BURST_SIZE   = 8           # # frames per burst

# Geometry (you = origin, AP somewhere in front)
AP_MAC           = "02:11:22:33:44:55"   # your own AP in FTM responder mode
ANTENNA_SPACING  = 0.03        # 3 cm, roughly λ/2 @ 5 GHz
SPEED_OF_LIGHT   = 299_792_458 # m s⁻¹
