"""
Canonical manifest for Cimeika Unified
Contains the canonical bundle identifier for the system

Based on CIMEIKA_CANON_TZ_v1.yaml
"""

# Canonical bundle identifier - CANON v1.0.0
CANON_BUNDLE_ID = "CIMEIKA_CANON_TZ_v1"
CANON_VERSION = "1.0.0"

# Core principles from CANON
CANON_PRINCIPLES = [
    "reality_first",
    "action_before_explanation",
    "one_entry_point",
    "no_psychology",
    "no_advice",
    "reaction_not_guidance",
    "minimal_surface_max_depth"
]

# Canonical manifest metadata
CANON_MANIFEST = {
    "canon_bundle_id": CANON_BUNDLE_ID,
    "version": CANON_VERSION,
    "name": "Cimeika",
    "entry_action": "Ci",
    "language": "uk",
    "status": "CANON",
    "description": "Ci is the action. Cimeika unfolds after.",
    "principles": CANON_PRINCIPLES,
    "modules": [
        "ci",
        "kazkar",
        "podija",
        "nastrij",
        "malya",
        "gallery",
        "calendar"
    ],
    "modules_unfolding": {
        "ci": "entry_action",
        "podija": "event_layer",
        "nastrij": "state_layer",
        "calendar": "time_layer",
        "kazkar": "narrative_layer",
        "gallery": "visual_trace",
        "malya": "variants_and_ideas"
    }
}
