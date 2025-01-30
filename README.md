# 🚀 Timing Simulator for Vector-MIPS5 Architecture
## Author: Anuj Attri
**TimingSim** is a Python-based timing simulator designed to analyze the execution efficiency of a VMIPS-like vector microarchitecture. The simulator models instruction processing times without actual data movements, enabling performance analysis of various assembly programs.

---

## 📌 Features

- **Functional Simulator**: Ensures correctness of VMIPS-like vector assembly programs.
- **Timing Simulator**: Evaluates instruction execution time under microarchitectural constraints.
- **Performance Analysis**: Benchmarks **dot product**, **fully connected layers**, and **convolution operations**.
- **Memory Conflict Optimization**: Reduces vector memory bank conflicts, improving efficiency.
- **Configurable Architecture**: Supports adjustable **dispatch queues, vector memory settings, and compute pipeline depths**.

---

## 📂 Project Structure
```
TimingSim/  
├── control_operations/            # Vector control instructions  
├── conv/                          # Convolution operations  
├── dot_product/                   # Dot product computations  
├── fully_connect/                 # Fully connected layer operations  
├── shuffle_operations/             # Vector shuffle operations  
├── timing_simulator/               # Timing simulation logic  
├── vector_len_operations/          # Vector length computations  
├── aa11527_funcsimulator.py        # Functional simulator script  
├── aa11527_timingsimulator.py      # Timing simulator script  
├── Config.txt                      # Configuration settings  
├── README.md                       # Project documentation  
├── LICENSE                         # License file  
├── func_sim_description.pdf        # Functional simulator description  
├── generate_vlr.py                 # Script to generate vector length register  
└── vlr.txt                         # Vector length register file  
```

---
## ⚙️ Installation & Usage

### 🔧 Prerequisites
- **Python 3.11+**
- Standard Python libraries (**sys, os, collections, re**)

### 📥 Clone Repository
```
git clone https://github.com/Anuj-Attri/TimingSim.git
cd TimingSim
```

### ▶️ Running the Functional Simulator
```
python3 aa11527_funcsimulator.py --iodir <path/to/input/output/directory>
```

### ▶️ Running the Timing Simulator
```
python3 aa11527_timingsimulator.py --iodir <path/to/input/output/directory>
```

## 📊 Performance Analysis
The simulator evaluates various microarchitecture configurations using dot product, fully connected layer, and convolution operations. Key performance metrics include:

- Instruction cycle counts
- Execution bottleneck identification
- Effect of memory bank conflicts
  
### 🔥 Optimizations Implemented
✔️ Lazy Memory Initialization - Reduces startup time & memory usage.\
✔️ Regex-Based Instruction Parsing - Speeds up instruction decoding.\
✔️ Busy Board for Resource Tracking - Resolves RAW & WAW hazards.\
✔️ Separate Instruction Queues - Enhances parallelism in execution.\
✔️ Memory Bank Conflict Resolution - Optimizes vector memory accesses.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙌 Acknowledgments

This project is developed as part of ECE-GY-9413 - Timing Simulation for VMIPS at NYU Tandon School of Engineering.

🔗 [Project Report](https://github.com/Anuj-Attri/TimingSim/blob/master/timing_simulator/aa11527_final_report.pdf)

⭐ Star this repository if you found it helpful! 🚀
