# Mafia:
Programming basics project for the first term at Esfahan University in 2019.



# **Multiplayer Role-Playing Console Game** 🎮🧛‍♂️

**Languages & Tools:** C++, Windows Console, ANSI Coloring, Standard Template Library (STL)

---

## **Overview**
This project is a **multiplayer, console-based role-playing game** inspired by **Werewolf / Mafia**, where each player has a unique role with special powers. The game dynamically handles **day/night cycles**, **voting**, and **role-specific abilities**, providing an immersive gameplay experience directly in the console.  

Players can interact via commands to **attack, save, love, or perform unique role actions**, while the game automatically tracks the status of each character and determines victory conditions.

---

## **Gameplay Features**
- **Roles Implemented:**
  - WOLFMAN  
  - KILLER  
  - FIREMAN  
  - ANGLE (Guardian Angel)  
  - LOVE (Cupid / Love Angle)  
  - FACTION (Faction Member)  
  - HUNTER  
  - VILLAGER
- **Game Mechanics:**
  - Day/Night cycles with different roles activating in their turn.
  - **Voting system** to eliminate players.
  - **Partner system** for Love Angle (linked fate of players).
  - **Fire / Oil mechanic** for FIREMAN interactions.
  - **Faction mechanics** for team-based gameplay.
  - **Real-time status display** using console colors.
- **Interactive Commands:**
  - `Eat`, `Kill`, `Oil`, `Burn`, `Love`, `Save`, `Shoot`, `Cult`, `Vote`
  - Each role can perform a **single action per day**, tracked automatically.

---

## **Technical Details**
- Written in **C++** using **structs** and **enums** for player roles and statuses.
- Dynamic memory allocation to handle an arbitrary number of players.
- Uses **Windows.h** for console text coloring to enhance visual feedback.
- Implements **functions for role actions**, **voting**, and **win condition checks**.
- Supports **randomized role assignment** for varied gameplay every session.

---

## **Game Flow**
1. Input number of players and their names.
2. Assign roles randomly, including six key roles and the rest as villagers or werewolves.
3. Loop through **daily command input**, allowing each role to perform actions:
   - Kill, save, set on fire, link lovers, shoot, join faction, vote, etc.
4. After each day, check for **win conditions**:
   - Faction wins if only faction members are alive.
   - Werewolves win if their count equals remaining alive and no killers/firemen remain.
   - Villagers win if all enemies (WOLFMAN, KILLER, FIREMAN) are eliminated.
5. Game continues until **a winning condition is met**.

---

## **Console UI**
- Color-coded console output:
  - **Green** = Alive  
  - **Red** = Dead  
  - **Yellow** = Oily status (vulnerable to fire)
- Columns displayed:
  - Name | Role | Status | Is Oily | Partner
- Real-time updates after every command.

---

## **Skills & Learning Outcomes**
- **C++ advanced programming**: enums, structs, pointers, dynamic memory.
- **Game design and logic**: turn-based mechanics, role interactions.
- **Console UI design**: colored outputs, formatted tables.
- **Problem-solving**: handling complex conditions and multi-role interactions.

---

## **Running the Game**
1. Compile the code using a **C++ compiler on Windows**:
   ```bash
   g++ -o RoleGame main.cpp
