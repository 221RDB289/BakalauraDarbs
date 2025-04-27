import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


def parse_tripinfo(filepath, vtype):
    trips = []
    tree = ET.parse(filepath)
    root = tree.getroot()
    # noderīgā info piemērs:
    # departDelay="3.00" arrival="11346.00" duration="11343.00" routeLength="77559.02" waitingTime="1199.00" waitingCount="58" stopTime="1740.00" timeLoss="2551.80" speedFactor="0.97"
    for tripinfo in root.findall("tripinfo"):
        if vtype == tripinfo.get("vType"):
            result = {
                "id": f'Kurjers Nr. {int(tripinfo.get("id").split("_")[1])+1}',
                # "departDelay": float(tripinfo.get("departDelay")),
                # "arrival": float(tripinfo.get("arrival")),
                "duration": float(tripinfo.get("duration")),
                "routeLength": int(
                    float(tripinfo.get("routeLength")) / 1000
                ),  # m uz km
                "waitingTime": float(tripinfo.get("waitingTime")),
                "waitingCount": int(tripinfo.get("waitingCount")),
                "stopTime": float(tripinfo.get("stopTime")),
                "timeLoss": float(tripinfo.get("timeLoss")),
                "speedFactor": float(tripinfo.get("speedFactor")),
            }
            trips.append(result)
    return trips


def visualize_data(trips):
    ids = [trip["id"] for trip in trips]
    durations = [trip["duration"] for trip in trips]
    routeLengths = [trip["routeLength"] for trip in trips]
    waitingTimes = [trip["waitingTime"] for trip in trips]
    stopTimes = [trip["stopTime"] for trip in trips]
    timeLosses = [trip["timeLoss"] for trip in trips]
    speedFactors = [trip["speedFactor"] for trip in trips]

    fig, ax = plt.subplots()
    ax.bar(ids, routeLengths, color="Orange")
    ax.set_title("Kurjeru Nobrauktais Ceļš (km)")
    for i in range(len(ids)):
        plt.text(i, routeLengths[i] // 2, routeLengths[i], ha="center")
    plt.show()


if __name__ == "__main__":
    filepath = "output/tripinfo.xml"
    vtype = "myCourier"
    trips = parse_tripinfo(filepath, vtype)
    print(trips)
    visualize_data(trips)
