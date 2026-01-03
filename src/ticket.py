import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def generate_ticket(plate):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "output")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime("%H:%M")
    
    qr_data = f"{plate}|{now.strftime('%Y%m%d%H%M%S')}"
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB').resize((280, 280))

    ticket = Image.new('RGB', (500, 800), color='white')
    draw = ImageDraw.Draw(ticket)
    
    draw.text((80, 40), "ISMAIL OKSUZ AUTOPARK SYSTEM", fill="black")
    ticket.paste(qr_img, (110, 100))
    
    draw.text((140, 420), f"PLATE: {plate}", fill="black")
    draw.line((50, 480, 450, 480), fill="black", width=3)
    
    draw.text((50, 520), f"DATE: {date_str}", fill="black")
    draw.text((50, 560), f"TIME: {time_str}", fill="black")
    draw.text((50, 620), "ENTRY: GATE A", fill="black")
    
    notice = "Do not fold the ticket.\nKeep away from sunlight."
    draw.text((50, 680), notice, fill="black")

    filename = os.path.join(output_dir, f"ticket_{plate}.png")
    ticket.save(filename)
    return filename