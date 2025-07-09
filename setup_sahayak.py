#!/usr/bin/env python3
"""
🚀 Sahayak AI Platform Automated Setup Script
This script automates the complete setup process for the Sahayak platform
"""

import os
import sys
import subprocess
import json
import urllib.request
import platform
from pathlib import Path
import shutil

class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_step(step_num, text):
    """Print formatted step"""
    print(f"{Colors.BOLD}{Colors.GREEN}Step {step_num}:{Colors.END} {Colors.WHITE}{text}{Colors.END}")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def run_command(cmd, check=True, capture_output=False):
    """Run shell command with error handling"""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, check=check, 
                                 capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=check)
            return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {cmd}")
        if capture_output and e.stdout:
            print(f"Output: {e.stdout}")
        if capture_output and e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_system_requirements():
    """Check if system has all required tools"""
    print_step(1, "Checking System Requirements")
    
    requirements = {
        'python': {'cmd': 'python --version', 'min_version': '3.9'},
        'node': {'cmd': 'node --version', 'min_version': '18.0'},
        'npm': {'cmd': 'npm --version', 'min_version': '8.0'},
        'git': {'cmd': 'git --version', 'min_version': '2.0'}
    }
    
    missing = []
    
    for tool, info in requirements.items():
        result = run_command(info['cmd'], check=False, capture_output=True)
        if result:
            print_success(f"{tool.upper()} is installed")
        else:
            missing.append(tool)
            print_error(f"{tool.upper()} is not installed")
    
    if missing:
        print_error("Missing requirements. Please install:")
        for tool in missing:
            if tool == 'python':
                print("  - Python 3.9+: https://python.org/downloads/")
            elif tool == 'node':
                print("  - Node.js 18+: https://nodejs.org/")
            elif tool == 'npm':
                print("  - npm (comes with Node.js)")
            elif tool == 'git':
                print("  - Git: https://git-scm.com/downloads")
        return False
    
    return True

