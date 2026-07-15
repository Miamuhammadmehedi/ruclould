# RuvCloud 🚀
RuvCloud is a powerful, lightweight, open-source dual-hosting tool built exclusively for **Termux**. It allows you to repurpose any old Android smartphone into a **24/7 Personal Cloud Server and Website Host** simultaneously.

It runs a File Manager on one port and your Custom Website on another port, exposing both securely to the global internet using native SSH tunneling.

---

## 🛠️ Features
- **Dual Mode:** Runs a remote File Manager and hosts static HTML websites at the same time.
- **Independent Links:** Generates two distinct global URLs via `localhost.run`.
- **Pure Python & Bash:** No shady binaries or third-party app installations needed.
- **Homelab Ready:** Perfect for turning old Android devices into zero-cost servers.

---

## 📥 Installation & Setup

Open your **Termux** app and run these commands:

```bash
git clone [https://github.com/miamuhammadmehedi/RuvCloud.git](https://github.com/YOUR_GITHUB_USERNAME/RuvCloud.git)
cd RuvCloud
chmod +x install.sh
./install.sh