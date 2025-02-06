# 📄 Project Documentation for Catcher

## 📝 Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Database Schema](#database-schema)
7. [Error Handling](#error-handling)
8. [Report Generation](#report-generation)
9. [Contributing](#contributing)

---

## 📌 Introduction

The **Catcher** is a Python-based client based bot using **Telethon** to monitor Telegram channels, extract product prices, convert them, and store them in **PostgreSQL**. It also generates reports and supports automation features.

---

## ✨ Features

✔️ Reads **channel usernames** from a txt file 

✔️ Monitors specified Telegram channels for **new messages**  

✔️ Extracts **prices (Toman)** and converts Rial to Toman

✔️ Saves extracted data to **PostgreSQL**  

✔️ Detects **phone numbers, links, and other details**  

✔️ Generates **CSV Reports**  

✔️ Automatically **joins new channels** on request (soon)

---

## Installation

### 1️⃣ Prerequisites

- Python 3.8+
- PostgreSQL
- Telethon
- Asyncpg

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/itisroach/catcher.git
cd catcher
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up PostgreSQL Database

Create a database and update the `.env` file with your credentials.

```sql
CREATE DATABASE your_db_name;
```

---

## ⚙️ Configuration

### 🔹 Database Config (`.env`)

```ini
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_HOST=localhost
DB_PORT=5432
```

### 🔹 Telegram API Config (`.env`)

You can get telegram API credentials from [here](https://core.telegram.org/api/obtaining_api_id)

```python
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
SESSION_NAME=your_session_name
```

---

## 🚀  Usage

### Run the Catcher

```bash
python main.py
```


### Adding New Channels

Modify the txt file `CHANNELS` list.

---

## 🗄️ Database Schema

| Column       | Type      | Description                                    |
|-------------|----------  |------------------------------                   |
| id          | SERIAL     | Primary Key                                     |
| channel     | TEXT       | Telegram channel username                       |
| message_id  | BIGINT     | Unique ID of the message                        |
| price_toman | BIGINT     | Price in Toman                                  |
| details     | TEXT       | Saves other info about products                 |
| post_link   | TEXT       | Saves the link to the Telegram Message          |
| websites_link   | TEXT (n:m relation)       | Saves links that was mentioned in the Telegram Message          |
| phone_numbers  | TEXT (n:m relation)       | Saves phone numbers that was mentioned in the Telegram Message          |
| time        | TIMESTAMP  | Date & time of the message                      |

---

## 🚨 Error Handling

- **Invalid Username** → Skips and logs error  
- **Invalid Price Format** → Skips message 
- **Database Connection Error** → Logs the Error connection automatically  

---

## 📊 Report Generation

### Generating CSV Reports

If you want to generate a csv report you can go to you telegram saved messages and then type report.

* You can type `report {channel_name}` to get all records with that channel name.
* You can type `report {date} {greater|less|equal(default)}` to get records by date. 

After that a .csv file will be sent to your saved message containg those reports.

---

## 👨‍💻 Contributing

1. Fork the repository  
2. Create a feature branch  
3. Commit changes  
4. Submit a pull request  



