import requests
import boto3

# =========================
# CONFIGURATION
# =========================

PROM_URL = "http://localhost:9090/api/v1/query"

# 🔥 Replace with your actual SNS Topic ARN
TOPIC_ARN = "arn:aws:sns:ap-south-1:492413877464:cloud-alerts"

# AWS SNS client
sns = boto3.client("sns")


# =========================
# PROMETHEUS FUNCTIONS
# =========================

def query_prometheus(query):
    try:
        response = requests.get(PROM_URL, params={"query": query})
        return response.json()
    except Exception as e:
        print("Prometheus Error:", e)
        return None


def is_backend_up():
    data = query_prometheus("up")

    if not data:
        return False

    results = data.get("data", {}).get("result", [])

    for item in results:
        metric = str(item.get("metric", {}))
        value = item.get("value", [])[1]

        # 🔍 Checking backend service
        if "backend" in metric and value == "1":
            return True

    return False


# =========================
# SNS ALERT FUNCTION
# =========================

def send_sns_alert(message):
    try:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Cloud Alert 🚨",
            Message=message
        )
        print("📩 SNS Alert Sent!")
    except Exception as e:
        print("SNS Error:", e)


# =========================
# POLICY ENGINE
# =========================

def check_system():
    print("\n===== CLOUD MONITORING SYSTEM =====\n")

    backend_status = is_backend_up()

    if not backend_status:
        print("⚠️ BACKEND is DOWN ❌")
        print("👉 Dependent service is still running")
        print("👉 Recommendation: Stop or restart dependent service")

        message = """
🚨 ALERT: Backend Service DOWN

Backend service is not running.
A dependent service is still active.

Recommendation:
Stop or restart dependent service to optimize resource usage.
"""

        send_sns_alert(message)

    else:
        print("✅ All services are running efficiently")


# =========================
# MAIN EXECUTION
# =========================

if __name__ == "__main__":
    check_system()