def setup_project_structure():
    """Set up the project directory structure"""
    print_step(2, "Setting up Project Structure")
    
    # Create main directories
    directories = [
        'sahayak-frontend',
        'sahayak-backend',
        'docs',
        'scripts',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print_success(f"Created directory: {directory}")

def setup_backend():
    """Set up the backend environment"""
    print_step(3, "Setting up Backend Environment")
    
    backend_dir = Path('sahayak-backend')
    os.chdir(backend_dir)
    
    # Create virtual environment
    print_info("Creating Python virtual environment...")
    if platform.system() == "Windows":
        run_command('python -m venv venv')
        activate_cmd = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
    else:
        run_command('python3 -m venv venv')
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
    
    print_success("Virtual environment created")
    
    # Install dependencies
    print_info("Installing Python dependencies...")
    run_command(f'{pip_cmd} install --upgrade pip')
    
    if Path('requirements.txt').exists():
        run_command(f'{pip_cmd} install -r requirements.txt')
        print_success("Backend dependencies installed")
    else:
        print_warning("requirements.txt not found, skipping dependency installation")
    
    os.chdir('..')

def setup_frontend():
    """Set up the frontend environment"""
    print_step(4, "Setting up Frontend Environment")
    
    frontend_dir = Path('sahayak-frontend')
    
    if not frontend_dir.exists():
        print_info("Frontend directory not found, creating React app...")
        run_command('npx create-react-app sahayak-frontend --template typescript')
    
    os.chdir(frontend_dir)
    
    # Install dependencies
    print_info("Installing Node.js dependencies...")
    if Path('package.json').exists():
        run_command('npm install')
        print_success("Frontend dependencies installed")
    else:
        print_warning("package.json not found, skipping dependency installation")
    
    os.chdir('..')

def create_environment_files():
    """Create environment configuration files"""
    print_step(5, "Creating Environment Configuration Files")
    
    # Backend .env file
    backend_env = """# ================================
# SAHAYAK AI PLATFORM CONFIGURATION
# ================================

# ---- APPLICATION SETTINGS ----
APP_NAME=Sahayak AI Platform
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# ---- SECURITY ----
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-too
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# ---- GOOGLE CLOUD CONFIGURATION ----
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account.json

# ---- FIREBASE CONFIGURATION ----
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\\nYOUR_PRIVATE_KEY\\n-----END PRIVATE KEY-----\\n"
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id

# ---- AI SERVICE CONFIGURATION ----
OPENAI_API_KEY=your-openai-api-key-optional
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=1000

# ---- DEMO MODE ----
DEMO_MODE=true
MOCK_AI_RESPONSES=true
"""
    
    # Frontend .env file
    frontend_env = """# ================================
# SAHAYAK FRONTEND CONFIGURATION
# ================================

# ---- FIREBASE CONFIGURATION ----
VITE_FIREBASE_API_KEY=your-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789012
VITE_FIREBASE_APP_ID=1:123456789012:web:abcdef123456789

# ---- API CONFIGURATION ----
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# ---- APPLICATION SETTINGS ----
VITE_APP_NAME=Sahayak
VITE_APP_VERSION=1.0.0
VITE_ENVIRONMENT=development

# ---- DEMO MODE ----
VITE_DEMO_MODE=true
VITE_SHOW_DEMO_DATA=true
"""
    
    # Write backend .env
    backend_env_path = Path('sahayak-backend/.env')
    if not backend_env_path.exists():
        with open(backend_env_path, 'w') as f:
            f.write(backend_env)
        print_success("Created backend .env file")
    else:
        print_info("Backend .env file already exists")
    
    # Write frontend .env
    frontend_env_path = Path('sahayak-frontend/.env')
    if not frontend_env_path.exists():
        with open(frontend_env_path, 'w') as f:
            f.write(frontend_env)
        print_success("Created frontend .env file")
    else:
        print_info("Frontend .env file already exists")

def create_startup_scripts():
    """Create convenient startup scripts"""
    print_step(6, "Creating Startup Scripts")
    
    scripts_dir = Path('scripts')
    scripts_dir.mkdir(exist_ok=True)
    
    if platform.system() == "Windows":
        # Windows batch files
        start_backend = """@echo off
echo Starting Sahayak Backend...
cd sahayak-backend
call venv\\Scripts\\activate
python -m uvicorn main:app --reload --port 8000
pause
"""
        
        start_frontend = """@echo off
echo Starting Sahayak Frontend...
cd sahayak-frontend
npm run dev
pause
"""
        
        start_all = """@echo off
echo Starting Sahayak Platform...
start "Backend" cmd /c scripts\\start-backend.bat
timeout /t 5
start "Frontend" cmd /c scripts\\start-frontend.bat
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
pause
"""
        
        with open('scripts/start-backend.bat', 'w') as f:
            f.write(start_backend)
        with open('scripts/start-frontend.bat', 'w') as f:
            f.write(start_frontend)
        with open('scripts/start-all.bat', 'w') as f:
            f.write(start_all)
        
        print_success("Created Windows startup scripts")
    
    else:
        # Unix shell scripts
        start_backend = """#!/bin/bash
echo "Starting Sahayak Backend..."
cd sahayak-backend
source venv/bin/activate
python -m uvicorn main:app --reload --port 8000
"""
        
        start_frontend = """#!/bin/bash
echo "Starting Sahayak Frontend..."
cd sahayak-frontend
npm run dev
"""
        
        start_all = """#!/bin/bash
echo "Starting Sahayak Platform..."
gnome-terminal -- bash scripts/start-backend.sh &
sleep 5
gnome-terminal -- bash scripts/start-frontend.sh &
echo "Both servers are starting..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
"""
        
        with open('scripts/start-backend.sh', 'w') as f:
            f.write(start_backend)
        with open('scripts/start-frontend.sh', 'w') as f:
            f.write(start_frontend)
        with open('scripts/start-all.sh', 'w') as f:
            f.write(start_all)
        
        # Make scripts executable
        run_command('chmod +x scripts/*.sh')
        print_success("Created Unix startup scripts")

def check_google_cloud_cli():
    """Check if Google Cloud CLI is installed"""
    print_step(7, "Checking Google Cloud CLI")
    
    result = run_command('gcloud --version', check=False, capture_output=True)
    if result:
        print_success("Google Cloud CLI is installed")
        return True
    else:
        print_warning("Google Cloud CLI is not installed")
        print_info("To install Google Cloud CLI:")
        print("  1. Visit: https://cloud.google.com/sdk/docs/install")
        print("  2. Follow installation instructions for your OS")
        print("  3. Run: gcloud auth login")
        print("  4. Run: gcloud auth application-default login")
        return False

def create_documentation():
    """Create helpful documentation files"""
    print_step(8, "Creating Documentation")
    
    readme_content = """# 🎓 Sahayak AI Platform

An AI-powered educational assistant for multi-grade classrooms in India.

## 🚀 Quick Start

### Using Startup Scripts
- **Windows**: Run `scripts/start-all.bat`
- **Linux/Mac**: Run `scripts/start-all.sh`

### Manual Start
1. **Backend**: 
   ```bash
   cd sahayak-backend
   source venv/bin/activate  # or venv\\Scripts\\activate on Windows
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend**:
   ```bash
   cd sahayak-frontend
   npm run dev
   ```

## 📱 Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Configuration
- Update `.env` files in both `sahayak-backend` and `sahayak-frontend`
- For AI features, configure Google Cloud credentials
- See `docs/COMPLETE_SETUP_GUIDE.md` for detailed instructions

## 📚 Documentation
- [Complete Setup Guide](docs/COMPLETE_SETUP_GUIDE.md)
- [AI Implementation Guide](docs/AI_IMPLEMENTATION_GUIDE.md)

## 🆘 Need Help?
1. Check the documentation in the `docs/` folder
2. Ensure all environment variables are set correctly
3. Verify Google Cloud credentials (if using AI features)
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    print_success("Created README.md")

def display_completion_message():
    """Display completion message with next steps"""
    print_header("🎉 SETUP COMPLETE!")
    
    print(f"{Colors.BOLD}{Colors.GREEN}Sahayak AI Platform has been set up successfully!{Colors.END}\n")
    
    print(f"{Colors.BOLD}📂 Project Structure:{Colors.END}")
    print("  📁 sahayak-frontend/    - React frontend application")
    print("  📁 sahayak-backend/     - FastAPI backend application")
    print("  📁 docs/               - Documentation and guides")
    print("  📁 scripts/            - Startup scripts")
    print("  📄 README.md           - Project overview and quick start")
    
    print(f"\n{Colors.BOLD}🚀 Next Steps:{Colors.END}")
    
    print(f"\n{Colors.PURPLE}1. Start the Platform:{Colors.END}")
    if platform.system() == "Windows":
        print("   Run: scripts\\start-all.bat")
    else:
        print("   Run: scripts/start-all.sh")
    
    print(f"\n{Colors.PURPLE}2. Access the Application:{Colors.END}")
    print("   - Frontend: http://localhost:5173")
    print("   - Backend API: http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    
    print(f"\n{Colors.PURPLE}3. Configure AI Features (Optional):{Colors.END}")
    print("   - Set up Google Cloud Project")
    print("   - Update environment variables")
    print("   - See docs/COMPLETE_SETUP_GUIDE.md")
    
    print(f"\n{Colors.PURPLE}4. Start Development:{Colors.END}")
    print("   - Backend runs in demo mode by default")
    print("   - Frontend has all UI components ready")
    print("   - Check docs/ for implementation guides")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}🎓 Happy Learning with Sahayak!{Colors.END}")

def main():
    """Main setup function"""
    print_header("🎓 SAHAYAK AI PLATFORM SETUP")
    
    print(f"{Colors.BOLD}Welcome to the Sahayak AI Platform setup assistant!{Colors.END}")
    print("This script will set up your complete development environment.\n")
    
    # Check system requirements
    if not check_system_requirements():
        print_error("Please install missing requirements and run again.")
        return False
    
    try:
        # Run setup steps
        setup_project_structure()
        setup_backend()
        setup_frontend()
        create_environment_files()
        create_startup_scripts()
        check_google_cloud_cli()
        create_documentation()
        
        # Display completion message
        display_completion_message()
        
        return True
        
    except Exception as e:
        print_error(f"Setup failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 