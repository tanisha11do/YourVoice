from calle import CalleClient

from config import CALLE_API_KEY
from prompts import YOURVOICE_TASK
from schemas import YOURVOICE_RESULT_SCHEMA

def create_calle_client() -> CalleClient:
    return CalleClient(
        api_key=CALLE_API_KEY
    )


def prepare_call_payload(           #prepares structure to send to CALL-E for call response
    phone_number: str,
    campaign_id: str = "demo_001"
) -> dict:

    return {
        "task": YOURVOICE_TASK,
        "recipient": {
            "phone": phone_number,
            "region": "IN",
            "locale": "en-IN"
        },
        "result_schema": YOURVOICE_RESULT_SCHEMA,
        "metadata": {
            "project": "YourVoice",
            "campaign_id": campaign_id
        }
    }

def start_call(
    phone_number: str,
    campaign_id: str,
) -> dict:

    calle = create_calle_client()

    payload = prepare_call_payload(
        phone_number=phone_number,
        campaign_id=campaign_id
    )

    response = calle.calls.create(**payload)

    return response

def save_completed_call_to_supabase(
    calle_call: dict,
    supabase_client,
) -> str:
    
    if calle_call.get("status") != "completed":
        raise ValueError(
            f"CALL-E call is not completed. "
            f"Current status: {calle_call.get('status')}"
        )

    structured_result = calle_call.get("structured_result")

    if not structured_result:
        raise ValueError(
            "CALL-E call completed but has no structured_result."
        )

    recipients = calle_call.get("recipients", [])

    if not recipients:
        raise ValueError("CALL-E response contains no recipient.")

    recipient = recipients[0]

    phones = recipient.get("phones", [])

    if not phones:
        raise ValueError("CALL-E response contains no phone number.")

    calle_call_id = calle_call["id"]

    existing = (
        supabase_client
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

    campaign_response = (
        supabase_client
        .table("campaigns")
        .select("id")
        .eq("name", "YourVoice Community Needs Assessment")
        .limit(1)
        .execute()
    )

    if not campaign_response.data:
        raise ValueError(
            "YourVoice campaign was not found in Supabase."
        )

    campaign_uuid = campaign_response.data[0]["id"]

    call_data = {
        "calle_call_id": calle_call["id"],
        "campaign_id": campaign_uuid,
        "phone": phones[0],
        "consent": structured_result.get("consent"),
        "needs_help": structured_result.get("needs_help"),
        "previous_assistance": structured_result.get(
            "previous_assistance"
        ),
        "follow_up_requested": structured_result.get(
            "follow_up_requested"
        ),
        "additional_notes": structured_result.get(
            "additional_notes"
        ),
        "status": "completed",
    }

    
    response = (                        # insert call
        supabase_client
        .table("calls")
        .insert(call_data)
        .execute()
    )

    call_id = response.data[0]["id"]


    issues = structured_result.get("issues", [])   #insert individual issues

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
        (
            supabase_client
            .table("issues")
            .insert(issue_rows)
            .execute()
        )

    return call_id


def process_completed_call(
    call_id: str,
    supabase_client,
) -> str:

    calle = create_calle_client()

    call = calle.calls.get(call_id)

    print(f"CALL-E status: {call.get('status')}")

    saved_call_id = save_completed_call_to_supabase(
        call,
        supabase_client,
    )

    return saved_call_id