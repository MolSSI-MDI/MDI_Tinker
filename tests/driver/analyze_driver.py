import mdi
from mdi import MDI_NAME_LENGTH, MDI_COMMAND_LENGTH
import sys

iarg = 1
while iarg < len(sys.argv):
    arg = sys.argv[iarg]

    if arg == "-mdi":
        # Initialize MDI
        if len(sys.argv) <= iarg+1:
            raise Exception("Argument to -mdi option not found")
        mdi.MDI_Init(sys.argv[iarg+1])
        iarg += 1
    else:
        raise Exception("Unrecognized argument")

    iarg += 1

# Connect to the engine
comm = mdi.MDI_Accept_Communicator()

# Get the name of the engine, which will be checked and verified at the end
mdi.MDI_Send_Command("<NAME", comm)
initial_name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)

# Verify that the engine is still responsive
mdi.MDI_Send_Command("<NAME", comm)
final_name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)
assert initial_name == final_name
print("Engine name: " + str(final_name))

mdi.MDI_Send_Command("<CELL", comm)
cell = mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm)
print("Cell: " + str(cell))

mdi.MDI_Send_Command("<CELL_DISPL", comm)
cell_displ = mdi.MDI_Recv(3, mdi.MDI_DOUBLE, comm)
print("Cell_displ: " + str(cell_displ))

mdi.MDI_Send_Command("<NATOMS", comm)
natoms = mdi.MDI_Recv(1, mdi.MDI_INT, comm)
print("NAtoms: " + str(natoms))

mdi.MDI_Send_Command("<COORDS", comm)
coords = mdi.MDI_Recv(3*natoms, mdi.MDI_DOUBLE, comm)
print("Coords: " + str(coords))

mdi.MDI_Send_Command("<ENERGY", comm)
energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
print("Energy: " + str(energy))

coords[0] += 0.1
mdi.MDI_Send_Command(">COORDS", comm)
mdi.MDI_Send(coords, 3*natoms, mdi.MDI_DOUBLE, comm)
print("Coords: " + str(coords))

mdi.MDI_Send_Command("<ENERGY", comm)
energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
print("Energy: " + str(energy))

print("CCC")

mdi.MDI_Send_Command("EXIT", comm)
