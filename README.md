# 🚀 Cloud Monitoring System using AWS, Prometheus & Grafana

## 📌 Project Overview

This project implements a **cloud-based monitoring and alerting system** using AWS EC2, Docker, Prometheus, Grafana, and Telegram.

It continuously monitors system metrics such as **CPU, Memory, Disk, and Network usage**, and sends **real-time alerts to Telegram** when thresholds are exceeded.

---

## 🧠 Architecture Overview

```
Node Exporter → Prometheus → Grafana → Alert Rule → Telegram Webhook
```

### 🔹 Components:

* **AWS EC2 (Ubuntu)** → Cloud infrastructure
* **Docker** → Containerized deployment
* **Node Exporter** → Collects system metrics
* **Prometheus** → Stores & processes metrics
* **Grafana** → Visualization & alerting
* **Telegram Bot** → Sends notifications

---

## ⚙️ Technologies Used

* AWS EC2
* Docker & Docker Compose
* Prometheus (Monitoring)
* Grafana (Visualization + Alerts)
* Node Exporter
* Telegram Bot API

---

## 📁 Project Structure

```
cloud-monitoring-project/
│
├── docker-compose.yml
├── prometheus.yml
├── README.md
```

---

## 🐳 Docker Setup

### 🔹 docker-compose.yml

```yaml
version: '3'

services:
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  node-exporter:
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - "9100:9100"

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
```

---

## 📊 Prometheus Configuration

### 🔹 prometheus.yml

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

👉 Prometheus collects metrics every 15 seconds from Node Exporter.

---

## 🚀 How to Run the Project (Step-by-Step)

### 🔹 Step 1: Launch EC2 Instance

* Create Ubuntu EC2 instance on AWS
* Allow ports: **3000, 9090, 9100**

---

### 🔹 Step 2: Install Docker

```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

---

### 🔹 Step 3: Install Docker Compose

```bash
sudo apt install docker-compose -y
```

---

### 🔹 Step 4: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/cloud-monitoring-project.git
cd cloud-monitoring-project
```

---

### 🔹 Step 5: Start Services

```bash
docker-compose up -d
```

---

### 🔹 Step 6: Access Services

* Prometheus → `http://<EC2-IP>:9090`
* Grafana → `http://<EC2-IP>:3000`

---

### 🔹 Step 7: Login to Grafana

```
Username: admin
Password: admin
```

---

## 📈 Grafana Setup

### 🔹 Add Data Source

1. Go to **Settings → Data Sources**
2. Add **Prometheus**
3. URL:

```
http://prometheus:9090
```

---

### 🔹 Import Dashboard

* Import Node Exporter Dashboard (ID: 1860)

---

## 🧮 PromQL Query Used

```promql
100 - (avg by(instance)(irate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
```

👉 This calculates **CPU Usage %**

---

## 🚨 Alert Rule Configuration

### 🔹 Condition

```
WHEN CPU usage > 80%
```

---

### 🔹 Evaluation

```
Every 1 minute
```

---

### 🔹 Description

Alert triggers when CPU usage crosses threshold.

---

## 📩 Telegram Integration

### 🔹 Step 1: Create Bot

* Use BotFather in Telegram
* Get Bot Token

---

### 🔹 Step 2: Get Chat ID

* Use @userinfobot

---

### 🔹 Step 3: Webhook URL

```
https://api.telegram.org/bot<TOKEN>/sendMessage
```

---

### 🔹 Step 4: JSON Body

```json
{
  "chat_id": YOUR_CHAT_ID,
  "text": "🚨 ALERT: High CPU Usage Detected!"
}
```

---

### 🔹 Step 5: Configure in Grafana

* Go to **Alerting → Contact Points**
* Add:

  * Type: Webhook
  * Method: POST
  * URL: Telegram API

---

## 🔥 Testing the System

### 🔹 Generate CPU Load

```bash
sudo apt install stress -y
stress --cpu 2
```

👉 This will trigger alert when CPU > 80%

---

## 📈 Scalability

* Currently single-node system
* Can scale by:

  * Adding multiple Node Exporters
  * Using Kubernetes
  * Prometheus federation

---

## 🧠 Key Features

* Real-time monitoring
* Alerting system
* Telegram notifications
* Containerized deployment
* Cloud-based infrastructure

---

## 🎯 Conclusion

This project demonstrates a **complete monitoring pipeline** from data collection to real-time alerting using modern DevOps tools.

---

## 👨‍💻 Author

Aditya Khandelwal

---

## 📌 Future Improvements

* Kubernetes deployment
* Multi-node monitoring
* Email/SMS alerts
* Auto-scaling infrastructure

---
