from fastapi import FastAPI, WebSocket
import uvicorn
import json
import asyncio

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  
  try:
    while True:
      try:
        data = await asyncio.wait_for(websocket.receive_text(), timeout=60.0) # 60 seconds timeout before disconnecting
        
        message = json.loads(data).get("message")
        
        username = json.loads(data).get("username")
        
        print(f"Received message from user ({username}): {message}")

        dummy_data = [
          {"message": f"Hello ({username}) from AI Server (1)", "is_finished": False},
          {"message": f"Hello ({username}) from AI Server (2)", "is_finished": False},
          {"message": f"Hello ({username}) from AI Server (3)", "is_finished": False},
          {"message": f"Hello ({username}) from AI Server (4)", "is_finished": False},
          {"message": f"Hello ({username}) from AI Server (5)", "is_finished": True}
        ]

        for data in dummy_data:
          await asyncio.sleep(2)
          
          await websocket.send_text(json.dumps(data))
      
      except asyncio.TimeoutError:
        print(f"Disconnecting from Client because of inactivity")
        
        await websocket.send_json({"message": "Disconnecting because of inactivity"})
        
        await websocket.close()
        
        break
      
  except:
    await websocket.close()

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8001)