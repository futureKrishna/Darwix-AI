#!/usr/bin/env python3
"""
Production server with real ML models
Downloads and caches ML models for production-grade AI features
"""
import subprocess
import sys
import time
import os

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

def setup_production_ml():
    """Setup production ML environment"""
    print("🤖 Setting up production ML environment...")
    print("This will download and cache ML models (one-time setup)")
    
    # Test if we can load the models
    try:
        from app.ai_insights import AIInsightsProcessor
        # Force real models for production
        processor = AIInsightsProcessor(use_real_models=True)
        print("✅ Production ML models ready!")
        return True
    except Exception as e:
        print(f"⚠️  ML setup issue: {e}")
        print("Continuing with fallback implementations...")
        return False

def main():
    print("🚀 Production Server - Sales Analytics Microservice")
    print("=" * 60)
    print("Features:")
    print("🧠 Real ML models (sentence-transformers + Hugging Face)")
    print("📊 Production-grade AI insights")
    print("🔍 Real semantic similarity")
    print("💬 Advanced sentiment analysis")
    print("=" * 60)
    
    # Step 1: Setup ML environment
    ml_ready = setup_production_ml()
    
    # Step 2: Database setup
    if not run_command("python setup_database.py", "Database setup"):
        print("⚠️  Database setup had issues, but continuing...")
    
    # Step 3: Generate data with production AI
    if not os.path.exists("sales_analytics.db") or input("\nRegenerate data with production AI? (y/n): ").lower() == 'y':
        print("\n📊 Generating data with production AI models...")
        # Set environment variable to force real models
        os.environ['USE_REAL_ML'] = 'true'
        if not run_command("python generate_data.py", "Production data generation"):
            print("❌ Data generation failed. Exiting.")
            return False
    else:
        print("✅ Using existing database")
    
    # Step 4: Start server
    print("\n🌐 Starting Production FastAPI server...")
    print("Server starting at http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print(f"ML Models: {'✅ Real Models' if ml_ready else '⚠️  Fallback'}")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped.")
    
    print("\n✅ Production setup complete!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
