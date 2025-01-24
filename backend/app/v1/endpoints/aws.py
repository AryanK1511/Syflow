import json
import os
import subprocess

import jwt
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from backend.app.config import settings

app = FastAPI()
token_auth_scheme = HTTPBearer()


def set_up():
    """Sets up configuration for the app"""
    config = {
        "DOMAIN": settings.AUTH0_DOMAIN,  # Use settings.AUTH0_DOMAIN
        "API_AUDIENCE": settings.AUTH0_API_AUDIENCE,
        "ISSUER": settings.AUTH0_ISSUER,
        "ALGORITHMS": settings.AUTH0_ALGORITHMS,
    }
    return config


class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self, token, permissions=None, scopes=None):
        self.token = token
        self.permissions = permissions
        self.scopes = scopes
        self.config = set_up()

        # This gets the JWKS from a given URL and does processing so you can use any of
        # the keys available
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(self.token).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        if self.scopes:
            result = self._check_claims(payload, "scope", str, self.scopes.split(" "))
            if result.get("error"):
                return result

        if self.permissions:
            result = self._check_claims(payload, "permissions", list, self.permissions)
            if result.get("error"):
                return result

        return payload

    def _check_claims(self, payload, claim_name, claim_type, expected_value):
        instance_check = isinstance(payload[claim_name], claim_type)
        result = {"status": "success", "status_code": 200}

        payload_claim = payload[claim_name]

        if claim_name not in payload or not instance_check:
            result["status"] = "error"
            result["status_code"] = 400

            result["code"] = f"missing_{claim_name}"
            result["msg"] = f"No claim '{claim_name}' found in token."
            return result

        if claim_name == "scope":
            payload_claim = payload[claim_name].split(" ")

        for value in expected_value:
            if value not in payload_claim:
                result["status"] = "error"
                result["status_code"] = 403

                result["code"] = f"insufficient_{claim_name}"
                result["msg"] = (
                    f"Insufficient {claim_name} ({value}). You don't have "
                    "access to this resource"
                )
                return result
        return result


@app.get("/")
async def root():
    print(settings.AUTH0_DOMAIN)
    return {"message": "Hello World"}


@app.get("/api/private")
def private(response: Response, token: str = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    # result = {"status": "success"}
    return result


class ServerRequest(BaseModel):
    user_id: str
    server_name: str
    instance_type: str


@app.post("/provision_server")
def provision_server(req: ServerRequest):
    """
    Provisions a new Minecraft server EC2 instance for a given user
    and returns the public DNS/IP of the newly created instance.
    """

    tf_vars = {
        "TF_VAR_user_id": req.user_id,
        "TF_VAR_server_name": req.server_name,
        "TF_VAR_instance_type": req.instance_type,
    }

    env = os.environ.copy()
    env.update(tf_vars)

    tf_dir = "../automation/setup/provision-instances"  # The path where your Terraform files are

    # 3. Run Terraform init
    init_cmd = ["terraform", "init", "-input=false"]
    process_init = subprocess.run(
        init_cmd, cwd=tf_dir, env=env, capture_output=True, text=True
    )
    if process_init.returncode != 0:
        raise HTTPException(status_code=400, detail=process_init.stderr)

    # 4. Run Terraform apply (auto-approve for simplicity)
    apply_cmd = ["terraform", "apply", "-auto-approve", "-input=false"]
    process_apply = subprocess.run(
        apply_cmd, cwd=tf_dir, env=env, capture_output=True, text=True
    )
    if process_apply.returncode != 0:
        raise HTTPException(status_code=400, detail=process_apply.stderr)

    # 5. Extract outputs
    #    You can run 'terraform output -json' to get outputs in JSON.
    output_cmd = ["terraform", "output", "-json"]
    process_output = subprocess.run(
        output_cmd, cwd=tf_dir, env=env, capture_output=True, text=True
    )
    if process_output.returncode != 0:
        raise HTTPException(status_code=400, detail=process_output.stderr)

    try:
        outputs = json.loads(process_output.stdout)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Could not parse Terraform output.")

    public_dns = outputs.get("public_dns", {}).get("value", None)
    public_ip = outputs.get("public_ip", {}).get("value", None)

    if not public_dns:
        raise HTTPException(
            status_code=404, detail="Could not find instance DNS in Terraform output."
        )

    # 6. Return the server info to the user
    return {
        "message": "Minecraft server provisioned successfully!",
        "public_dns": public_dns,
        "public_ip": public_ip,
    }
