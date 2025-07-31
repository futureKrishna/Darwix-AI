#!/usr/bin/env python3
"""
Fast development server with optimized startup
Uses fallback AI implementations for quick development cycles
"""
import subprocess
import sys
import time
import asyncio
import os

async def setup_database():
    """Setup database tables"""
    try:
        from app.models import Base
        from app.database import engine
        
        print("🔄 Setting up database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with code {e.returncode}")
        return False

def main():
    print("🚀 Fast Development Server - Sales Analytics Microservice")
    print("=" * 60)
    print("Features:")
    print("✅ Fast startup with fallback AI implementations")
    print("✅ All API endpoints functional")
    print("✅ Production-ready architecture")
    print("✅ Complete database with 200+ calls")
    print("=" * 60)
    
    # Step 1: Setup database
    try:
        success = asyncio.run(setup_database())
        if not success:
            print("⚠️  Database setup had issues, but continuing...")
    except Exception as e:
        print(f"⚠️  Database setup error: {e}, but continuing...")
    
    # Step 2: Generate data (only if needed)
    if not os.path.exists("sales_analytics.db"):
        print("\n📊 Generating sample data...")
        if not run_command("python generate_data.py", "Data generation"):
            print("❌ Data generation failed. Exiting.")
            return False
        print("✅ Sample data generated successfully")
    else:
        print("✅ Database already exists, skipping data generation")
    
    # Step 3: Start server immediately
    print("\n🌐 Starting FastAPI server...")
    print("Server will start at http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nFor PRODUCTION with real ML models, use: python production_ml_run.py")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped.")
    
    print("\n✅ Development setup complete!")
    print("\n📋 Available endpoints:")
    print("  • GET /health")
    print("  • GET /api/v1/calls (with all filters)")
    print("  • GET /api/v1/calls/{call_id}")
    print("  • GET /api/v1/calls/{call_id}/recommendations")
    print("  • GET /api/v1/analytics/agents")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
