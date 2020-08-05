import websocket # pip install websocket-client
import time

# nc -lk 9999 (start.sh)


def on_message(ws, message):
    print('message', message)

def on_error(ws, error):
    print('errors', error)

def on_close(ws):
    print("### closed ###")


websocket.enableTrace(True)
url = "ws://localhost:9999"
ws = websocket.WebSocketApp(url,
        header=None,
        on_open=None,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_ping=None,
        on_pong=None,
        on_cont_message=None,
        keep_running=True,
        get_mask_key=None,
        cookie=None,
        subprotocols=None,
        on_data=None)
# ws.run_forever()
