# Daily Weather Status & Discord Webhook Automation

Grabs(GET) Weather Information from an API endpoint and sends a webhook to a discord channel on a automated schedule (Daily @ 08:00).
This is used to simulate a method of log or result automation in an enterprise environment, by grabbing data from an endpoint and sending it via a webhook.

---

## 🏗️ Architecture & Technical Stack

* **Language:** Python 3.11
* **Data Source:** National Weather Service (NWS) API (`KGIF` METAR ground station)
* **Notification Delivery:** Discord Webhook API (HTTP POST)
* **Infrastructure & CI/CD:** GitHub Actions (Ubuntu runner environments)
* **Secret Management:** GitHub Repository Secrets & Environment Variables (`.env`)

---

## 🔄 How It Works

1. **Scheduled Telemetry Ingestion:** A GitHub Actions cron trigger executes the Python pipeline on a daily automated schedule.
2. **API Data Extraction:** `main.py` makes a secure HTTP request to the NWS API endpoints, parsing live JSON payloads for atmospheric pressure, temperature, wind telemetry, and observation timestamps.
3. **Payload Formatting:** The script processes and structures the raw data into a human-readable alert message.
4. **Webhook Dispatch:** The structured payload is securely transmitted via an encrypted POST request to a Discord channel webhook, providing instant visibility without manual intervention.

---

## 🏢 Simulating Enterprise Alerting & Platform Engineering

This project is built to mirror **Site Reliability Engineering (SRE)** and platform engineering patterns found in production enterprise environments:

* **Automated Monitoring & Cron Triggers:** Just as enterprise systems rely on cloud schedulers or Kubernetes CronJobs to run health probes, this pipeline uses GitHub Actions to run unattended workloads on reliable cloud infrastructure.
* **Decoupled Secret Management:** Sensitive production credentials (like Discord Webhook URLs) are strictly isolated from source code using environment variables and GitHub Secrets, mirroring enterprise secret stores (e.g., HashiCorp Vault, AWS Secrets Manager).
* **Proactive Event-Driven Notifications:** Routing telemetry summaries directly to a team communication channel mimics enterprise incident management integrations (such as Datadog, PagerDuty, or Slack webhooks) used to notify on-call engineers of system status or operational metrics.
* **Environment Isolation:** Running code on ephemeral cloud runners (`ubuntu-latest`) rather than a local workstation ensures reproducibility, eliminating "it works on my machine" failure modes.

---

## 🚀 Getting Started Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Leon2022863/weather-status-daily-discord-automation.git](https://github.com/Leon2022863/weather-status-daily-discord-automation.git)
   cd weather-status-daily-discord-automation
