# HomeDefender

**HomeDefender** is an open-source home security system built on top of [Home Assistant](https://www.home-assistant.io/) as an **Integration**. It enables intelligent intruder detection and notification using AI-powered video analysis and tight integration with the Home Assistant automation system.

With HomeDefender, you can monitor your home through IP cameras and sensors, detect suspicious activities (such as intruders or animals), and receive alerts or trigger alarms via Home Assistant. Remote access is supported through Home Assistant Cloud (Nabu Casa), allowing you to check the status of your home from anywhere.

## 🔐 Features

* **AI-Powered Intruder Detection**  
  Utilizes the Ultralytics YOLOv8 neural network to detect humans and pets (or other animals).

* **Dangerous Sound Detection (Glass Break)**  
  The system uses sound analysis to determine whether a dangerous event (such as glass breaking) or a non-threatening event (such as pets or human speech) has occurred. All data is processed on a local server — nothing is sent outside the local system ensuring the integrity of the user's personal data.

* **Home Assistant Integration**  
  Built as an Integration within the Home Assistant environment.

* **Remote Monitoring**  
  Accessible from anywhere via Home Assistant Cloud (Nabu Casa).

* **Email and Push Notifications**  
  The system can send email messages or push notifications through the Home Assistant app.

---

## 🛠️ Development Environment Setup Instructions

### 1. Prerequisites

Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (or any Docker Engine) and **leave it running**.

### 2. Setting Up the Development Environment via Home Assistant

1. Visit the official setup page:  
   👉 [https://developers.home-assistant.io/docs/development_environment/](https://developers.home-assistant.io/docs/development_environment/)

2. Paste the following repository URL into the input field:

   ```text
   https://github.com/TPO-2024-2025/HomeDefender
   ```

3. Click **Open** and allow your browser to launch **Visual Studio Code**.

4. If prompted, approve the installation of the **Remote - Containers** extension.

5. Wait for the container to build. This may take a few minutes.

### 3. Fixing the YOLOv8 Model File

The preloaded `yolov8n.pt` file may be invalid due to GitHub compression. Replace it with:

```bash
cd config/custom_components/tpo_home_security
rm yolov8n.pt  # če obstaja
wget https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt -O yolov8n.pt
```

This will download the YOLOv8n model used for detecting humans and animals.

### 4. Running Home Assistant

In Visual Studio Code:

* Open the command palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
* Select: `Tasks: Run Task` → `Run HomeAssistant Core`

This will start Home Assistant, which will be available at:

👉 [http://localhost:8123](http://localhost:8123)

---

## 📷 Camera Setup

By default, no camera is connected and this area in the Dashboard is empty.

1. Open the **Generic Camera** card in the Home Assistant dashboard.
2. Click settings and enter the stream URL of your IP camera.

💡 For development:  
Use the **DroidCam** app on Android to simulate an IP camera on your local network using your smartphone.

---

## 🌐 Remote Access to the System

HomeDefender is also accessible remotely via Nabu Casa:

👉 [https://10q88uinbelha2kghc5bd5dvqybqo6ec.ui.nabu.casa/](https://10q88uinbelha2kghc5bd5dvqybqo6ec.ui.nabu.casa/)

Use this secure link to access the Home Assistant dashboard from anywhere.

---

## 🎥 Video Tutorial

For a complete setup, watch this [YouTube video](https://www.youtube.com/watch?v=i3Z57cE1wpY), which explains the full environment setup steps in detail.

It also shows terminal outputs in Visual Studio Code and usage examples mentioned in the presentation.

---

## 📄 Licensing

This repository includes code and models under the following licenses:

* **Home Assistant Core**  
  Licensed under Apache License 2.0  
  → [https://github.com/home-assistant/core/blob/dev/LICENSE.md](https://github.com/home-assistant/core/blob/dev/LICENSE.md)

* **Ultralytics YOLOv8**  
  Licensed under GNU AGPL-3.0  
  → [https://github.com/ultralytics/ultralytics/blob/main/LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE)

All contributions to this project must comply with the licenses listed above.

---

> HomeDefender is a student project developed for educational purposes (TPO 2024/2025). It demonstrates how AI vision can enhance home security through the use of Home Assistant.
