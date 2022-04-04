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

mdi.MDI_Send_Command("<NATOMS", comm)
natoms = mdi.MDI_Recv(1, mdi.MDI_INT, comm)
print("NAtoms: " + str(natoms))

#mdi.MDI_Send_Command("<ENERGY", comm)
#energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
#print("Energy1: " + str(energy))

#mdi.MDI_Send_Command("<ENERGY", comm)
#energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
#print("Energy2: " + str(energy))

#mdi.MDI_Send_Command("<FORCES", comm)
#forces = mdi.MDI_Recv(3*natoms, mdi.MDI_DOUBLE, comm)
##print("Forces: " + str(forces))

#mdi.MDI_Send_Command("<POLEDIMS", comm)
#polardim = mdi.MDI_Recv(1, mdi.MDI_INT, comm)
#print("Polardim: " + str(polardim))


# Get the charges
mdi.MDI_Send_Command("<CHARGES", comm)
charges = mdi.MDI_Recv(natoms, mdi.MDI_DOUBLE, comm)
#print("Charges: " + str(charges))


# Get the polarizabilities
#mdi.MDI_Send_Command("<POLARITIES", comm)
#polarities = mdi.MDI_Recv(natoms, mdi.MDI_DOUBLE, comm)
#print("Polarities: " + str(polarities))

# Get the multipoles
mdi.MDI_Send_Command("<MULTIPOLES", comm)
multipoles = mdi.MDI_Recv(9*natoms, mdi.MDI_DOUBLE, comm)
for iatom in range(natoms):
    print("Multipoles " + str(iatom) + ":" + str(multipoles[9*(iatom-1):9*(iatom)]))

do_polarize = True
if do_polarize:

    multipoles[9*(328-1)] = -0.84608
    multipoles[9*(329-1)] = 0.37959
    multipoles[9*(330-1)] = 0.41834
    multipoles[9*(1165-1)] = -0.73451
    multipoles[9*(1166-1)] = 0.40495
    multipoles[9*(1167-1)] = 0.37771

    polarize = 1

else:

    multipoles[9*(328-1)] = 0.0
    multipoles[9*(329-1)] = 0.0
    multipoles[9*(330-1)] = 0.0
    multipoles[9*(1165-1)] = 0.0
    multipoles[9*(1166-1)] = 0.0
    multipoles[9*(1167-1)] = 0.0

    polarize = 0

# Send the multipoles
mdi.MDI_Send_Command(">MULTIPOLES", comm)
mdi.MDI_Send(multipoles, 9*natoms, mdi.MDI_DOUBLE, comm)

mdi.MDI_Send_Command(">POLARIZE", comm)
mdi.MDI_Send(polarize, 1, mdi.MDI_INT, comm)

##polarities[0] += 0.1
#mdi.MDI_Send_Command(">POLARITIES", comm)
#mdi.MDI_Send(polarities, natoms, mdi.MDI_DOUBLE, comm)

##multipoles[6] += 0.1
#mdi.MDI_Send_Command(">MULTIPOLES", comm)
#mdi.MDI_Send(multipoles, 9*natoms, mdi.MDI_DOUBLE, comm)

mdi.MDI_Send_Command("<ENERGY", comm)
energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
print("Energy3: " + str(energy))


print("CCC")

mdi.MDI_Send_Command("EXIT", comm)
