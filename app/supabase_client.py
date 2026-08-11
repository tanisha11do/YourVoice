import os
from typing import Any

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


def create_supabase_client() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_PUBLISHABLE_KEY"]

    return create_client(url, key)

def save_call_result(           #actual function inserting data into supabase
    client: Client,
    *,
    calle_call_id: str,
    campaign_id: str,
    phone: str,
    result: dict[str, Any],
) -> str:

    existing = (
        client
        .table("calls")
        .select("id")
        .eq("calle_call_id", calle_call_id)
        .limit(1)
        .execute()
    )

    if existing.data:
        print(
            f"CALL-E call {calle_call_id} already exists. "
            "Skipping duplicate insert."
        )
        return existing.data[0]["id"]


    call_data = {
        "calle_call_id": calle_call_id,
        "campaign_id": campaign_id,
        "phone": phone,
        "consent": result.get("consent"),
        "needs_help": result.get("needs_help"),
        "previous_assistance": result.get("previous_assistance"),
        "follow_up_requested": result.get("follow_up_requested"),
        "additional_notes": result.get("additional_notes"),
        "status": "completed",
    }

    response = (
        client
        .table("calls")
        .insert(call_data)
        .execute()
    )

    call_id = response.data[0]["id"]

    issues = result.get("issues", [])

    if issues:
        issue_rows = [
            {
                "call_id": call_id,
                "category": issue["category"],
                "description": issue["description"],
                "severity": issue["severity"],
                "duration": issue["duration"],
            }
            for issue in issues
        ]

        client.table("issues").insert(issue_rows).execute()

    return call_id