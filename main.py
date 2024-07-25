import asyncio
import json
from aiohttp import web
import aiohttp
import aiohttp.web
from get_ip import get_ips

connected_clients = set()


async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    connected_clients.add(ws)
    print(f"Client connected: {request.remote}")

    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print(f"Received message: {msg.data}")
                try:
                    events = json.loads(msg.data)
                    if isinstance(events, list):
                        response_message = json.dumps(events)
                        print(f"Broadcasting message: {response_message}")
                        await broadcast_message(response_message, ws)
                except json.JSONDecodeError:
                    print("Invalid JSON format received.")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f"WebSocket connection closed with exception: {ws.exception()}")
    finally:
        connected_clients.remove(ws)
        print(f"Client disconnected: {request.remote}")

    return ws


async def broadcast_message(message, sender_ws):
    for client in connected_clients:
        if client != sender_ws:
            try:
                await client.send_str(message)
            except:
                print(f"Error sending message to client, client disconnected.")
                connected_clients.remove(client)


async def handle_index(request):
    return web.FileResponse('static/index.html')


async def handle_server(request):
    return web.FileResponse('static/server.html')


async def handle_copy_code(request):
    return web.FileResponse('static/keypress_simulation.js')


async def save_preset(request):
    try:
        preset_name = request.match_info['name']
        data = await request.json()
        with open(f'presets/{preset_name}.json', 'w') as f:
            json.dump(data, f)
        return web.Response(text='Preset saved successfully')
    except Exception as e:
        print(f"Error saving preset: {e}")
        return web.Response(text='Failed to save preset', status=500)


async def load_preset(request):
    try:
        preset_name = request.match_info['name']
        with open(f'presets/{preset_name}.json', 'r') as f:
            data = json.load(f)
        return web.json_response(data)
    except Exception as e:
        print(f"Error loading preset: {e}")
        return web.Response(text='Failed to load preset', status=500)


async def list_presets(request):
    import os
    presets = [f.split('.')[0] for f in os.listdir('presets') if f.endswith('.json')]
    return web.json_response(presets)


async def handle_ping(request):
    return web.Response(text='pong')


async def main():
    app = web.Application()

    # Set up routes
    app.router.add_get('/ws', handle_websocket)
    app.router.add_get('/', handle_index)
    app.router.add_get('/server', handle_server)
    app.router.add_get('/code.js', handle_copy_code)
    app.router.add_post('/presets/{name}', save_preset)
    app.router.add_get('/presets/{name}', load_preset)
    app.router.add_get('/presets', list_presets)
    app.router.add_get('/ping', handle_ping)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '', 8080)
    await site.start()

    print('All IPs, select the working\n' + '\n'.join(get_ips()))
    print("Server started at http://IP_FROM_LIST:8080")
    print("WebSocket server started at ws://IP_FROM_LIST:8080/ws")

    await asyncio.Future()


asyncio.run(main())
