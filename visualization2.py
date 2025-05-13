import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from collections import Counter

# Path to your trips file
TRIPS_FILE = "simulation_files/traffic.trips.xml"

# Parse XML and collect depart times
tree = ET.parse(TRIPS_FILE)
root = tree.getroot()

depart_times = [float(trip.get("depart")) for trip in root.findall("trip")]
counter = Counter(depart_times)

# Sort by time
times = sorted(counter.keys())
counts = [counter[t] for t in times]

# Plot
plt.figure(figsize=(12, 6))
plt.bar(times, counts, width=1.0)
plt.title("Vehicle Departures per Second (Binomial Distribution)")
plt.xlabel("Time (s)")
plt.ylabel("Number of Departures")
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()
