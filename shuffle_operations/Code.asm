# Instruction Test: Register Shuffle Operations
# Author: Anuj Attri

LV VR1, SR0          # Load vector data from memory address in SR0 into VR1
UNPACKLO VR2, VR0, VR1 
UNPACKLO VR3, VR1, VR0 
UNPACKHI VR4, VR0, VR1 
UNPACKHI VR5, VR1, VR0 
PACKLO VR6, VR2, VR3   
PACKHI VR7, VR2, VR3   # Pack upper halves of vectors in VR2 and VR3 into VR7
HALT                   