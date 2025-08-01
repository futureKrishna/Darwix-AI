# WebSocket Testing Guide

## 🌐 Testing WebSocket Functionality

Since the application doesn't include a WebSocket test page, here are several ways to test the real-time sentiment streaming:

### **Method 1: Browser Developer Console (Easiest)**

1. Open your browser and go to any webpage
2. Open Developer Tools (F12)
3. Go to the Console tab
4. Paste and run this code:

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/sentiment/call_f7a5985b-5220-4361-b627-f9fa1a841763');

ws.onopen = function(event) {
    console.log('✅ Connected to WebSocket');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('📊 Sentiment Update:', data);
};

ws.onclose = function(event) {
    console.log('❌ WebSocket connection closed');
};

ws.onerror = function(error) {
    console.log('⚠️ WebSocket error:', error);
};

// To close the connection later:
// ws.close();
```

### **Method 2: Python Script**

Create a simple Python WebSocket client:

```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/sentiment/call_f7a5985b-5220-4361-b627-f9fa1a841763"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            
            # Listen for messages
            async for message in websocket:
                data = json.loads(message)
                print(f"📊 Sentiment Update: {data}")
                
    except Exception as e:
        print(f"⚠️ Error: {e}")

# Run the client
asyncio.run(test_websocket())
```

### **Method 3: Command Line with websocat**

Install websocat and test:
```bash
# Install websocat (cross-platform WebSocket client)
# Windows: choco install websocat
# Mac: brew install websocat
# Linux: snap install websocat

# Test WebSocket connection
websocat ws://localhost:8000/ws/sentiment/call_f7a5985b-5220-4361-b627-f9fa1a841763
```

### **Method 4: Online WebSocket Tester**

Use online tools like:
- websocket.org/echo.html
- www.websocket.org/echo.html
- piehost.com/websocket-tester

Connect to: `ws://localhost:8000/ws/sentiment/call_f7a5985b-5220-4361-b627-f9fa1a841763`
