"""
Canonical manifest for Cimeika Unified
Contains the canonical bundle identifier for the system
"""

# Canonical bundle identifier
# This constant identifies the current canon version of the system
CANON_BUNDLE_ID = "ci-canon-bundle-001"

# Canonical manifest metadata
CANON_MANIFEST = {
    "canon_bundle_id": CANON_BUNDLE_ID,
    "version": "0.1.0",
    "name": "Cimeika Unified",
    "description": "Central ecosystem for Cimeika project",
    "modules": [
        "ci",
        "kazkar",
        "podija",
        "nastrij",
        "malya",
        "gallery",
        "calendar"
    ]
}
