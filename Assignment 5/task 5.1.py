# task 5.1.py - Secure Login System with Username and Password Validation
import hashlib
import secrets
import json
import os
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple

class LoginSystem:
    """
    Secure login system with password hashing, session management, and rate limiting.
    """
    
    def __init__(self, users_file: str = "users.json", session_file: str = "sessions.json"):
        self.users_file = users_file
        self.session_file = session_file
        self.sessions: Dict[str, Dict] = {}
        self.login_attempts: Dict[str, list] = {}
        self.max_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
        
        # Load existing data
        self.load_users()
        self.load_sessions()
    
    def load_users(self):
        """Load users from file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self):
        """Save users to file with restricted permissions"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
        # Set file permissions to read/write for owner only (Unix)
        if os.name != 'nt':  # Not Windows
            os.chmod(self.users_file, 0o600)
    
    def load_sessions(self):
        """Load sessions from file"""
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                self.sessions = json.load(f)
    
    def save_sessions(self):
        """Save sessions to file"""
        with open(self.session_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
        if os.name != 'nt':
            os.chmod(self.session_file, 0o600)
    
    def validate_username(self, username: str) -> Tuple[bool, Optional[str]]:
        """
        Validate username format.
        Returns (is_valid, error_message)
        """
        if not username:
            return False, "Username cannot be empty"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 20:
            return False, "Username must be at most 20 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, None
    
    def validate_password(self, password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password strength.
        Returns (is_valid, error_message)
        """
        if not password:
            return False, "Password cannot be empty"
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if len(password) > 128:
            return False, "Password must be at most 128 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        return True, None
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """
        Hash password using PBKDF2 with random salt.
        Returns (hashed_password, salt) tuple.
        """
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Use PBKDF2 for password hashing
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 100k iterations
        )
        hashed = key.hex()
        return hashed, salt
    
    def verify_password(self, password: str, hashed: str, salt: str) -> bool:
        """Verify password against stored hash using constant-time comparison"""
        new_hash, _ = self.hash_password(password, salt)
        return secrets.compare_digest(new_hash, hashed)
    
    def register_user(self, username: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Register a new user with validation.
        Returns (success, message)
        """
        # Validate username
        valid, error = self.validate_username(username)
        if not valid:
            return False, error
        
        # Validate password
        valid, error = self.validate_password(password)
        if not valid:
            return False, error
        
        # Check if user already exists
        if username in self.users:
            return False, "Username already exists"
        
        # Hash password
        hashed, salt = self.hash_password(password)
        
        # Store user
        self.users[username] = {
            'hashed_password': hashed,
            'salt': salt,
            'created_at': datetime.now().isoformat()
        }
        self.save_users()
        return True, "User registered successfully"
    
    def check_rate_limit(self, username: str) -> Tuple[bool, Optional[str]]:
        """
        Check if user is rate limited.
        Returns (is_allowed, error_message)
        """
        if username not in self.login_attempts:
            return True, None
        
        attempts = self.login_attempts[username]
        now = datetime.now()
        
        # Remove old attempts
        attempts = [t for t in attempts if now - datetime.fromisoformat(t) < self.lockout_duration]
        self.login_attempts[username] = attempts
        
        if len(attempts) >= self.max_attempts:
            return False, f"Account locked. Try again after {self.lockout_duration}"
        
        return True, None
    
    def record_failed_attempt(self, username: str):
        """Record a failed login attempt"""
        if username not in self.login_attempts:
            self.login_attempts[username] = []
        self.login_attempts[username].append(datetime.now().isoformat())
    
    def create_session(self, username: str) -> str:
        """Create a new session token"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)
        
        self.sessions[token] = {
            'username': username,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat()
        }
        self.save_sessions()
        return token
    
    def validate_session(self, token: str) -> Optional[str]:
        """Validate session token and return username if valid"""
        if token not in self.sessions:
            return None
        
        session = self.sessions[token]
        expires_at = datetime.fromisoformat(session['expires_at'])
        
        if datetime.now() > expires_at:
            del self.sessions[token]
            self.save_sessions()
            return None
        
        return session['username']
    
    def login(self, username: str, password: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Attempt to login with timing attack protection.
        Returns (success, message, session_token)
        """
        # Validate input
        valid, error = self.validate_username(username)
        if not valid:
            return False, error, None
        
        # Check rate limiting
        allowed, error = self.check_rate_limit(username)
        if not allowed:
            return False, error, None
        
        # Use a dummy hash for non-existent users to prevent timing attacks
        if username not in self.users:
            # Perform dummy verification to maintain consistent timing
            dummy_hash = "0" * 64
            dummy_salt = "0" * 32
            self.verify_password(password, dummy_hash, dummy_salt)
            self.record_failed_attempt(username)
            return False, "Invalid username or password", None
        
        user = self.users[username]
        
        # Verify password
        if not self.verify_password(password, user['hashed_password'], user['salt']):
            self.record_failed_attempt(username)
            return False, "Invalid username or password", None
        
        # Clear failed attempts on successful login
        if username in self.login_attempts:
            del self.login_attempts[username]
        
        # Create session
        token = self.create_session(username)
        return True, "Login successful", token
    
    def logout(self, token: str) -> bool:
        """Logout and invalidate session"""
        if token in self.sessions:
            del self.sessions[token]
            self.save_sessions()
            return True
        return False


# Example usage and testing
if __name__ == "__main__":
    # Initialize login system
    login_system = LoginSystem()
    
    # Example: Register a user
    # In production, credentials should come from user input or secure sources
    # NEVER hardcode credentials in production code!
    
    print("=== Login System Demo ===")
    print("\n1. Register a new user:")
    
    # Get credentials from user input (secure approach)
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    success, message = login_system.register_user(username, password)
    print(f"Registration: {message}")
    
    if success:
        print("\n2. Login test:")
        login_username = input("Enter username: ").strip()
        login_password = input("Enter password: ").strip()
        
        success, message, token = login_system.login(login_username, login_password)
        print(f"Login: {message}")
        
        if success:
            print(f"Session token: {token}")
            
            # Validate session
            username = login_system.validate_session(token)
            if username:
                print(f"Session valid for user: {username}")
            
            # Logout
            login_system.logout(token)
            print("Logged out successfully")