# SCCPU:
/SCCPU/Second project for the Computer Architecture in 2022 using graphics using c/c++
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ⚡ Single-Cycle CPU in C (with GUI)

This project implements a **Single-Cycle CPU simulator** written entirely in **C language**, featuring an **interactive graphical interface**.  
It is designed to execute the **machine code** produced by the assembler and visually demonstrate how each instruction affects the CPU’s internal state.

---

## 🧠 Overview
The simulator mimics the behavior of a **single-cycle processor**, where each instruction — from fetch to write-back — is executed in a single clock cycle.  
With its **graphical interface**, users can observe how data moves through components like the ALU, registers, and memory in real-time.

---

## 🎨 Graphical Interface Features
- Visual representation of:
  - **Program Counter (PC)**
  - **Instruction Memory**
  - **Register File**
  - **ALU Operations**
  - **Data Memory**
- Step-by-step instruction execution  
- Real-time highlighting of active components  
- Memory and register content updates after each clock cycle  
- Optional **auto-run** mode for continuous simulation

---

## ⚙️ Technical Details
- **Language:** C  
- **Graphics Library:** (e.g., `SDL2` / `GTK` / `OpenGL` — *replace with what you used*)  
- **Instruction Set:** Compatible with the assembler’s output format  
- **Execution Mode:** Single-cycle (each instruction completes in one clock tick)

---

## 🧱 Example Workflow
1. Write your assembly program and save it as `program.as`
2. Use the **assembler** to generate machine code:
   ```bash
   ./assembler program.as




![Screenshot (1066)](https://user-images.githubusercontent.com/83461302/184843348-51ac2bd1-dfc3-4104-9c8c-2805359c98bf.png)



