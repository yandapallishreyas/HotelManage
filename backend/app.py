from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Firebase Admin Initialization
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Room capacity
ROOM_LIMITS = {
    "Standard Non-AC": 2,
    "Standard AC": 2,
    "Suite Non-AC": 1,
    "Suite AC": 1
}

ROOM_PRICES = {
    "Standard Non-AC": 3500,
    "Standard AC": 4000,
    "Suite Non-AC": 4500,
    "Suite AC": 5000
}

@app.route("/book", methods=["POST"])
def book_room():
    data = request.json
    room_type = data.get("roomType")

    # Check availability
    room_ref = db.collection("bookings")
    bookings = room_ref.where("roomType", "==", room_type).stream()
    count = sum(1 for _ in bookings)

    if count >= ROOM_LIMITS[room_type]:
        return jsonify({"status": "fail", "message": "No rooms available for this type."}), 400

    # Add booking to Firestore
    doc_ref = room_ref.add(data)

    # Generate PDF
    pdf_filename = f"booking_{doc_ref[1].id}.pdf"
    os.makedirs("generated_pdfs", exist_ok=True)
    pdf_path = os.path.join("generated_pdfs", pdf_filename)
    generate_pdf(data, pdf_path)

    return jsonify({
        "status": "success",
        "message": "Booking confirmed!",
        "pdf": pdf_filename
    }), 200

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = os.path.join("generated_pdfs", filename)
    return send_file(file_path, as_attachment=True)

def generate_pdf(details, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Header
    c.setFillColor(colors.darkblue)
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)

    c.setFillColor(colors.whitesmoke)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width / 2, height - 50, "HOTEL VNR")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 70, "123 VNR Street, Hyderabad | 📞 +91-9876543210")

    # Confirmation title
    y = height - 120
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.green)
    c.drawCentredString(width / 2, y, "Reservation Confirmed")

    # Draw info box
    y -= 40
    box_top = y
    c.setFillColor(colors.whitesmoke)
    c.setStrokeColor(colors.grey)
    c.rect(50, y - 260, width - 100, 250, fill=True, stroke=True)

    labels = {
        "name": "Guest Name",
        "phone": "Phone Number",
        "address": "Address",
        "checkIn": "Check-In Date",
        "checkOut": "Check-Out Date",
        "roomType": "Room Type"
    }

    c.setFont("Helvetica", 12)
    y = box_top - 30
    for key in labels:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.darkblue)
        c.drawString(60, y, f"{labels[key]}:")
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(200, y, str(details.get(key, "N/A")))
        y -= 30

    price = ROOM_PRICES.get(details.get("roomType"), 0)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, "Room Charges (per night):")
    c.drawString(250, y, f"₹ {price}")
    y -= 40

    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, y, "This document is computer-generated and does not require a signature.")
    y -= 10
    c.drawCentredString(width / 2, y, "Please present it during check-in.")

    # Footer timestamp
    c.setFont("Helvetica", 8)
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    c.drawRightString(width - 50, 30, f"Generated on {now}")

    c.showPage()
    c.save()

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
