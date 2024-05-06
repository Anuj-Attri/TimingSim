# Author: Anuj Attri

# Start

import os
import argparse
import copy
import re
from collections import deque
import sys

complete_list = []
vlr_list = []

def copy_file_contents(iodir, output_str):
    # check if file exists at the specified directory path
    if os.path.exists(iodir):
        # open the file for reading
        with open(iodir, 'r') as file:
            # read the contents of the file
            file_contents = file.read() + "\n"
            # concatenate the file contents to the front of output_str
            new_output_str = "\n\n" + file_contents + "\n\n" + output_str
            # print(f"All contents of file {iodir} copied to the front of {output_str}")
            return new_output_str
    else:
        print(f"File not found at {iodir}")
        return output_str
    
def parseInstr(instrStr: str):
     # Check if the input string matches the format "LV VR1 (0,1,...)"
    match = re.match(r'^(\w+)\s+(\w+)\s+\((\d+(?:,\s*\d+)*)\)$', instrStr)
    if match:
        # If it matches, remove the spaces between the commas and split the last part by commas
        last_part = [int(d) for d in match.group(3).replace(' ','').split(',')]
        # Return the parts as a list with the last part as a list of integers
        instrList = [match.group(1), match.group(2), last_part]
    else:
        # Check if the input string matches the format "B (3)"
        match = re.match(r'^(\w+)\s+\((\d+)\)$', instrStr)
        if match:
            # If it matches, return the parts as a list with the last part as an integer
            instrList = [match.group(1), int(match.group(2))]
        else:
            # If it doesn't match either format, split the input string by whitespace and return the parts as a list
            instrList = re.split(r'\s+', instrStr.strip())
    # print(instrList)
    return instrList

class Config(object):
    def __init__(self, iodir):
        self.filepath = os.path.abspath(os.path.join(iodir, "Config.txt"))
        self.parameters = {} # dictionary of parameter name: value as strings.

        try:
            with open(self.filepath, 'r') as conf:
                self.parameters = {line.split('=')[0].strip(): line.split('=')[1].split('#')[0].strip() for line in conf.readlines() if not (line.startswith('#') or line.strip() == '')}
            print("Config - Parameters loaded from file:", self.filepath)
            print("Config parameters:", self.parameters)
        except:
            print("Config - ERROR: Couldn't open file in path:", self.filepath)
            raise

class IMEM(object):
    def __init__(self, iodir):
        self.size = pow(2, 16) # Can hold a maximum of 2^16 instructions.
        self.filepath = os.path.abspath(os.path.join(iodir, "resolved_Code.asm"))
        # self.filepath = os.path.abspath(os.path.join(iodir, "Code.asm"))
        self.instructions = []

        try:
            with open(self.filepath, 'r') as insf:
                self.instructions = [ins.split('#')[0].strip() for ins in insf.readlines() if not (ins.startswith('#') or ins.strip() == '')]
            print("IMEM - Instructions loaded from file:", self.filepath)
            # print("IMEM - Instructions:", self.instructions)
        except:
            print("IMEM - ERROR: Couldn't open file in path:", self.filepath)
            raise
        # print(self.instructions)
    def Read(self, idx): # Use this to read from IMEM.
        if idx < self.size:
            return self.instructions[idx]
        else:
            print("IMEM - ERROR: Invalid memory access at index: ", idx, " with memory size: ", self.size)

