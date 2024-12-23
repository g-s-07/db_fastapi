

from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.auth.auth_bearer import JWTBearer
from exceptions.user import user_not_found_exception, incorrect_password_exception, user_already_exists_exception
import os
from app.database import get_db
from helpers.send_email import _send_email 
router = APIRouter()
from fastapi import FastAPI, File, UploadFile, Form
import httpx
from fastapi.responses import JSONResponse
from typing import Any, List, Dict


from typing import List

@router.post("/send_email/", dependencies=[Depends(JWTBearer())], tags=["general_api"],
             description=''' API for sending emails with optional file attachments, developed by Fenil Ponkiya (fenil.ponkiya@infoanalytica.com). This endpoint requires JWTBearer authentication and allows users to send an email with custom HTML content and multiple attachments. The API takes the following required parameters: 
- `sender_email` (str): The email address of the sender. 
- `receiver_email` (str): The email address of the recipient.
- `sender_password` (str): The password for the sender's email account for SMTP authentication.
- `subject` (str): The subject of the email.
- `html_content` (str): The HTML content to be sent as the body of the email.
- `file_attachments` (List[UploadFile], optional): A list of file attachments to include in the email. This parameter is optional and can accept multiple files.
'''

     )
async def send_email(
    sender_email: str = Form(...),
    receiver_email: str = Form(...),
    Cc_email: str = Form(None),
    Bcc_email: str = Form(None),
    sender_password: str = Form(...),
    subject: str = Form(...),   
    html_content: str = Form(...),
    file_attachments: List[UploadFile] = File(None)  # Accept multiple files
):  
    receiver_email_list  = receiver_email.split(",")
    if Cc_email: cc_email_list  = Cc_email.split(",") 
    else: cc_email_list = []
    if Bcc_email: bcc_email_list  = Bcc_email.split(",") 
    else : bcc_email_list = []
    attachments = []
    if file_attachments:
        for file_attachment in file_attachments:
            file_contents = await file_attachment.read()
            attachments.append((file_attachment.filename, file_contents))

    return _send_email(
        subject=subject,
        body=html_content,
        receiver_email=receiver_email_list,
        cc_email=cc_email_list,
        bcc_email=bcc_email_list,
        sender_email=sender_email,
        smtp_server=os.getenv("SMTP_SERVER"),
        smtp_port=os.getenv("SMTP_PORT"),
        smtp_password=sender_password,
        attachment_files=attachments  # Pass the list of attachments
    )

@router.post("/post_teams_notification/", dependencies=[Depends(JWTBearer())], tags=["general_api"],
             description='''API for posting notifications to Microsoft Teams using a webhook URL and adaptive card payload. Developed by Hetarthi Mori (hetarthi.mori@infoanalytica.com). This endpoint requires JWTBearer authentication. The API takes the following parameters:
- `webhook_url` (str): The webhook URL for posting the notification to Teams.
- `notification_payload` (Dict[str, Any]): The JSON payload representing the adaptive card to be sent as a notification to Teams.

The API uses the provided webhook to send the notification and returns a success message upon delivery. It handles errors and returns appropriate HTTP status codes for failed attempts.'''
)
async def send_adaptive_card_payload(request: Request, webhook_url: str = Body(..., embed=True), adaptive_card_payload: Dict[str, Any] = Body(..., embed=True)
):
    try:
        async with httpx.AsyncClient() as client:
            webhook_response = await client.post(
                webhook_url,
                json=adaptive_card_payload, 
                headers={'Content-Type': 'application/json'}
            )  
        if webhook_response.status_code not in(200,202) and webhook_response.text not in (200,202):
            raise HTTPException(status_code=webhook_response.status_code, detail="Failed to send data to webhook")
        return JSONResponse(content={"message": "Data sent to Teams successfully!!"})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))