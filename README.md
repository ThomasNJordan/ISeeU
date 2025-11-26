# ISeeU
[ARCHIVE] PantherHacks Cyber Track Winner 🏆🏆🏆


WiFi Post-Exploitation Tool for Motion Detection

## Inspiration
Rooted a router? Now what? What if you could literally *see* into a target's physical environment? Introducing ISeeU

The inspiration for the project came from a very cool project from Carnegie Mellon University doing a very similar thing. The main goal was to attempt to utilize Wi-Fi routers to put people in a 3D environment, with near pinpoint accuracy depending on router firmware and ability, and use it as a LIDAR camera. 

## What it does
The finalized version of the project (after several pivots) utilizes a Wi-Fi access point in tandem with a router to create a connection between the two devices. If someone walks between the connection, the power consumption to maintain the connection will fluctuate, signifying that someone or something has moved between the devices. 

## How we built it
We got custom drivers to place the antennas into monitor mode. We then used a library called Scapy to listen to neighboring Wi-Fi access point broadcast packets. Using the power consumption located in the Radio Header, we can determine the strength of the signal that is being received, and find any fluctuations that will indicate motion between the two devices. 

## Challenges we ran into
- With internal storage
  - The router prior to being configured to use a USB drive as an external storage device has an internal 
    storage capacity of 1.3 MB. The operating system took up .09 MB leaving us with a 
    measly 0.4 MB to work with. Once we were able to configure the router to accept an external drive 
    though, we were able to have a little more than 15 GB of storage. This, like the other problems listed 
    below, took a surprising amount of time to fix, but once a solution was found, it allowed us to begin 
    work on the project. 
- Driver issues
  - Driver issues were a never-ending problem for us during this project. With nearly 24 hours sunk into 
    either attempting to create, debug, or deal with drivers breaking constantly, we were forced to pivot 
    project ideas from using CIS to RISSI due to the router simply breaking when we'd try to flash 
    patched firmware to it. 
- Outdated software dependencies
  - Due to the age of the router, there were outdated software dependencies everywhere as updating 
    the router was not an option. Issues arose when upgrading the firmware, as the version of gcc, g++, 
    python, and other languages were so old that they were no longer available in most package 
    managers. We had to compile each of those languages from source, and a multitude of other 
    examples similar to this existed for us throughout the entire 48 hours of the hackathon. 

## Accomplishments that we're proud of
- After pivoting several times, we finally were able to create a deliverable we were all proud of. Scanning the connection between the router and the access point to determine movement isn't exactly what we had in mind upon entering the hackathon, but it is an impressive demonstration of the lack of security around routers and their access points as anyone capable of this undertaking could create artificial motion detection systems throughout any building of their choosing. 

## What we learned
Our group learned that it is possible to use Radio Header information to detect human movement and object placement in an environment. This is a new domain of physical security risk from a digital device. This presents a new threat capability and is worth considering when developing a security plan. 

## What's next for ISeeYou Router Motion Detection System
We will finish debugging and we plan to add a custom driver to the firmware to read CSI data for a clearer image and better resolution. We also will experiment with the broadcast rate with CSI and RSSI information as to increase the amount of data points we have.
