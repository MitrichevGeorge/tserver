from flask import Flask, request, jsonify
import user_agents
import ipaddress

app = Flask(__name__)

def get_real_ip():
    # Берём список адресов из X-Forwarded-For (если прокси)
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        # Берём первый адрес (обычно это клиентский)
        ip_candidates = [ip.strip() for ip in x_forwarded_for.split(",")]
    else:
        # Fallback — прямой IP
        ip_candidates = [request.remote_addr]

    # Проверяем каждый IP
    for ip in ip_candidates:
        try:
            ip_obj = ipaddress.ip_address(ip)
            # Если это валидный IPv4 или IPv6 — возвращаем
            return str(ip_obj)
        except ValueError:
            continue
    return "Unknown"

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    client_ip = get_real_ip()
    ua_string = request.headers.get("User-Agent", "Unknown")
    ua = user_agents.parse(ua_string)

    data = {
        "client_ip": client_ip,  # Может быть IPv4 или IPv6
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
    app.run(host="0.0.0.0", port=5000)
