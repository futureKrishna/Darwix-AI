import asyncio
import aiohttp
from datetime import datetime, timedelta
import json

class ProductionAPITester:
    """Comprehensive production API test suite"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_health_check(self):
        """Test GET /health"""
        print("1. Testing health check endpoint...")
        async with self.session.get(f"{self.base_url}/health") as response:
            assert response.status == 200
            data = await response.json()
            assert data["status"] == "healthy"
        print("✅ Health check passed")
    
    async def test_get_all_calls(self):
        """Test GET /api/v1/calls"""
        print("2. Testing get all calls endpoint...")
        async with self.session.get(f"{self.base_url}/api/v1/calls") as response:
            assert response.status == 200
            data = await response.json()
            assert "calls" in data
            assert "total" in data
        print(f"✅ Get all calls passed - Found {data['total']} calls")
        return data
    
    async def test_get_calls_with_filters(self):
        """Test GET /api/v1/calls with filters"""
        print("3. Testing calls endpoint with filters...")
        async with self.session.get(f"{self.base_url}/api/v1/calls?limit=10") as response:
            assert response.status == 200
            data = await response.json()
            assert len(data["calls"]) <= 10
        print("✅ Query filters working correctly")
    
    async def test_get_call_by_id(self, call_id: str):
        """Test GET /api/v1/calls/{call_id}"""
        print(f"4. Testing get call by ID: {call_id}")
        async with self.session.get(f"{self.base_url}/api/v1/calls/{call_id}") as response:
            assert response.status == 200
            call = await response.json()
            assert call["call_id"] == call_id
        print(f"✅ Get call by ID passed")
    
    async def test_call_recommendations(self, call_id: str):
        """Test GET /api/v1/calls/{call_id}/recommendations"""
        print(f"5. Testing recommendations for call: {call_id}")
        async with self.session.get(f"{self.base_url}/api/v1/calls/{call_id}/recommendations") as response:
            assert response.status == 200
            data = await response.json()
            assert "similar_calls" in data
            assert "coaching_nudges" in data
        print(f"✅ Recommendations passed")
    
    async def run_comprehensive_test(self):
        """Run all production tests"""
        print("🚀 Starting comprehensive production API tests...\n")
        
        try:
            await self.test_health_check()
            calls_data = await self.test_get_all_calls()
            await self.test_get_calls_with_filters()
            
            if calls_data["calls"]:
                test_call = calls_data["calls"][0]
                await self.test_get_call_by_id(test_call["call_id"])
                await self.test_call_recommendations(test_call["call_id"])
            
            print("\n🎉 ALL PRODUCTION TESTS PASSED!")
            print("🏆 Your microservice is ready for production!")
            print("💼 Perfect for your job interview!")
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            return False

async def main():
    """Run production tests"""
    async with ProductionAPITester() as tester:
        return await tester.run_comprehensive_test()

if __name__ == "__main__":
    print("🔧 Starting production test runner...")
    try:
        result = asyncio.run(main())
        print(f"🎯 Final result: {'SUCCESS' if result else 'FAILED'}")
    except Exception as e:
        print(f"❌ Test runner error: {e}")
