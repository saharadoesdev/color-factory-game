# Color Factory Game

This is my final project for SEO's Tech Developer First Year Academy program.

## Running the Game

### macOS

1.  **Open Terminal:** You can find it in `Applications/Utilities/Terminal`.
2.  **Run the following command to make the script executable:**
    ```bash
    chmod +x run_game.command
    ```
    You only need to do this once.
3.  **Double-click `run_game.command`** to start the game.

    **Note:** If you see a security warning from macOS, you may need to run the following command in the Terminal to allow the script to run:
    ```bash
    xattr -d com.apple.quarantine run_game.command
    ```

### Windows

1.  **Double-click `run_game.bat`** to start the game.

### Manual Setup (All Platforms)

If you prefer to set up the game manually, follow these steps:

1.  **Open a terminal or command prompt.**
2.  **Navigate to the project directory:**
    ```bash
    cd /path/to/color-factory-game
    ```
3.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```
4.  **Activate the virtual environment:**
    -   **macOS/Linux:** `source venv/bin/activate`
    -   **Windows:** `venv\Scripts\activate`
5.  **Install dependencies:**
    ```bash
    pip install pygame
    ```
6.  **Run the game:**
    ```bash
    python3 main.py
    ```