class DMEM(object):
    # Word addressible - each address contains 32 bits.
    def __init__(self, name, iodir, addressLen):
        self.name = name
        self.size = pow(2, addressLen)
        self.min_value  = -pow(2, 31)
        self.max_value  = pow(2, 31) - 1
        self.ipfilepath = os.path.abspath(os.path.join(iodir, name + ".txt"))
        self.opfilepath = os.path.abspath(os.path.join(iodir, name + "OP.txt"))
        self.data = []

        try:
            with open(self.ipfilepath, 'r') as ipf:
                self.data = [int(line.strip()) for line in ipf.readlines()]
            print(self.name, "- Data loaded from file:", self.ipfilepath)
            # print(self.name, "- Data:", self.data)
            self.data.extend([0x0 for i in range(self.size - len(self.data))])
        except:
            print(self.name, "- ERROR: Couldn't open input file in path:", self.ipfilepath)
            raise

    def Read(self, idx): # Use this to read from DMEM.
        pass # Replace this line with your code here.

    def Write(self, idx, val): # Use this to write into DMEM.
        pass # Replace this line with your code here.

    def dump(self):
        try:
            with open(self.opfilepath, 'w') as opf:
                lines = [str(data) + '\n' for data in self.data]
                opf.writelines(lines)
            print(self.name, "- Dumped data into output file in path:", self.opfilepath)
        except:
            print(self.name, "- ERROR: Couldn't open output file in path:", self.opfilepath)
            raise

class RegisterFile(object):
    def __init__(self, name, count, length = 1, size = 32):
        self.name       = name
        self.reg_count  = count
        self.vec_length = length # Number of 32 bit words in a register.
        self.reg_bits   = size
        self.min_value  = -pow(2, self.reg_bits-1)
        self.max_value  = pow(2, self.reg_bits-1) - 1
        self.registers  = [[0x0 for e in range(self.vec_length)] for r in range(self.reg_count)] # list of lists of integers

    def Read(self, idx):
        pass # Replace this line with your code.

    def Write(self, idx, val):
        pass # Replace this line with your code.

    def dump(self, iodir):
        opfilepath = os.path.abspath(os.path.join(iodir, self.name + ".txt"))
        try:
            with open(opfilepath, 'w') as opf:
                row_format = "{:<13}"*self.vec_length
                lines = [row_format.format(*[str(i) for i in range(self.vec_length)]) + "\n", '-'*(self.vec_length*13) + "\n"]
                lines += [row_format.format(*[str(val) for val in data]) + "\n" for data in self.registers]
                opf.writelines(lines)
            print(self.name, "- Dumped data into output file in path:", opfilepath)
        except:
            print(self.name, "- ERROR: Couldn't open output file in path:", opfilepath)
            raise
        
class BusyBoard(object):
    def __init__(self, count: int):
        self.size = count
        self.element  = [0 for _ in range(count)] # list of lists of integers

    def Mark(self, idx: int):
        '''
            Only Mark if it is going to write this register/memory 
        '''
        if idx != None:
            self.element[idx] += 1

    def Clear(self, idx: int):
        if idx != None and self.element[idx] > 0:
            self.element[idx] -= 1

    def isBusy(self, idx: int):
        if idx != None:
            return self.element[idx] != 0

class MemoryBank(object):
    def __init__(self, bankSize: int, busyTime: int):
        self.size = bankSize
        self.bankBusyCount  = [0 for _ in range(bankSize)]
        self.bankMemoryAddr = [-1 for _ in range(bankSize)]

        self.busyTime = busyTime

    def isBusy(self, bank_idx: int):
        if bank_idx != None:
            if (self.bankMemoryAddr[bank_idx] == -1):
                return False
            else:
                return True
        
    def InitBank(self, mem_addr: int):
        '''
            bank_idx: the bank to use
            mem_addr: the memory address to access
        '''
        # Interleved memory bank
        idx = mem_addr % self.size
        if not self.isBusy(idx):
            self.bankBusyCount[idx] = self.busyTime - 1
            self.bankMemoryAddr[idx] = mem_addr
            return idx
        # End of Interleved memory bank

        # # Continuous memory bank
        # mem_per_bank = pow(2, 17) // self.size
        # idx = mem_addr // mem_per_bank
        # if not self.isBusy(idx):
        #     self.bankBusyCount[idx] = self.busyTime
        #     self.bankMemoryAddr[idx] = mem_addr
        #     return idx
        # # End of continuous memory bank

        # STALL since there is not empty bank!
        return -1

    def CountDown(self):
        complete_mem = -1
        for i in range(self.size):
            if self.bankBusyCount[i] > 0:
                self.bankBusyCount[i] -= 1
            elif self.bankBusyCount[i] == 0 and self.bankMemoryAddr[i] != -1:
                complete_mem = self.bankMemoryAddr[i]
                self.bankMemoryAddr[i] = -1
        return complete_mem
        
