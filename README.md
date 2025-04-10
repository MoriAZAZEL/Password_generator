How It Works

Initialization: Sets up character sets and an empty history list.
Menu System: Offers three options - generate password, view history, or exit.
Password Generation Process:

Gets length and character preferences (lowercase, uppercase, numbers, symbols)
Creates a character pool based on preferences
Ensures at least one character from each selected type is included
Generates remaining characters randomly
Securely shuffles all characters


Additional Features:

Password strength evaluation based on length and character diversity
Clipboard integration (requires pyperclip module)
Password history tracking
File saving capability


User Input: All user inputs are validated to prevent crashes and ensure valid options.
