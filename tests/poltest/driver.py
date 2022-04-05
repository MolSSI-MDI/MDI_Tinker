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


class MDIDriver:

    def __init__(self):
        # Connect to the engine
        self.comm = mdi.MDI_Accept_Communicator()


        # Number of atoms in the system
        self.natoms = 0

        # Flag whether to compute polarization contribution to the energy
        self.polarize = 0
        
        # The current multipoles of the system
        self.multipoles = None

        # The current polarities of the system
        self.polarities = None


    def set_polar(self, do_polarize):

        atoms_to_zero = [328, 329, 330, 1165, 1166, 1167] 


        # Set the polarities of the QM atoms to zero
        for iatom in atoms_to_zero:
            self.polarities[iatom-1] = 0.0


        if do_polarize:

            self.polarize = 1

            self.multipoles[9*(328-1)] = -0.84608
            self.multipoles[9*(329-1)] = 0.37959
            self.multipoles[9*(330-1)] = 0.41834
            self.multipoles[9*(1165-1)] = -0.73451
            self.multipoles[9*(1166-1)] = 0.40495
            self.multipoles[9*(1167-1)] = 0.37771

            # Zero all components of the multipoles on a selected group of atoms, 
            # except for the monopoles
              
            for iatom in atoms_to_zero:
                for i in range(1, 9):
                    self.multipoles[9*(iatom-1)+i] = 0.0


        else:

            self.polarize = 0

            # Zero the multipoles on the QM atoms
            for iatom in atoms_to_zero:
                for i in range(9):
                    self.multipoles[9*(iatom-1)+i] = 0.0


        # Send the multipoles to the engine
        mdi.MDI_Send_Command(">MULTIPOLES", self.comm)
        mdi.MDI_Send(self.multipoles, 9*self.natoms, mdi.MDI_DOUBLE, self.comm)

        # Send the polarize flag to the engine
        mdi.MDI_Send_Command(">POLARIZE", self.comm)
        mdi.MDI_Send(self.polarize, 1, mdi.MDI_INT, self.comm)
        
        # Send the polarities to the engine
        mdi.MDI_Send_Command(">POLARITIES", self.comm)
        mdi.MDI_Send(self.polarities, self.natoms, mdi.MDI_DOUBLE, self.comm)

    def run(self):

        # Get the name of the engine, which will be checked and verified at the end
        mdi.MDI_Send_Command("<NAME", self.comm)
        name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, self.comm)
        print("Engine name: " + str(name))

        mdi.MDI_Send_Command("<NATOMS", self.comm)
        self.natoms = mdi.MDI_Recv(1, mdi.MDI_INT, self.comm)
        print("NAtoms: " + str(self.natoms))

        # Get the multipoles
        mdi.MDI_Send_Command("<MULTIPOLES", self.comm)
        self.multipoles = mdi.MDI_Recv(9*self.natoms, mdi.MDI_DOUBLE, self.comm)
        #for iatom in range(self.natoms):
        #    print("Multipoles " + str(iatom) + ":" + str(self.multipoles[9*(iatom-1):9*(iatom)]))

        # Get the polarities
        mdi.MDI_Send_Command("<POLARITIES", self.comm)
        self.polarities = mdi.MDI_Recv(self.natoms, mdi.MDI_DOUBLE, self.comm)
        for iatom in range(self.natoms):
            print("Polarities " + str(iatom) + ":" + str(self.polarities[iatom]))


        self.set_polar(False)



        mdi.MDI_Send_Command("<ENERGY", self.comm)
        energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, self.comm)
        print("Energy1: " + str(energy))

        self.set_polar(True)



        mdi.MDI_Send_Command("<ENERGY", self.comm)
        energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, self.comm)
        print("Energy2: " + str(energy))

        mdi.MDI_Send_Command("EXIT", self.comm)



driver = MDIDriver()
driver.run()
