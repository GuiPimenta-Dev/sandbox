import websocket

def test_websocket_connection(websocket_endpoint):
    try:
        ws = websocket.create_connection(websocket_endpoint)
        print("WebSocket connection established successfully.")
        ws.close()
    except Exception as e:
        print(f"Failed to establish WebSocket connection: {e}")

# Replace this with your actual WebSocket endpoint URL
websocket_endpoint = "wss://tmr3tat2fd.execute-api.us-east-2.amazonaws.com/dev/"

test_websocket_connection(websocket_endpoint)
