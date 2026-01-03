import cv2
import pytesseract
import numpy as np
import os
from ticket import generate_ticket
from database import save_entry, init_db

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

last_plate = ""
repeat_count = 0
STABILITY_THRESHOLD = 5

init_db()

def detect_and_read_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blur, 30, 200)

    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 2.0 < aspect_ratio < 6.0:
                roi = gray[y:y+h, x:x+w]
                roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

                config = '--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                text = pytesseract.image_to_string(roi, config=config).strip()
                
                if len(text) > 5:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    return text, frame
                    
    return None, frame

def start_system():
    global last_plate, repeat_count
    cap = cv2.VideoCapture(0)
    
    print("[SYSTEM] Camera active. Scanning for plates...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        plate, frame = detect_and_read_plate(frame)

        if plate:
            if plate == last_plate:
                repeat_count += 1
            else:
                last_plate = plate
                repeat_count = 1
            
            if repeat_count == STABILITY_THRESHOLD:
                print(f"[EVENT] Confirmed Plate: {plate}")
                save_entry(plate)
                path = generate_ticket(plate)
                print(f"[EVENT] Ticket Generated: {path}")
                cv2.putText(frame, "TICKET PRINTED", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                repeat_count = 0 

        cv2.imshow("ISMAIL OKSUZ AUTOPARK SYSTEM", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_system()