class Backend(object):
    def __init__(self, config: Config):
        # Vector operation pipeline
        self.MulPipeline = []
        self.DivPipeline = []
        self.AddPipeline = []

        # Vector memory pipeline
        self.VmemPipeline = []

        # Vector memory bank
        self.VmemBankQ = deque()
        self.VmemReturnQ = deque()

        # Scalar operation pipeline
        self.ScalarPipeline = []

        # Number of parallel instruction 
        self.numLanes = int(config.parameters["numLanes"])

        # Number of cycles takes
        self.pipelineDepthMul = int(config.parameters["pipelineDepthMul"])
        self.pipelineDepthAdd = int(config.parameters["pipelineDepthAdd"])
        self.pipelineDepthDiv = int(config.parameters["pipelineDepthDiv"])

        # VDMEM LS parameters
        self.vdmNumBanks = int(config.parameters["vdmNumBanks"])
        self.vlsPipelineDepth = int(config.parameters["vlsPipelineDepth"])
    
    def isClean(self):
        return (len(self.MulPipeline) == 0 and len(self.DivPipeline) == 0 and len(self.AddPipeline) == 0 and len(self.VmemPipeline) == 0 and len(self.ScalarPipeline) == 0)

    def dispatch(self, task_input):
        """
        task_input:
        (
            {"PC": int, "Instr": string, "cycle": int},
            "mul/div/add/scalar/vmem": string,
            numElement: int,
            busyReg: int/None,
            busyMems: list/None
        )
        """
        task, type, numElement, busyReg, busyMems = task_input
        if type == "mul" and len(self.MulPipeline) == 0:
            # !what will happen when numElement == 0?
            task["cycle"] += 1
            self.MulPipeline.append((task, self.pipelineDepthMul + numElement//self.numLanes - 2, busyReg)) # -2: the other -1 is for the cycle that dispatch it also execute one cycle
            return True
        elif type == "div" and len(self.DivPipeline) == 0:
            # !what will happen when numElement == 0?
            task["cycle"] += 1
            self.DivPipeline.append((task, self.pipelineDepthDiv + numElement//self.numLanes - 2, busyReg))
            return True
        elif type == "add" and len(self.AddPipeline) == 0:
            # !what will happen when numElement == 0?
            task["cycle"] += 1
            self.AddPipeline.append((task, self.pipelineDepthAdd + numElement//self.numLanes - 2, busyReg))
            return True
        elif type == "scalar" and len(self.ScalarPipeline) == 0:
            # !what will happen when numElement == 0?
            task["cycle"] += 1
            self.ScalarPipeline.append((task, 0, busyReg))
            return True
        elif type == "vmem" and len(self.VmemPipeline) == 0:
            # !what will happen when numElement == 0?
            if len(busyMems) == 0:
                # If no memory access
                # Add the task to complete list
                complete_list.append(task)
                return True
            else: 
                # Add the first mem access to Vmem bank
                return_value = public_vmembb.InitBank(mem_addr=busyMems[0])
                if return_value == -1:
                    # no available bank!  STALL! Do NOTHING!
                    return False
                else:
                    # available bank
                    task["cycle"] += 1
                    # Initialize memory access queue and dispatch the first one to memory bank
                    self.VmemBankQ = deque(busyMems)
                    self.VmemReturnQ = deque(busyMems)
                    self.VmemBankQ.popleft()
                    # No need to pass the time_left as it will be processed by memory bank
                    self.VmemPipeline.append((task, 0, busyReg))
                    return True
        else:
            # Either the type is not correct or the pipeline is full
            return False

    
    def update(self):
        global complete_list
        if len(self.MulPipeline) != 0:
            # task: {"PC": int, "Instr": string, "cycle": int}
            task, time_left, busyReg = self.MulPipeline[0]
            if time_left == 0:
                # Delete the element
                self.MulPipeline.clear()
                # Add the task to complete list
                complete_list.append(task)
                # Clear busyborad
                public_vrbb.Clear(busyReg)
            else:
                # Increment cycle spent
                task["cycle"] += 1
                # Count down
                self.MulPipeline[0] = (task, time_left - 1, busyReg)
        elif len(self.DivPipeline) != 0:
            # task: {"PC": int, "Instr": string, "cycle": int}
            task, time_left, busyReg = self.DivPipeline[0]
            if time_left == 0:
                # Delete the element
                self.DivPipeline.clear()
                # Add the task to complete list
                complete_list.append(task)
                # Clear busyborad
                public_vrbb.Clear(busyReg)
            else:
                # Increment cycle spent
                task["cycle"] += 1
                # Count down
                self.DivPipeline[0] = (task, time_left - 1, busyReg)
        elif len(self.AddPipeline) != 0:
            # task: {"PC": int, "Instr": string, "cycle": int}
            task, time_left, busyReg = self.AddPipeline[0]
            if time_left == 0:
                # Delete the element
                self.AddPipeline.clear()
                # Add the task to complete list
                complete_list.append(task)
                # Clear busyborad
                public_vrbb.Clear(busyReg)
            else:
                # Increment cycle spent
                task["cycle"] += 1
                # Count down
                self.AddPipeline[0] = (task, time_left - 1, busyReg)
        elif len(self.ScalarPipeline) != 0:
            # task: {"PC": int, "Instr": string, "cycle": int}
            task, _, busyReg = self.ScalarPipeline[0]
            # Delete the element
            self.ScalarPipeline.clear()
            # Add the task to complete list
            complete_list.append(task)
            # Clear SCALAR busyborad
            public_srbb.Clear(busyReg)
        elif len(self.VmemPipeline) != 0:
            # task: {"PC": int, "Instr": string, "cycle": int}
            # ! Are Vmem access complete as a whole, or it can be cleared from VMEM Busyboard one by one?
            task, _, busyReg = self.VmemPipeline[0]
            # Update the Memory Bank first
            complete_mem = public_vmembb.CountDown()
            # print("task", task, "complete_mem ", complete_mem)
            if complete_mem != -1:
                self.VmemReturnQ.remove(complete_mem)

            if len(self.VmemReturnQ) == 0:
                # Add the task to complete list
                complete_list.append(task)
                # Clear Vreg busyborad
                public_vrbb.Clear(busyReg)
                # print("task: ", task, "busyReg: ", busyReg, "busy time: ", public_vrbb.element[busyReg])
                # Reset VmemBankQ
                self.VmemBankQ.clear()
                # Reset VmemReturnQ
                self.VmemReturnQ.clear()
                # Reset VmemPipeline
                self.VmemPipeline.clear()
            else:
                # Count down
                task["cycle"] += 1
                if len(self.VmemBankQ) != 0:
                    # Try to add bank
                    return_value = public_vmembb.InitBank(mem_addr=self.VmemBankQ[0])
                    if return_value == -1:
                        # no available bank! Do NOTHING!
                        return
                    else:
                        # Successfully add to memory bank
                        self.VmemBankQ.popleft()
                        # Decrement mem access needed
                        self.VmemPipeline[0] = (task, 0, busyReg)
        else:
            # print("Empty backend!")
            return


class State(object):
    def __init__(self):
        self.IF = {"nop": False, "PC": 0}
        self.ID = {"nop": False, "Instr": {}, "op": "", "PC": 0}

class Core():
    def __init__(self, imem, sdmem, vdmem, config_input: Config):
        # Initialization
        self.IMEM = imem
        self.SDMEM = sdmem
        self.VDMEM = vdmem
        self.dataQueueDepth = int(config_input.parameters["dataQueueDepth"])
        self.computeQueueDepth = int(config_input.parameters["computeQueueDepth"])
        self.scalarQueueDepth = int(config_input.parameters["scalarQueueDepth"])
        
        self.RFs = {"SRF": RegisterFile("SRF", 8),
                    "VRF": RegisterFile("VRF", 8, 64)}
        self.state = State()
        self.nextState = State()
        
        self.PC = 0

        self.state.ID["nop"] = True
        
        
    def run(self):
        global vlr_list
        global complete_list
        instr = ""
        halt = False
        stall_time = 0
        stall = False

        vDataQ = deque()
        vComputeQ = deque()
        scalarQ = deque()

        total_cycle = 0

        while(True):
            # Backend
            # First update the backend status
            public_backend.update()

            # Dispatch the tasks in queue
            if len(vDataQ) != 0 and public_backend.dispatch(vDataQ[0]):
                vDataQ.popleft()
            if len(vComputeQ) != 0 and public_backend.dispatch(vComputeQ[0]):
                vComputeQ.popleft()
            if len(scalarQ) != 0 and public_backend.dispatch(scalarQ[0]):
                scalarQ.popleft()

            # Update cycle in the queues
            for ele in vDataQ:
                task, _, _, _, _ = ele
                task["cycle"] += 1
            for ele in vComputeQ:
                task, _, _, _, _ = ele
                task["cycle"] += 1
            for ele in scalarQ:
                task, _, _, _, _ = ele
                task["cycle"] += 1

            # End of Backend Handling

            # Decode Stage
            stall = False
            if self.state.ID["nop"] == False:
                op = self.state.ID["op"]
                pc = self.state.ID["PC"]
                # print(pc, instr)
                # Vector Operations
                if re.match(r"C(ADD|SUB|MUL|DIV)\w{2}", op):
                    rd = int(instr[1][2])
                    rs1 = int(instr[2][2])
                    rs2 = int(instr[3][2])

                    # Check Hazard
                    # print("rd busy? ", public_vrbb.isBusy(rd))
                    if (len(vComputeQ) <= self.computeQueueDepth and not public_vrbb.isBusy(rd)):
                        match op:
                            case "ADDVV" | "SUBVV":
                                if (not public_vrbb.isBusy(rs1) and not public_vrbb.isBusy(rs2)):
                                    # ! In WB to vector register, do I need to check whether rd is also busy?
                                    public_vrbb.Mark(rd)
                                    task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                                    stall_time = 0
                                    stall = False
                                    vComputeQ.append((task, "add", vlr_list[pc], rd, None))
                                else:
                                    stall = True
                            case "ADDVS" | "SUBVS":
                                if (not public_vrbb.isBusy(rs1) and not public_srbb.isBusy(rs2)):
                                    public_vrbb.Mark(rd)
                                    task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                                    stall_time = 0
                                    stall = False
                                    vComputeQ.append((task, "add", vlr_list[pc], rd, None))
                                else:
                                    stall = True    
                            case "MULVV":
                                if (not public_vrbb.isBusy(rs1) and not public_vrbb.isBusy(rs2)):
                                    public_vrbb.Mark(rd)
                                    task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                                    stall_time = 0
                                    stall = False
                                    vComputeQ.append((task, "mul", vlr_list[pc], rd, None))
                                else:
                                    stall = True
                            case "MULVS":
                                if (not public_vrbb.isBusy(rs1) and not public_srbb.isBusy(rs2)):
                                    public_vrbb.Mark(rd)
                                    task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                                    stall_time = 0
                                    stall = False
                                    vComputeQ.append((task, "mul", vlr_list[pc], rd, None))
                                else:
                                    stall = True
                            case "DIVVV":
                                if (not public_vrbb.isBusy(rs1) and not public_vrbb.isBusy(rs2)):
                                    public_vrbb.Mark(rd)
                                    task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                                    stall_time = 0
                                    stall = False
                                    vComputeQ.append((task, "div", vlr_list[pc], rd, None))
                                else:
                                    stall = True
                            case "DIVVS":
                                if (not public_vrbb.isBusy(rs1) and not public_srbb.isBusy(rs2)):
                                    public_vrbb.Mark(rd)
                                    task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                                    stall_time = 0
                                    stall = False
                                    vComputeQ.append((task, "div", vlr_list[pc], rd, None))
                                else:
                                    stall = True
                            case _ :
                                print("Core run - ERROR: Vector Operations invalid operation ", op)
                    else:
                        stall = True
                # Vector Mask Register Operations
                elif re.match(r"C(S\w{2}(VV|VS))", op):
                    rs1 = int(instr[1][2])
                    rs2 = int(instr[2][2])
                    # Check Hazard
                    if (len(vComputeQ) <= self.computeQueueDepth):
                        match op:
                            # !should we use "add" here? what is the cycle needed in S__VS?
                            case "SEQVV" | "SNEVV" | "SGTVV" | "SLTVV" | "SGEVV" | "SLEVV":
                                if (not public_vrbb.isBusy(rs1) and not public_vrbb.isBusy(rs2)):
                                    task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                                    stall_time = 0
                                    stall = False
                                    vComputeQ.append((task, "add", vlr_list[pc], None, None))
                                else:
                                    stall = True
                            case "SEQVS" | "SNEVS" | "SGTVS" | "SLTVS" | "SGEVS" | "SLEVS":
                                if (not public_vrbb.isBusy(rs1) and not public_srbb.isBusy(rs2)):
                                    task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                                    stall_time = 0
                                    stall = False
                                    vComputeQ.append((task, "add", vlr_list[pc], None, None))
                                else:
                                    stall = True
                            case _ :
                                print("Core run - ERROR: Vector Mask Operations invalid operation ", op)
                    else:
                        stall = True
                elif op == "CVM":
                    if (len(scalarQ) <= self.scalarQueueDepth):
                        task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                        stall_time = 0
                        stall = False
                        scalarQ.append((task, "scalar", vlr_list[pc], None, None))
                    else:
                        stall = True
                elif op == "POP":
                    rs = int(instr[1][2])
                    if (len(scalarQ) <= self.scalarQueueDepth and (not public_srbb.isBusy(rs))):
                        public_srbb.Mark(rs)
                        task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                        stall_time = 0
                        stall = False
                        scalarQ.append((task, "scalar", vlr_list[pc], rs, None))
                    else:
                        stall = True
                # Vector Length Register Operations
                elif op == "MTCL" or op == "MFCL":
                    rs = int(instr[1][2])
                    if (len(scalarQ) <= self.scalarQueueDepth and (not public_srbb.isBusy(rs))):
                        if op == "MTCL":
                            task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                            stall_time = 0
                            stall = False
                            scalarQ.append((task, "scalar", vlr_list[pc], None, None))
                        elif op == "MFCL":
                            public_srbb.Mark(rs)
                            task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                            stall_time = 0
                            stall = False
                            scalarQ.append((task, "scalar", vlr_list[pc], rs, None))
                        else:
                            print("Core run - ERROR: Vector Length Mask Operations invalid operation ", op)
                    else:
                        stall = True
                # Memory Access Operations 
                elif re.match(r"C((LV|SV)\w{0,2})", op):
                    rs1 = int(instr[1][2])
                    mems = instr[2]

                    if (len(vDataQ) <= self.dataQueueDepth) and (not stall) and (not public_vrbb.isBusy(rs1)):   
                        # Also check rs1 isBusy since there are two pipelines that WB to rs1
                        # ! Does read mem also need to be busy? A: No
                        if op == "LV" or op == "LVWS" or op == "LVI":
                            public_vrbb.Mark(rs1)
                            task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                            stall_time = 0
                            stall = False
                            vDataQ.append((task, "vmem", vlr_list[pc], rs1, mems))
                        elif op == "SV" or op == "SVWS" or op == "SVI":
                            task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                            stall_time = 0
                            stall = False
                            vDataQ.append((task, "vmem", vlr_list[pc], None, mems))
                        else:
                            print("Core run - ERROR: Vector Memory Access Operations invalid operation ", op)
                    else:
                        stall = True
                elif op == "LS" or op == "SS":
                    rs1 = int(instr[1][2])
                    mems = instr[2]
                    # ! should I also resolve the scalar memory conflict?
                    if (len(scalarQ) <= self.scalarQueueDepth and (not public_srbb.isBusy(rs1))):
                        if op == "LS" :
                            public_srbb.Mark(rs1)
                            task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                            stall_time = 0
                            stall = False
                            scalarQ.append((task, "scalar", vlr_list[pc], rs1, None))
                        elif op == "SS":
                            task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                            stall_time = 0
                            stall = False
                            scalarQ.append((task, "scalar", vlr_list[pc], None, None))
                        else:
                            print("Core run - ERROR: Memory Access Operations LS/SS invalid operation ", op)
                    else:
                        stall = True
                # Scalar Operations
                elif op == "ADD" or op == "SUB" or op == "AND" or op == "OR" or op == "XOR" or op == "SLL" or op == "SRL" or op ==  "SRA":
                    rd = int(instr[1][2])
                    rs1 = int(instr[2][2])
                    rs2 = int(instr[3][2])
                    if (len(scalarQ) <= self.scalarQueueDepth and (not public_srbb.isBusy(rd)) and (not public_srbb.isBusy(rs1)) and (not public_srbb.isBusy(rs2))):
                        public_srbb.Mark(rd)
                        task = {"PC": pc - 1, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                        stall_time = 0
                        stall = False
                        if pc < len(vlr_list):
                            vlr_value = vlr_list[pc]
                        else:
                            # print(f"Error: PC value {pc} exceeds VLR list length {len(vlr_list)}")
                            break
                        scalarQ.append((task, "scalar", vlr_list[pc], rd, None))
                    else:
                        stall = True
                # Control
                elif re.match("B", op):
                    if (len(scalarQ) <= self.scalarQueueDepth):
                        task = {"PC": pc, "Instr": self.state.ID["Instr"], "cycle": 2 + stall_time}
                        stall_time = 0
                        stall = False
                        scalarQ.append((task, "scalar", vlr_list[pc], None, None))
                    else:
                        stall = True
                # Halt
                elif op == "HALT":
                    pass
                else:
                    pass
                    # print("Core - ERROR: Operation invalid ", op)


            # IF stage
            # print("self.state.IF[nop]: " + str(self.state.IF["nop"]) + " | STALL: " + str(stall) + " | halt: " + str(halt))
            if (self.state.IF["nop"] == False and stall == False and halt == False):
                instr = parseInstr(self.IMEM.Read(self.PC))
                # print("PC: ", self.PC, "Instr: ", instr)
                op = instr[0]
                if op == "HALT":
                    halt = True
                    complete_list.append({"PC": self.PC, "Instr": "HALT", "cycle": 1})
                    # self.nextState.ID["Instr"] = self.state.ID["Instr"]
                    # self.nextState.ID["op"] = self.state.ID["op"]
                    # self.state.IF["nop"] = True
                    self.nextState.IF["nop"] = True
                    self.nextState.ID["nop"] = True
                else:
                    self.nextState.ID = {"nop": False, "Instr": self.IMEM.Read(self.PC), "op": op, "PC": self.PC}
                    self.PC = self.PC + 1
                    self.nextState.IF["PC"] = self.PC
                    self.nextState.ID["nop"] = False
            
            if stall:
                stall_time += 1

            self.state = self.nextState
            total_cycle += 1

            if (halt and public_backend.isClean() and (len(vDataQ) == 0) and (len(vComputeQ) == 0) and (len(scalarQ) == 0)):
                return total_cycle
            # if (halt and public_backend.isClean() and (len(vDataQ) == 0) and (len(vComputeQ) == 0) and (len(scalarQ) == 0) or total_cycle > 600):
            #     return total_cycle

    def dumpregs(self, iodir):
        for rf in self.RFs.values():
            rf.dump(iodir)

if __name__ == "__main__":
    #parse arguments for input file location
    parser = argparse.ArgumentParser(description='Vector Core Functional Simulator')
    parser.add_argument('--iodir', default="", type=str, help='Path to the folder containing the input files - instructions and data.')
    args = parser.parse_args()

    iodir = os.path.abspath(args.iodir)
    print("IO Directory:", iodir)

    # Parse Config
    config = Config(iodir)

    # # Parse IMEM
    imem = IMEM(iodir)

    ''' 
    for str in imem.instructions:
        parseInstr(str)
    '''

    # Parse SMEM
    sdmem = DMEM("SDMEM", iodir, 13) # 32 KB is 2^15 bytes = 2^13 K 32-bit words.
    # Parse VMEM
    vdmem = DMEM("VDMEM", iodir, 17) # 512 KB is 2^19 bytes = 2^17 K 32-bit words. 

    # Read VLR
    try:
        vlr_filepath = os.path.abspath(os.path.join(iodir, "vlr.txt"))
        with open(vlr_filepath, 'r') as insf:
            vlr_list = [int(vlr.split('#')[0].strip()) for vlr in insf.readlines() if not (vlr.startswith('#') or vlr.strip() == '')]
        print("VLR loaded from file:", vlr_filepath)
        # print("VLR:", vlr_list)
        # print("VLR length:", len(vlr_list))
    except:
        print("VLR - ERROR: Couldn't open file in path:", vlr_filepath)
        raise

    # Initialize busyboards
    public_srbb = BusyBoard(8)
    public_vrbb = BusyBoard(8)
    public_vmembb = MemoryBank(bankSize=int(config.parameters["vdmNumBanks"]), busyTime=int(config.parameters["vlsPipelineDepth"]))

    # Initialize backend
    public_backend = Backend(config=config)
    # Create Vector Core
    vcore = Core(imem, sdmem, vdmem, config)

    # Run Core
    total_cycle = vcore.run()   
    vcore.dumpregs(iodir)

    sdmem.dump()
    vdmem.dump()

    # sort the final instructions with PC in ascending order
    sorted_lst = sorted(complete_list, key=lambda x: x["PC"])
    output_str = ""
    for d in sorted_lst:
        output_str += f"{d['Instr']} latency: {d['cycle']}\n"
    output_str = copy_file_contents(iodir=os.path.abspath(os.path.join(iodir, "Config.txt")), output_str=output_str) # Put the total cycle to the front
    output_str = "Total cycle: " + str(total_cycle) + "\n" + output_str
    
    # output instruction level latency
    # Redirect stdout to a text file
    with open(iodir + '/output_results.txt', 'w') as file:
        sys.stdout = file

        # Now, all print statements will be directed to the file instead of the console
        print("srbb = \n", public_srbb.element)
        print("\nvrbb = \n", public_vrbb.element)
        print("\npublic_backend = \n")
        print("\nAddPipeline = \n", public_backend.AddPipeline)
        print("\nMulPipeline = \n", public_backend.MulPipeline)
        print("\nDivPipeline = \n", public_backend.DivPipeline)
        print("\nScalarPipeline = \n", public_backend.ScalarPipeline)
        print("\nVmemPipeline = \n", public_backend.VmemPipeline)
        print("\nbankBusyCount = \n", public_vmembb.bankBusyCount)
        print("\nbankMemoryAddr = \n", public_vmembb.bankMemoryAddr)
        print("Total cycle: " + str(total_cycle))

        # Write output instruction level latency into another file
        with open(iodir + "/instruction_latency.txt", "w") as vlr_file:
            vlr_file.write(output_str)

    # Reset stdout to its original value
    sys.stdout = sys.__stdout__

    print("Output has been written to file.")


    # THE END