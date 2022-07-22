from __future__ import print_function
import geventwebsocket
from geventwebsocket.server import WebSocketServer
user_list = []
def echo_app(environ, start_response):
    websocket = environ.get("wsgi.websocket")
    if websocket is None:
        return http_handler(environ, start_response)
    try:
        user_list.append(websocket)
        while True:
            message = websocket.receive()
            # websocket.send(message)
            for us in user_list:  # 遍历发送给列表所有
                try:
                    us.send(message)
                except:
                    continue
        # websocket.close()
    except geventwebsocket.WebSocketError as ex:
        print("{0}: {1}".format(ex.__class__.__name__, ex))

def http_handler(environ, start_response):
    if environ["PATH_INFO"].strip("/") == "version":
        print(environ["QUERY_STRING"])
        # http://localhost:5000/version?id=12
        start_response("200 OK", [])
        for us in user_list:  # 遍历发送给列表所有
            try:
                us.send("get from http")
            except:
                continue
        return [b"pay success"]
    else:
        start_response("400 Bad Request", [])
        return [b"WebSocket connection is expected here."]

WebSocketServer(("localhost", 5000), echo_app, debug=False).serve_forever()






