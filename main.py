import random
import string
import secrets
import pyperclip
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self):
        self.lower = string.ascii_lowercase
        self.upper = string.ascii_uppercase
        self.numbers = string.digits
        self.symbols = string.punctuation
        self.history = []
        
    def welcome(self):
        """Display welcome message"""
        print("\n" + "=" * 50)
        print("|{:^48}|".format("Welcome to the Advanced Password Generator"))
        print("=" * 50)
    
    def goodbye(self):
        """Display goodbye message"""
        print("\n" + "=" * 50)
        print("|{:^48}|".format("Thanks for using the Password Generator"))
        print("=" * 50)
    
    def get_password_length(self):
        """Get password length from user with validation"""
        while True:
            try:
                length = input("\nEnter the length of password (minimum 8): ")
                length = int(length)
                if length < 8:
                    print("Password must be at least 8 characters long.")
                    continue
                return length
            except ValueError:
                print("Please enter a valid number.")
    
    def get_character_preferences(self):
        """Get user preferences for character types"""
        preferences = {}
        
        print("\nPassword character options:")
        preferences["lower"] = self.get_yes_no("Include lowercase letters (a-z)? (y/n): ")
        preferences["upper"] = self.get_yes_no("Include uppercase letters (A-Z)? (y/n): ")
        preferences["numbers"] = self.get_yes_no("Include numbers (0-9)? (y/n): ")
        preferences["symbols"] = self.get_yes_no("Include symbols (!@#$%)? (y/n): ")
        
        # Ensure at least one character type is selected
        if not any(preferences.values()):
            print("You must select at least one character type. Using all types.")
            preferences = {"lower": True, "upper": True, "numbers": True, "symbols": True}
            
        return preferences
    
    def get_yes_no(self, prompt):
        """Get a yes or no response from the user"""
        while True:
            response = input(prompt).lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'.")
    
    def generate_character_pool(self, preferences):
        """Generate character pool based on user preferences"""
        all_characters = ""
        required_chars = []
        
        if preferences["lower"]:
            all_characters += self.lower
            required_chars.append(secrets.choice(self.lower))
        
        if preferences["upper"]:
            all_characters += self.upper
            required_chars.append(secrets.choice(self.upper))
        
        if preferences["numbers"]:
            all_characters += self.numbers
            required_chars.append(secrets.choice(self.numbers))
        
        if preferences["symbols"]:
            all_characters += self.symbols
            required_chars.append(secrets.choice(self.symbols))
            
        return all_characters, required_chars
    
    def generate_password(self, length, preferences):
        """Generate a password with the given specifications"""
        # Get character pool and required characters
        all_characters, required_chars = self.generate_character_pool(preferences)
        
        # Generate the rest of the password
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [secrets.choice(all_characters) for _ in range(remaining_length)]
        
        # Shuffle the password characters
        secrets.SystemRandom().shuffle(password_chars)
        
        # Join into a string
        password = ''.join(password_chars)
        
        # Add to history
        self.history.append(password)
        
        return password
    
    def evaluate_strength(self, password):
        """Evaluate password strength"""
        length = len(password)
        has_lower = any(c in self.lower for c in password)
        has_upper = any(c in self.upper for c in password)
        has_number = any(c in self.numbers for c in password)
        has_symbol = any(c in self.symbols for c in password)
        
        # Calculate diversity score
        diversity = sum([has_lower, has_upper, has_number, has_symbol])
        
        if length >= 12 and diversity >= 4:
            return "Very Strong"
        elif length >= 10 and diversity >= 3:
            return "Strong"
        elif length >= 8 and diversity >= 2:
            return "Moderate"
        else:
            return "Weak"
    
    def copy_to_clipboard(self, password):
        """Copy password to clipboard"""
        try:
            pyperclip.copy(password)
            return True
        except:
            return False
    
    def save_to_file(self, password):
        """Save password to file"""
        try:
            filename = "passwords.txt"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create the file if it doesn't exist
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                    f.write("# Password Generator History\n\n")
            
            # Append the password
            with open(filename, "a") as f:
                f.write(f"{timestamp}: {password}\n")
                
            return True, filename
        except:
            return False, ""
    
    def display_menu(self):
        """Display the main menu options"""
        print("\nOptions:")
        print("1. Generate a new password")
        print("2. View password history")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        return choice
    
    def run(self):
        """Run the password generator program"""
        self.welcome()
        
        while True:
            choice = self.display_menu()
            
            if choice == "1":
                # Get password specifications
                length = self.get_password_length()
                preferences = self.get_character_preferences()
                
                # Generate password
                password = self.generate_password(length, preferences)
                strength = self.evaluate_strength(password)
                
                # Display the password and its strength
                print("\n" + "-" * 50)
                print(f"Your password: {password}")
                print(f"Strength: {strength}")
                print("-" * 50)
                
                # Additional options
                if self.get_yes_no("\nCopy to clipboard? (y/n): "):
                    success = self.copy_to_clipboard(password)
                    if success:
                        print("Password copied to clipboard successfully!")
                    else:
                        print("Could not copy to clipboard. Pyperclip module may not be installed correctly.")
                
                if self.get_yes_no("Save to file? (y/n): "):
                    success, filename = self.save_to_file(password)
                    if success:
                        print(f"Password saved to {filename}!")
                    else:
                        print("Could not save to file.")
            
            elif choice == "2":
                # Display password history
                if not self.history:
                    print("\nNo passwords generated yet.")
                else:
                    print("\nPassword History:")
                    for i, password in enumerate(self.history, 1):
                        print(f"{i}. {password} - {self.evaluate_strength(password)}")
            
            elif choice == "3":
                self.goodbye()
                break
            
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.run()