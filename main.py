from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import resend # <- DINAGDAG KO TO

app = FastAPI()

# PAYAGAN NATIN YUNG PORTFOLIO WEBSITE MO NA MAG REQUEST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jvhluces.github.io"], # Ginawa ko na specific
    allow_methods=["POST"],
    allow_headers=["*"],
)

# GINAMIT NA NATIN RESEND IMbes NA GMAIL
resend.api_key = os.getenv("RESEND_API_KEY") # <- ITO YUNG ILALAGAY MO SA RENDER

@app.post("/contact")
async def contact_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Print sa Render Logs para macheck
    print("================== BAGONG MESSAGE ==================")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Message: {message}")
    print("====================================================")

    if not resend.api_key:
        return JSONResponse(
            status_code=503,
            content={"message": "Email service is not configured on the server."},
        )

    try:
        # SEND EMAIL GAMIT SI RESEND
        params = {
            "from": "Portfolio <onboarding@resend.dev>", # test email muna
            "to": ["janineluces49@gmail.com"], # EMAIL MO DITO
            "subject": f"New Portfolio Message from {name}",
            "html": f"""
            <h2>May bagong message sa Portfolio mo!</h2>
            <p><b>From:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Message:</b><br>{message}</p>
            """
        }
        
        resend.Emails.send(params)
        
        return JSONResponse(content={"message": "Email sent successfully!"})
        
    except Exception as e:
        print(f"EMAIL ERROR: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to send email. Check Resend API Key."},
        )
