/**
 * Canonical manifest constants for Cimeika frontend
 * Must match backend canon configuration
 */

export const CANON_BUNDLE_ID = "ci-canon-bundle-001";

export interface CanonManifest {
  canon_bundle_id: string;
  version: string;
  name: string;
  description: string;
  modules: string[];
}

export const CANON_MANIFEST: CanonManifest = {
  canon_bundle_id: CANON_BUNDLE_ID,
  version: "0.1.0",
  name: "Cimeika Unified",
  description: "Central ecosystem for Cimeika project",
  modules: [
    "ci",
    "kazkar",
    "podija",
    "nastrij",
    "malya",
    "gallery",
    "calendar"
  ]
};
