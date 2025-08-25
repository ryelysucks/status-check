import a2s

SERVER = ("arma.sketchyvirus.xyz", 2309)

def check_server():
    try:
        info = a2s.info(SERVER)

        # Basic server info
        details = {
            "server_name": info.server_name,
            "map": info.map_name,
            "players": f"{info.player_count}/{info.max_players}",
            "game": info.game,
            "online_players": []
        }

        # Get player list
        players = a2s.players(SERVER)
        if players:
            details["online_players"] = [p.name for p in players]

        return details

    except Exception as e:
        return {"error": f"Server Offline! ({e})"}
