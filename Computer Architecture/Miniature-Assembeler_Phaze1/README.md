# Miniature-Assembeler:
Computer Architecture project for the fourth term at Esfahan University in 2022 using C.


# 🧠 Simple Assembler in C

This project is a **simple assembler** written in **C language**.  
It reads an assembly source file (`.as`), builds a **symbol table** for labels, and converts each instruction into **machine code** stored in a `.m` file.

---

## ⚙️ Features
- Two-pass assembler:
  - **Pass 1:** Builds the label symbol table  
  - **Pass 2:** Generates machine code for each instruction
- Supports **R-type**, **I-type**, and **J-type** instruction formats  
- Handles the **`.fill`** directive for data memory initialization  
- Outputs machine code in **decimal format**  
- Includes basic **error checking** for invalid syntax or undefined labels

---

## 🧩 Main Functions
| Function | Description |
|-----------|-------------|
| `ISLABLE()` | Detects label definitions in the source code |
| `CREATTABLE()` | Builds the symbol table containing label names and addresses |
| `PRINTTABLE()` | Displays all label–address pairs |
| `GETInsInDecimal()` | Converts a binary instruction (array of bits) into its decimal value |
| `main()` | Controls file reading, parsing, translation, and output generation |

---

## 📂 Input & Output
| File | Description |
|------|--------------|
| `program.as` | Input assembly file |
| `program.m` | Output file containing decimal machine code |

---

## 🧱 Example Usage
```bash
gcc assembler.c -o assembler
./assembler program.as

