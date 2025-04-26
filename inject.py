import subprocess, time
from scapy.all import RadioTap, Dot11, sendp
from config import AP_MAC, FTM_TX_RATE, FTM_BURST_SIZE

def send_ftm_burst(iface: str):
    """
    Craft and inject 802.11 action frames (category = 0x3, action = 0x24)
    requesting an FTM exchange. Many driver/AP combos will automatically
    reply with an FTM response carrying the timestamps we need.
    """
    dot11 = Dot11(type=0, subtype=13,     # action frame
                  addr1=AP_MAC,
                  addr2="de:ad:be:ef:ca:fe",
                  addr3=AP_MAC)
    # Category 3 (HT), Action 36 (FTM Request) per spec
    payload = bytes.fromhex("03 24") + b"\x00"*2
    frame = RadioTap()/dot11/payload

    for _ in range(FTM_BURST_SIZE):
        sendp(frame, iface=iface, verbose=False)
        time.sleep(1/FTM_TX_RATE)
