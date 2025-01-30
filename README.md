# 🚀 Timing Simulator for VMIPS Architecture
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

TimingSim/ │── control_operations/ # Vector control instructions │── conv/ # Convolution operations │── dot_product/ # Dot product computations │── fully_connect/ # Fully connected layer operations │── shuffle_operations/ # Vector shuffle operations │── timing_simulator/ # Timing simulation logic │── vector_len_operations/ # Vector length computations │── aa11527_funcsimulator.py # Functional simulator script │── aa11527_timingsimulator.py # Timing simulator script │── Config.txt # Configuration settings │── README.md # Project documentation │── LICENSE # License file │── func_sim_description.pdf # Functional simulator description │── generate_vlr.py # Script to generate vector length register │── vlr.txt # Vector length register file

---
# How to run
To run the functional simulator, use command *python aa11527_funcsimulator.py --iodir <path/to/the/directory/containing/for/your/test>*. You can also run the *aa11527_functional_simulator.bat* to run all test functions.

To run performance analysis with the timing simulator, use *python aa11527_timingsimulator.py --iodir <path/to/the/directory/containing/for/your/test>*.
