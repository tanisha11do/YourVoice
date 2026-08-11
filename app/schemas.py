YOURVOICE_RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "consent": {
            "type": "string",
            "enum": ["yes", "no"]
        },
        "needs_help": {
            "type": "string",
            "enum": ["yes", "no", "unknown"]
        },
        "issues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": [
                            "food",
                            "water",
                            "electricity",
                            "housing",
                            "transport",
                            "employment",
                            "other"
                        ]
                    },
                    "description": {
                        "type": "string"
                    },
                    "severity": {
                        "type": "string",
                        "enum": [
                            "low",
                            "medium",
                            "high",
                            "unknown"
                        ]
                    },
                    "duration": {
                        "type": "string"
                    }
                },
                "required": [
                    "category",
                    "description",
                    "severity",
                    "duration"
                ]
            }
        },
        "previous_assistance": {
            "type": "string",
            "enum": ["yes", "no", "unknown"]
        },
        "follow_up_requested": {
            "type": "string",
            "enum": ["yes", "no", "unknown"]
        },
        "additional_notes": {
            "type": "string"
        }
    },
    "required": [
        "consent",
        "needs_help",
        "issues",
        "previous_assistance",
        "follow_up_requested",
        "additional_notes"
    ]
}