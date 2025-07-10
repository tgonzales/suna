#!/usr/bin/env python3
"""
Production deployment script for Suna.
This script handles the deployment process including initialization of production settings.
"""

import os
import subprocess
import sys
import asyncio
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {cmd}")
            return True
        else:
            print(f"❌ {cmd}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed to run command: {cmd}")
        print(f"Error: {e}")
        return False

def check_environment():
    """Check if required environment variables are set"""
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'SUPABASE_SERVICE_ROLE_KEY',
        'REDIS_URL',
        'FERNET_KEY',
        'DAYTONA_URL',
        'DAYTONA_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All required environment variables are set")
    return True

def deploy_frontend():
    """Deploy frontend"""
    print("\n🚀 Deploying frontend...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Install dependencies
    if not run_command("npm ci", cwd=frontend_dir):
        return False
    
    # Build for production
    if not run_command("npm run build", cwd=frontend_dir):
        return False
    
    print("✅ Frontend deployed successfully")
    return True

def deploy_backend():
    """Deploy backend"""
    print("\n🚀 Deploying backend...")
    
    backend_dir = Path(__file__).parent / "backend"
    
    # Build Docker image
    if not run_command("docker build -t suna-backend .", cwd=backend_dir):
        return False
    
    # Run production initialization
    if not run_command("python init_production.py", cwd=backend_dir):
        print("⚠️  Production initialization failed, but continuing...")
    
    print("✅ Backend deployed successfully")
    return True

def main():
    """Main deployment function"""
    print("🚀 Starting Suna production deployment...")
    
    # Check environment
    if not check_environment():
        print("❌ Deployment failed - Environment check failed")
        return False
    
    # Deploy backend
    if not deploy_backend():
        print("❌ Deployment failed - Backend deployment failed")
        return False
    
    # Deploy frontend
    if not deploy_frontend():
        print("❌ Deployment failed - Frontend deployment failed")
        return False
    
    print("\n✅ Suna deployed successfully!")
    print("\n📋 Next steps:")
    print("1. Configure your cloud provider (Vercel, Railway, etc.)")
    print("2. Set up environment variables in your cloud platform")
    print("3. Deploy the built applications")
    print("4. Configure custom domain (optional)")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)