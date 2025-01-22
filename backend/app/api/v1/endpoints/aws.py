import json
import os
import subprocess

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class ServerRequest(BaseModel):
    user_id: str
    server_name: str
    instance_type: str


@router.post("/provision-server")
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
