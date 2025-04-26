# ---------- Radio / geometry -------------------------------------------------
CHANNEL           = 36                   # 5 GHz
CENTER_FREQUENCY  = 5_180_000_000        # Hz
ANTENNA_SPACING   = 0.05                 # ≈5 cm between WDR4300 antennas

# ---------- Capture ----------------------------------------------------------
SAMPLE_DURATION   = 10                   # seconds of data to collect
PCAP_BUFSIZE      = 4096                 # bytes | tcpdump -s <N>

# ---------- Distance via CIR -----------------------------------------------
SPEED_OF_LIGHT    = 299_792_458          # m s⁻¹
CHANNEL_BW        = 40e6                 # Hz (HT40)

# ---------- Misc -------------------------------------------------------------
AP_MAC            = "C0:4A:00:DE:AD:BE"  # router’s BSSID
