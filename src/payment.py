import cv2
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "parking.db")

def process_payment(plate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT entry_time, status FROM entries WHERE plate = ? AND status = 'INSIDE'", (plate,))
    result = cursor.fetchone()
    
    if result:
        entry_time_str, status = result
        entry_time = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
        hours = (datetime.now() - entry_time).total_seconds() / 3600
        
        if hours <= 3:
            print(f"[INFO] Plate {plate} is within free period (Under 3h). No payment needed.")
        else:
            print(f"[PAYMENT] Plate {plate} owes fee. Processing...")
            cursor.execute("UPDATE entries SET status = 'PAID' WHERE plate = ? AND status = 'INSIDE'", (plate,))
            conn.commit()
            print("[SUCCESS] Payment complete.")
    else:
        print("[ERROR] No unpaid entry found for this plate.")
    conn.close()

def start_payment_scanner():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    print("[PAYMENT KIOSK] Scan your ticket QR code...")

    while True:
        ret, frame = cap.read()
        if not ret: break
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            plate = data.split('|')[0]
            process_payment(plate)
            cv2.waitKey(2000)
            break
        cv2.imshow("PAYMENT KIOSK", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_payment_scanner()