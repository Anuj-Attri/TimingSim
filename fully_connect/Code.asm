# Instruction Test: Fully Connected
# Author: Anuj Attri

# SMEM 0: 0 the starting vaddr of vector
# SMEM 1: 256 the starting vaddr of matrix
# SMEM 2: 70000 the starting vaddr of result
# SMEM 3: 256 the size of vector
# SMEM 4: 1
# SMEM 5: 65536 + 256
# SMEM 6: 64
# Load addresses to scalar reg
# SMEM 0: 0 the starting vaddr of vector
# SMEM 1: 256 the starting vaddr of matrix
# SMEM 2: 70000 the starting vaddr of result
# SMEM 3: 256 the size of vector
# SMEM 4: 1
# SMEM 5: 65536 + 256
# SMEM 6: 64
# Load addresses to scalar reg
LS SR2 SR0 1        # SR2 = Matrix = B address = 256
LS SR4 SR0 2        # SR4 = starting addr of reduction array = 70000
LS SR7 SR0 3        # SR7 = size of vector = 256
LS SR6 SR0 4        # SR6 = 1
LS SR3 SR0 6        # SR3 = length size = 64
# Start of DP
LV VR1 SR1          # Loop1 start: Load first 64 of A in VR1
LV VR2 SR2          # Load first 64 of B in VR2
MULVV VR1 VR1 VR2   # Multiple first 64 of A and B to VR1
ADDVV VR0 VR0 VR1   # Add dp of first 64 of A and B to VR0
ADD SR1 SR1 SR3     # Increment addr of A by 64
ADD SR2 SR2 SR3     # Increment addr of B by 64
BLT SR1 SR7 -6      # If start addr of A(SR1) less than 256, branch to Loop1
# Start of the array reduction, stored in VR0
SV VR0 SR4          # Loop2 start: reduction array now stored starting from addr 70000
BEQ SR3 SR6 7       # If SR3 == 1, reduced dp is already stored at 70000, branch to HALT
SRA SR3 SR3 SR6     # Shift right SR3 by 1 (SR3 /= 2)
MTCL SR3            # Set value in SR3 to VLR
ADD SR5 SR4 SR3     # SR5 is the addr of second half of the reduction array = 70000 + VLR
LV VR1 SR5          # Load the second half of the reduction array to VR1
ADDVV VR0 VR0 VR1   # Add the first and second half of the reduction array to VR0
BEQ SR0 SR0 -7      # jmp to reduction array store, Loop2 start
# Change to the next row of matrix
ADD SR4 SR4 SR6     # The memory to put the result increment by 1
LS SR1 SR0 0        # SR1 = Vector = A address = 0
LS SR5 SR0 5        # SR5 = 65536 + 256
LS SR3 SR0 6        # SR3 = length size = 64
MTCL SR3            # Set VLR = 64
ADDVV VR0 VR3 VR3     # Clean VR0
BLT SR2 SR5 -21     # If Matrix B address is smaller than its max address, loop DP again
HALT                # End of execution, address starting from 70000 in VDMEM should be 5625216,5625216,...,5625216 with 256 times of 5625216