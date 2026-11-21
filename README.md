# GAMEX

### A Tic-Tac-Toe AI Powered by a Depth-Limited Minimax Engine

> **Project Topic:** Develop a generic two-player zero-sum game engine, test it on Tic-Tac-Toe, and implement configurable-depth Minimax search. The application displays the game-tree statistics: number of nodes explored, maximum depth, utility value, and best move.

GAMEX is an interactive Python demonstration of game-playing artificial intelligence. It combines a generic minimax search engine with a polished Tkinter interface, allowing users to play Tic-Tac-Toe against an AI and inspect the search process in real time.

The project demonstrates core AI concepts including:

- Depth-limited minimax search
- Maximizing and minimizing players
- Utility and heuristic evaluation
- Search node exploration
- Terminal-state detection
- Interactive game-state visualization

---

## Features

- Play as **X** against an AI-controlled **O**
- Adjustable AI search depth from **1 to 9**
- Live game status and score tracking
- Position analysis with:
  - Explored nodes
  - Maximum search depth
  - AI utility value
  - Recommended move
- Clean monochrome desktop interface
- Resettable rounds
- Automated minimax unit tests

---

## Requirements

- Python 3.9 or newer
- Tkinter, included with standard Python installations on Windows

No third-party runtime packages are required.

---

## Running the Application

### Windows

Double-click:

```text
run_game.bat
```

### Command line

From the project directory, run:

```bash
python -m src.app
```

---

## How to Play

1. Launch GAMEX.
2. Select an empty square to place `X`.
3. The AI evaluates the resulting position and places `O`.
4. Complete three marks in a row, column, or diagonal to win.
5. Use **New game** to start another round.

The search-depth control changes how many moves ahead the AI examines. Higher depths produce stronger decisions but require more computation.

---

## Game Analysis

GAMEX exposes the information produced during each AI search:

| Metric | Description |
| --- | --- |
| Nodes | Number of positions explored |
| Max Depth | Deepest level reached by the search |
| Utility | Position value from the AI player's perspective |
| Best Move | Recommended row and column |

Use **Analyze position** to evaluate the current board without making an AI move.

---

## Project Structure

```text
GAMEX-ai-project/
├── src/
│   ├── app.py       # Tkinter user interface
│   ├── engine.py    # Generic minimax implementation
│   └── ttt.py       # Tic-Tac-Toe game-state implementation
├── tests/
│   └── test_minimax.py
├── run_game.bat
├── run_tests.bat
└── README.md
```

### Key Components

- **`engine.py`** implements the reusable depth-limited minimax algorithm.
- **`ttt.py`** adapts Tic-Tac-Toe to the generic game-state interface.
- **`app.py`** manages the interface, player interaction, scoring, and AI searches.
- **`test_minimax.py`** verifies move selection and evaluation behavior.

---

## Running Tests

### Windows

Run:

```text
run_tests.bat
```

### Command line

```bash
python -m unittest discover -s tests -v
```

---

## Minimax Overview

Minimax models a turn-based game as a search tree. GAMEX uses alpha-beta pruning to skip branches that cannot affect the result. The AI assumes:

- Its turn attempts to **maximize** the utility value.
- The opponent's turn attempts to **minimize** that value.
- The search stops at a terminal state or the configured depth limit.
- Heuristic evaluation estimates board quality for positions beyond the search depth.

The engine remains separate from the Tic-Tac-Toe implementation, demonstrating a reusable AI search layer for other turn-based games.

---

## Building a Windows Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Then build GAMEX:

```bash
pyinstaller --onefile --windowed --name GAMEX src/app.py
```

The executable is generated in the `dist` directory.

---

## Educational Context

GAMEX is designed as an AI project demonstration for explaining how search-based systems make decisions in constrained environments. It is small enough to inspect and modify, while still illustrating meaningful concepts used in more complex game engines.
