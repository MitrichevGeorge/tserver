from flask import Flask, request, jsonify
import user_agents

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # IP-адрес клиента
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    # User-Agent
    ua_string = request.headers.get("User-Agent", "Unknown")
    ua = user_agents.parse(ua_string)

    data = {
        "client_ip": ip,
        "user_agent_raw": ua_string,
        "device": {
            "family": ua.device.family,
            "brand": ua.device.brand,
            "model": ua.device.model,
            "is_mobile": ua.is_mobile,
            "is_tablet": ua.is_tablet,
            "is_pc": ua.is_pc,
            "is_bot": ua.is_bot,
        },
        "os": {
            "family": ua.os.family,
            "version": ua.os.version_string,
        },
        "browser": {
            "family": ua.browser.family,
            "version": ua.browser.version_string,
        },
        "requested_path": f"/{path}"
    }
    return jsonify(data)

if __name__ == "__main__":
    # Локально можно запустить так
    app.run(host="0.0.0.0", port=5000)
