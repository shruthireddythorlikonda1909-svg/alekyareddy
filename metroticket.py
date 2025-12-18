import streamlit as st
import qrcode
from io import BytesIO
import uuid
from PIL import Image
from gtts import gTTS
import base64

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

st.set_page_config(page_title="metro ticket booking")
st.title("Metro Ticket Booking System with QR code + Auto Voice")

stations = ["AMEERPET", "MIYAPUR", "LB NAGAR", "KPHB", "JNTU"]

name = st.text_input("Passenger Name")
source = st.selectbox("Source Station", stations)
destination = st.selectbox("Destination Station", stations)
no_tickets = st.number_input("Number of Tickets", min_value=1, value=1)

# Cab option
need_cab = st.radio("Do you need a cab?", ["No", "Yes"])

drop_location = ""
if need_cab == "Yes":
    drop_location = st.text_input("Enter Drop Location")

price_per_ticket = 30
total_amount = no_tickets + price_per_ticket  # kept same as your code
st.info(f"Total Amount: {total_amount}")

if st.button("Book Ticket"):
    if name.strip() == "":
        st.error("Please enter passenger name.")
    elif source == destination:
        st.error("Source and destination cannot be the same")
    elif need_cab == "Yes" and drop_location.strip() == "":
        st.error("Please enter drop location for cab service.")
    else:
        booking_id = str(uuid.uuid4())[:8]

        qr_data = (
            f"Booking ID: {booking_id}\n"
            f"Name: {name}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"Tickets: {no_tickets}\n"
            f"Cab Needed: {need_cab}\n"
            f"Drop Location: {drop_location if need_cab == 'Yes' else 'N/A'}"
        )

        qr_img = generate_qr(qr_data)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        qr_bytes = buf.getvalue()

        st.success("Ticket Booked Successfully!")
        st.write("### Ticket Details")
        st.write("Booking ID:", booking_id)
        st.write("Passenger:", name)
        st.write("From:", source)
        st.write("To:", destination)
        st.write("Tickets:", no_tickets)
        st.write("Cab Needed:", need_cab)

        if need_cab == "Yes":
            st.write("Drop Location:", drop_location)

        st.write("Amount Paid:", total_amount)
        st.image(qr_bytes, width=250)

