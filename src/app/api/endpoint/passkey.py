import base64
import uuid
from fastapi import APIRouter, Request
import webauthn
import os
import time
import json
from webauthn.helpers.structs import RegistrationCredential

from model.payload import PasskeyBeginPayload

route = APIRouter()

@route.post("/begin")
async def begin_passkey(request: Request, payload: PasskeyBeginPayload):
    id = uuid.uuid4()

    options = webauthn.generate_registration_options(
        rp_id=os.getenv("RP_ID"),
        rp_name=os.getenv("RP_NAME"),
        user_id=id.bytes,
        user_name=payload.username,
        timeout=int(time.time() * 1000) + 5 * 60 * 1000
    )

    challenge = base64.urlsafe_b64encode(options.challenge).decode()
    print(options.challenge)
    print(challenge)
    print(list(options.challenge))

    request.session["challenge"] = challenge

    opt = json.loads(webauthn.options_to_json(options))

    print(opt["challenge"])

    return opt

@route.post("/complete")
async def complete_passkey(request: Request):
    body = await request.json()

    print(json.dumps(body, indent=4))
    print(request.session["challenge"])
    print(list(base64.urlsafe_b64decode(body["challenge"])))

    verify = webauthn.verify_registration_response(
        credential=body,
        expected_challenge=base64.urlsafe_b64decode(request.session["challenge"]),
        expected_origin="http://localhost",
        expected_rp_id="localhost"
    )

    print(verify)

    return webauthn.options_to_json(verify)