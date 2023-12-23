from PySpice.Spice.Parser import SpiceParser

netlist_path = "circuit.netlist"
parser = SpiceParser(path=netlist_path)
circuit = parser.build_circuit()

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

for node in analysis.nodes.values():
    print(f"Node {str(node)}: {float(node):4.1f} V")
