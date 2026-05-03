<div align="center">

# ☁️ Cloud Monitoring System

### Real-time infrastructure observability on AWS — powered by Prometheus, Grafana & Telegram

[![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/ec2/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)](https://grafana.com/)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-22c55e?style=for-the-badge)]()

<br/>

> **Monitor your cloud infrastructure in real time. Visualise every metric. Get alerted on Telegram the instant something goes wrong.**

<br/>

</div>

---

## 🔭 Overview

This project delivers a **complete, production-grade observability stack** for cloud infrastructure. Once deployed, it:

- 📊 **Collects** CPU, memory, disk I/O, and network metrics every 15 seconds via Node Exporter
- 💾 **Stores** time-series data in Prometheus with configurable retention
- 📈 **Visualises** everything on beautiful Grafana dashboards
- 🚨 **Alerts** via Telegram the moment a threshold is crossed — no polling, no delay

The entire stack runs in **Docker containers**, making it reproducible, portable, and easy to tear down or redeploy.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS EC2 (Ubuntu)                         │
│                                                                 │
│  ┌───────────────┐    ┌─────────────────┐    ┌──────────────┐  │
│  │ Node Exporter │───▶│   Prometheus    │───▶│   Grafana    │  │
│  │  (port 9100)  │    │  (port 9090)    │    │ (port 3000)  │  │
│  └───────────────┘    └─────────────────┘    └──────┬───────┘  │
│       Scrapes               Stores &                │          │
│    system metrics         queries metrics     Alert Rules      │
│                                                     │          │
└─────────────────────────────────────────────────────┼──────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │  Telegram Bot   │
                                              │  (Webhook POST) │
                                              └─────────────────┘
                                                 Your Phone 📱
```

### Component Responsibilities

| Component         | Role                                                                 |
|-------------------|----------------------------------------------------------------------|
| **Node Exporter** | Runs on the host and exposes 1000+ OS-level metrics via HTTP        |
| **Prometheus**    | Scrapes Node Exporter every 15s, stores data, evaluates alert rules |
| **Grafana**       | Queries Prometheus, renders dashboards, fires contact point alerts  |
| **Telegram Bot**  | Receives webhook POST from Grafana and delivers the alert message   |

---

## 🛠️ Tech Stack

| Technology        | Version  | Purpose                        |
|-------------------|----------|--------------------------------|
| AWS EC2           | —        | Cloud compute (Ubuntu 22.04)   |
| Docker            | 24+      | Container runtime              |
| Docker Compose    | 2+       | Multi-container orchestration  |
| Prometheus        | latest   | Metrics collection & storage   |
| Grafana           | latest   | Dashboards & alerting          |
| Node Exporter     | latest   | System metrics exporter        |
| Telegram Bot API  | —        | Push notifications             |

---

## 📁 Project Structure

```
cloud-monitoring-project/
│
├── docker-compose.yml      # Defines all three services & their config
├── prometheus.yml          # Scrape jobs, intervals, and targets
└── README.md
```

---

## ✅ Prerequisites

Before you begin, make sure you have the following:

- [ ] An **AWS account** with permission to launch EC2 instances
- [ ] A **key pair** (.pem file) to SSH into the EC2 instance
- [ ] A **Telegram account** (to create an alert bot)
- [ ] Basic comfort with the **Linux CLI** and Docker

---

## 🚀 Getting Started

### 1. Launch EC2 Instance

1. Sign in to the [AWS EC2 Console](https://console.aws.amazon.com/ec2/).
2. Click **Launch Instance** and choose **Ubuntu Server 22.04 LTS**.
3. Select **`t3.micro`** as the instance type.
4. Under **Security Group**, add the following **inbound rules**:

   | Type   | Protocol | Port Range | Source     | Purpose       |
   |--------|----------|------------|------------|---------------|
   | SSH    | TCP      | 22         | Your IP    | Remote access |
   | Custom | TCP      | 3000       | 0.0.0.0/0  | Grafana       |
   | Custom | TCP      | 9090       | 0.0.0.0/0  | Prometheus    |
   | Custom | TCP      | 9100       | 0.0.0.0/0  | Node Exporter |

5. Launch the instance and connect via SSH:
```bash
   ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

> ⚠️ **Security note:** For production, restrict ports 9090 and 9100 to your IP or a VPN — they should not be publicly exposed.

---

### 2. Install Docker

```bash
# Update package index
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
sudo apt install docker.io docker-compose -y

# Start and enable Docker on boot
sudo systemctl enable --now docker

# (Optional) Run Docker without sudo
sudo usermod -aG docker $USER && newgrp docker
```

Verify the installation:
```bash
docker --version
docker-compose --version
```

---

### 3. Clone the Repository

```bash
git clone https://github.com/deathbyginger64/cloud-monitoring-project.git
cd cloud-monitoring-project
```

---

### 4. Start All Services

```bash
docker-compose up -d
```

Docker will pull the required images and start all three containers in the background. This may take a minute on first run.

---

### 5. Verify & Access

Check that all containers are healthy:
```bash
docker-compose ps
```

Expected output:
```
NAME            IMAGE                COMMAND                  STATUS    PORTS
grafana         grafana/grafana      "/run.sh"                Up        0.0.0.0:3000->3000/tcp
node-exporter   prom/node-exporter   "/bin/node_exporter"     Up        0.0.0.0:9100->9100/tcp
prometheus      prom/prometheus      "/bin/prometheus ..."    Up        0.0.0.0:9090->9090/tcp
```

Access the services in your browser:

| Service           | URL                                    | Default Credentials |
|-------------------|----------------------------------------|---------------------|
| **Grafana**       | `http://<EC2-PUBLIC-IP>:3000`          | admin / admin       |
| **Prometheus**    | `http://<EC2-PUBLIC-IP>:9090`          | —                   |
| **Node Exporter** | `http://<EC2-PUBLIC-IP>:9100/metrics`  | —                   |

---

## ⚙️ Configuration Reference

### docker-compose.yml

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
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - "9100:9100"
    restart: unless-stopped

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    restart: unless-stopped
```

> `restart: unless-stopped` ensures containers automatically recover after a reboot or crash.

---

### prometheus.yml

```yaml
global:
  scrape_interval: 15s      # How often to scrape targets
  evaluation_interval: 15s  # How often to evaluate alert rules

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

To monitor **additional hosts**, add more targets:
```yaml
    static_configs:
      - targets:
          - 'node-exporter:9100'   # This server
          - '10.0.0.5:9100'        # Server 2
          - '10.0.0.6:9100'        # Server 3
```

---

## 📊 Grafana Setup

### 1. Connect Prometheus as Data Source

1. Log in at `http://<EC2-PUBLIC-IP>:3000` (change the default `admin/admin` password when prompted).
2. Navigate to **Connections → Data Sources → Add new data source**.
3. Select **Prometheus**.
4. Set the URL to:
```
   http://prometheus:9090
```
5. Click **Save & Test** — you should see a green "Data source is working" banner.

---

### 2. Import the Node Exporter Dashboard

1. Go to **Dashboards → Import**.
2. Enter ID **`1860`** and click **Load**.
3. Select your Prometheus data source from the dropdown.
4. Click **Import**.

You now have a full dashboard showing CPU, memory, disk, and network metrics out of the box.

---

### 3. Create an Alert Rule

Navigate to **Alerting → Alert Rules → New alert rule** and configure:

**Query (PromQL):**
```promql
100 - (avg by(instance)(irate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
```

**Alert Settings:**

| Setting              | Value                                               |
|----------------------|-----------------------------------------------------|
| Condition            | Is above **80**                                     |
| Evaluate every       | `1m`                                                |
| For (pending period) | `2m` (avoids alert flapping on short spikes)        |
| Summary annotation   | `High CPU usage on {{ $labels.instance }}`          |

> The **pending period** of 2 minutes means the condition must stay true continuously before the alert fires, reducing false positives from transient spikes.

---

## 📩 Telegram Alerts

### Step 1 — Create a Bot

1. Open Telegram and search for **@BotFather**.
2. Send the command `/newbot` and follow the prompts.
3. Copy the **Bot Token** (format: `123456789:ABCdef...`).

### Step 2 — Get Your Chat ID

1. Search for **@userinfobot** in Telegram and send `/start`.
2. Copy the **Chat ID** from the reply (it may be a negative number for group chats).

### Step 3 — Test the Webhook Manually

Before configuring Grafana, verify your bot works by running this in your terminal:

```bash
curl -s -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "<YOUR_CHAT_ID>", "text": "✅ Telegram alert test successful!"}'
```

You should receive the message in Telegram immediately.

### Step 4 — Configure Grafana Contact Point

1. Go to **Alerting → Contact Points → Add contact point**.
2. Fill in the following:

   | Field   | Value                                                        |
   |---------|--------------------------------------------------------------|
   | Name    | `Telegram`                                                   |
   | Type    | `Webhook`                                                    |
   | Method  | `POST`                                                       |
   | URL     | `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage`  |

3. Under **Optional Webhook settings → HTTP Headers**, add:
```
   Content-Type: application/json
```
4. Under **Message body**, paste:
```json
   {
     "chat_id": "<YOUR_CHAT_ID>",
     "text": "🚨 *ALERT FIRED*\n\n*Rule:* {{ .CommonLabels.alertname }}\n*Summary:* {{ .CommonAnnotations.summary }}\n\n🔥 {{ .Alerts.Firing | len }} alert(s) currently firing.",
     "parse_mode": "Markdown"
   }
```
5. Click **Test** to send a test message, then **Save contact point**.

### Step 5 — Link Contact Point to Your Alert

1. Go to **Alerting → Notification Policies**.
2. Set the **Default policy** contact point to `Telegram`, or create a specific routing rule targeting your alert.

---

## 📐 Metrics Reference

| Metric                   | PromQL Query                                                                                                        | Description              |
|--------------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------|
| **CPU Usage %**          | `100 - (avg by(instance)(irate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)`                                   | Overall CPU utilisation  |
| **Memory Usage %**       | `(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100`                                          | RAM utilisation          |
| **Disk Usage %**         | `100 - ((node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100)`         | Root disk usage          |
| **Network In (bytes/s)** | `irate(node_network_receive_bytes_total[1m])`                                                                       | Inbound network traffic  |
| **Network Out (bytes/s)**| `irate(node_network_transmit_bytes_total[1m])`                                                                      | Outbound network traffic |
| **System Load (1m)**     | `node_load1`                                                                                                        | 1-minute load average    |

---

## 🧪 Testing the Pipeline

### Simulate High CPU Load

```bash
# Install the stress tool
sudo apt install stress -y

# Spike CPU for 3 minutes (adjust --cpu to match your vCPU count)
stress --cpu 2 --timeout 180
```

### What to Expect

1. Within **15 seconds**, Prometheus records CPU usage above 80%.
2. After **2 minutes** (the pending period), the alert state changes to **Firing**.
3. Grafana sends a **POST request** to the Telegram webhook.
4. You receive an alert message on your phone. 📱
5. When `stress` exits, CPU drops and Grafana sends an automatic **recovery notification**.

### Verify Alert State in Prometheus

Open `http://<EC2-PUBLIC-IP>:9090/alerts` to watch alert states in real time during the test.

---

## 🔧 Troubleshooting

<details>
<summary><strong>Containers keep restarting or won't start</strong></summary>

Check the logs of the failing container:
```bash
docker-compose logs prometheus
docker-compose logs grafana
docker-compose logs node-exporter
```
Look for configuration errors, missing files, or port conflicts.
</details>

<details>
<summary><strong>Prometheus shows no targets / targets are DOWN</strong></summary>

1. Open `http://<EC2-PUBLIC-IP>:9090/targets`.
2. If Node Exporter shows as DOWN, confirm the container is running:
```bash
   docker ps | grep node-exporter
```
3. Ensure the service name in `prometheus.yml` (`node-exporter`) exactly matches the Docker Compose service name.
</details>

<details>
<summary><strong>Grafana cannot connect to Prometheus</strong></summary>

Use `http://prometheus:9090` — the Docker service name — **not** `localhost:9090`. Containers communicate over an internal Docker network using service names, not localhost.
</details>

<details>
<summary><strong>Telegram test alert fails</strong></summary>

- Double-check your **Bot Token** and **Chat ID** for typos.
- Make sure you have started a conversation with the bot (send it `/start` first).
- Re-run the manual `curl` test to isolate whether the issue is in Telegram or Grafana.
</details>

<details>
<summary><strong>Alert never fires even under high CPU</strong></summary>

1. Confirm the PromQL query returns data in **Prometheus → Graph**.
2. In Grafana's alert list, look for the alert in **Pending** state — it must stay Pending for the full pending period before it fires.
3. Ensure the Notification Policy is pointing to your Telegram contact point.
</details>

---

## 📈 Scaling Beyond Single Node

This setup is intentionally minimal to get you started. Here is how to grow it:

**Multi-Host Monitoring** — Add more targets to `prometheus.yml`. Node Exporter must be running on each remote host:
```yaml
static_configs:
  - targets: ['node-exporter:9100', '10.0.0.5:9100', '10.0.0.6:9100']
```

**Persistent Storage** — By default, Prometheus data is lost when the container restarts. Add a named volume to preserve it:
```yaml
prometheus:
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus_data:/prometheus

volumes:
  prometheus_data:
```

**Kubernetes Deployment** — Use the official Helm chart for production:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack
```

**Prometheus Federation** — Aggregate metrics from multiple Prometheus instances into a single global view:
```yaml
- job_name: 'federate'
  honor_labels: true
  metrics_path: '/federate'
  params:
    match[]: ['{job=~".+"}']
  static_configs:
    - targets:
        - 'prometheus-region-1:9090'
        - 'prometheus-region-2:9090'
```

---

## 🗺️ Roadmap

- [x] Single-node monitoring with Prometheus + Grafana
- [x] Real-time Telegram alerting via webhooks
- [x] Fully containerised deployment with Docker Compose
- [ ] Persistent Prometheus storage via named volumes
- [ ] Grafana dashboard provisioning via config files (no manual import)
- [ ] Multi-node monitoring support
- [ ] Email and PagerDuty alert channels
- [ ] Kubernetes deployment with Helm (kube-prometheus-stack)
- [ ] Prometheus federation for multi-region visibility
- [ ] TLS / HTTPS for all exposed endpoints
- [ ] Auto-scaling triggers based on metric thresholds

---

## 👨‍💻 Author

**Aditya Khandelwal**

If you found this project useful, consider giving it a ⭐ on GitHub — it helps others discover it.

---

<div align="center">

Built with ❤️ using open-source tools

</div>
