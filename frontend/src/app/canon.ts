/**
 * Canonical manifest constants for Cimeika frontend
 * Based on CIMEIKA_CANON_TZ_v1.yaml
 * Must match backend canon configuration
 */

export const CANON_BUNDLE_ID = "CIMEIKA_CANON_TZ_v1";
export const CANON_VERSION = "1.0.0";

export const CANON_PRINCIPLES = [
  "reality_first",
  "action_before_explanation",
  "one_entry_point",
  "no_psychology",
  "no_advice",
  "reaction_not_guidance",
  "minimal_surface_max_depth"
] as const;

export interface CanonManifest {
  canon_bundle_id: string;
  version: string;
  name: string;
  entry_action: string;
  language: string;
  status: string;
  description: string;
  principles: readonly string[];
  modules: string[];
  modules_unfolding: Record<string, string>;
}

export const CANON_MANIFEST: CanonManifest = {
  canon_bundle_id: CANON_BUNDLE_ID,
  version: CANON_VERSION,
  name: "Cimeika",
  entry_action: "Ci",
  language: "uk",
  status: "CANON",
  description: "Ci is the action. Cimeika unfolds after.",
  principles: CANON_PRINCIPLES,
  modules: [
    "ci",
    "kazkar",
    "podija",
    "nastrij",
    "malya",
    "gallery",
    "calendar"
  ],
  modules_unfolding: {
    ci: "entry_action",
    podija: "event_layer",
    nastrij: "state_layer",
    calendar: "time_layer",
    kazkar: "narrative_layer",
    gallery: "visual_trace",
    malya: "variants_and_ideas"
  }
};
