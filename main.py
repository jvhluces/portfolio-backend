from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# PAYAGAN NATIN YUNG PORTFOLIO WEBSITE MO NA MAG REQUEST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or lagay mo "https://janineluces.github.io"
    allow_methods=["POST"],
)

# ITO YUNG EMAIL MO NA PADADALHAN NG MESSAGE
YOUR_EMAIL = os.getenv("YOUR_EMAIL", "janineluces49@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.post("/contact")
async def contact_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    if not EMAIL_PASSWORD:
        return JSONResponse(
            status_code=500,
            content={"message": "Email service is not configured."},
        )

    subject = f"New Portfolio Message from {name}"
    body = f"""
    Name: {name}
    Email: {email}
    Message: {message}
    """
    
    # SEND EMAIL SAYO
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = YOUR_EMAIL
    msg["Reply-To"] = email
    msg["To"] = YOUR_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(YOUR_EMAIL, EMAIL_PASSWORD)
        server.sendmail(YOUR_EMAIL, [YOUR_EMAIL], msg.as_string())

    return JSONResponse(content={"message": "Email sent successfully!"})