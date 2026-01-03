# Paid Autopark System

A plate recognition and QR-based automated parking management system.

## Overview

This project simulates a complete parking cycle including entry, payment, and exit. While the system could function using only a database, I implemented a physical ticket logic inspired by the Bursa Kent Meydanı AVM parking system. Upon entry, the system generates a PNG ticket with a QR code that must be scanned at the payment kiosk to authorize an exit.

## Features

* **Plate Recognition:** Automatic detection and reading of vehicle plates using OpenCV and Tesseract OCR.
* **Ticket Generation:** Creation of a PNG ticket with a QR code containing plate and entry time information.
* **Dynamic Pricing:** Free for the first 3 hours, with tiered pricing for longer durations.
* **QR Payment:** Digital scanning of the ticket to verify and update payment status.
* **Gate Control:** Exit system checks the database to ensure the 3-hour limit hasn't been exceeded or that payment has been made.

## Project Structure

* `src/`: Main application logic (Entry, Exit, Payment, Database).
* `test/`: Simulation tools for bulk data loading and QR testing without a camera.
* `data/`: CSV files for test data.
* `database/`: SQLite database storage.
* `output/`: Generated ticket images.

## Installation

```bash
git clone https://github.com/ismailoksuz/Paid-Autopark-System
cd Paid-Autopark-System
pip install -r requirements.txt

```

Note: Tesseract OCR must be installed on your system. Update the `tesseract_cmd` path in `prs.py` accordingly.

## Usage

1. **Entry:** Run `python3 src/prs.py` to start the entry camera.
2. **Payment:** Run `python3 src/payment.py` to scan the QR ticket.
3. **Exit:** Run `python3 src/exit.py` to verify status and open the gate.

## Author

ismailoksuz - https://github.com/ismailoksuz