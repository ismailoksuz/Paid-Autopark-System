import cv2
from datetime import datetime
from database import get_entry_full_info, remove_from_db
from prs import detect_and_read_plate

def calculate_fee(entry_time_str):
    entry_time = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
    duration = datetime.now() - entry_time
    hours = duration.total_seconds() / 3600
    
    if hours <= 3: return 0, True
    elif 3 < hours <= 4: return 100, False
    elif 4 < hours <= 6: return 200, False
    elif 6 < hours <= 12: return 300, False
    return 400, False

def start_exit_system():
    cap = cv2.VideoCapture(0)
    print("[EXIT SYSTEM] Camera active. Scanning plates for exit...")

    while True:
        ret, frame = cap.read()
        if not ret: break

        plate, frame = detect_and_read_plate(frame)

        if plate:
            info = get_entry_full_info(plate)
            if info:
                entry_time, status = info
                fee, is_free = calculate_fee(entry_time)
                
                if is_free:
                    print(f"[FREE PASS] Plate: {plate}. Duration < 3h. Gate Opening...")
                    remove_from_db(plate)
                    cv2.putText(frame, "FREE PASS - GATE OPEN", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                elif status == 'PAID':
                    print(f"[EXIT ALLOWED] Plate: {plate}. Payment verified. Gate Opening...")
                    remove_from_db(plate)
                    cv2.putText(frame, "PAID - GATE OPEN", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                else:
                    print(f"[PAYMENT REQUIRED] Plate: {plate}. Fee: {fee} TL. Status: {status}")
                    cv2.putText(frame, f"PAYMENT REQUIRED: {fee} TL", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            else:
                cv2.putText(frame, "UNKNOWN VEHICLE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow("EXIT CAMERA - ISMAIL OKSUZ SYSTEM", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_exit_system()