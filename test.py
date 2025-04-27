import sumolib

net = sumolib.net.readNet("simulation_files/map.net.xml")

# pārbauda vau abi ceļi ir savienoti:
edge1 = net.getEdge("-43376762")
edge2 = net.getEdge("-124457052#0")

if edge1.getToNode() == edge2.getFromNode() or edge1.getFromNode() == edge2.getToNode():
    print(f"Edge {edge1.getID()} is connected to {edge2.getID()}")
else:
    print(f"Edge {edge1.getID()} is NOT connected to {edge2.getID()}")
