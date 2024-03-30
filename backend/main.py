import random
import math
import requests
import base64
import os
from urllib.parse import urlencode
from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
app = FastAPI()

load_dotenv()
origins = [
    "http://localhost:5173",  # Adjust this to the URL and port your frontend runs on
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


STATE_KEY = "spotify_auth_state"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
URI = os.getenv("URI")
FRONT_URI = os.getenv("FRONT_URI")
REDIRECT_URI = URI + "/callback"


def generate_random_string(string_length):
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    text = "".join(
        [
            possible[math.floor(random.random() * len(possible))]
            for i in range(string_length)
        ]
    )

    return text


@app.get("/login")
def login(response: Response):
    state = generate_random_string(20)

    scope = "user-read-private user-read-email user-read-recently-played user-top-read"

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "state": state,
    }
    response = RedirectResponse(
        url="https://accounts.spotify.com/authorize?" + urlencode(params)
    )
    response.set_cookie(key=STATE_KEY, value=state)
    return response


@app.get("/callback")
def callback(request: Request, response: Response):

    code = request.query_params["code"]
    state = request.query_params["state"]

    url = "https://accounts.spotify.com/api/token"
    request_string = CLIENT_ID + ":" + CLIENT_SECRET
    encoded_bytes = base64.b64encode(request_string.encode("utf-8"))
    encoded_string = str(encoded_bytes, "utf-8")
    header = {"Authorization": "Basic " + encoded_string}

    form_data = {
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    api_response = requests.post(url, data=form_data, headers=header)

    if api_response.status_code == 200:
        data = api_response.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        response = RedirectResponse(url=f"{FRONT_URI}/user_profile")
        response.set_cookie(key="accessToken", value=access_token)
        response.set_cookie(key="refreshToken", value=refresh_token)

    return response


@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    if request.cookies.get("accessToken"):
        access_token = request.cookies.get("accessToken")
        print("TRUEEEE")
        header = {"Authorization": "Bearer " + access_token}
        response = requests.get("https://api.spotify.com/v1/me", headers=header)
        
        # Print the entire raw response
        print(response.content)
        
        # For JSON responses, this is more useful:
        try:
            response_data = response.json()
            print(response_data)
        except ValueError:
            # In case the response is not in JSON format
            print("Response is not in JSON format.")
            print(response.text)
            
        # Depending on the successful API call, you might want to include the user's information in your response
        if response.status_code == 200:
            # Example: Extracting and using the display name from Spotify's response
            user_display_name = response_data.get("display_name", "User")
            return f"Welcome! Identified as {user_display_name}"
        else:
            return "Welcome! Could not retrieve user details."
    else:
        print("FAAAALSE")
        return "Welcome!"


@app.get("/user")
def get_user(request: Request):
    access_token = request.cookies.get("accessToken")

    # Check if the access token is None
    if access_token is None:
        raise HTTPException(status_code=401, detail="Access token is missing")

    header = {"Authorization": f"Bearer {access_token}"}

    url = "https://api.spotify.com/v1/me"

    response = requests.get(url, headers=header)

    # Add additional error handling, e.g., checking response status
    if response.status_code != 200:
        # You can customize the response based on the actual error
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve user data from Spotify")

    # Assuming response is JSON
    return response.json()

@app.get("/refresh_token")
def refresh_token(request: Request):

    refresh_token = request.query_params["refresh_token"]
    request_string = CLIENT_ID + ":" + CLIENT_SECRET
    encoded_bytes = base64.b64encode(request_string.encode("utf-8"))
    encoded_string = str(encoded_bytes, "utf-8")
    header = {"Authorization": "Basic " + encoded_string}

    form_data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    url = "https://accounts.spotify.com/api/token"

    response = requests.post(url, data=form_data, headers=header)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error with refresh token")
    else:
        data = response.json()
        access_token = data["access_token"]

        return {"access_token": access_token}