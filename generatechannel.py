def generate_channel(status):
    print(status) # array shows properly here..?

    if "error" in status:
       # Return a fallback name if server is offline
       return f"❌-Server offline-❌"

    return f"✅-Server online ✅-"
