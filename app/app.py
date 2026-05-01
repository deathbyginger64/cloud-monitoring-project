import streamlit as st
import requests

PROM_URL = "http://localhost:9090/api/v1/query"

st.title("Cloud Resource Monitoring & Recommendation System")

def query_prometheus(query):
    try:
        response = requests.get(PROM_URL, params={"query": query})
        return response.json()
    except:
        return None

def is_backend_up():
    data = query_prometheus("up")

    if not data:
        return False

    results = data.get("data", {}).get("result", [])

    for item in results:
        metric = str(item.get("metric", {}))
        value = item.get("value", [])[1]

        if "backend" in metric and value == "1":
            return True

    return False

st.subheader("Monitoring Status (Prometheus)")

backend_status = is_backend_up()

if not backend_status:
    st.error("Critical Service DOWN ❌")
    st.warning("Dependent service is still active → Resource inefficiency detected")
    st.info("Recommendation: Stop or restart dependent service")
else:
    st.success("All services running efficiently ✅")
