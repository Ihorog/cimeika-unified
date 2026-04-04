#!/usr/bin/env bash
set -Eeuo pipefail

BASE="${1:-/storage/emulated/0/1/repo}"

CORE="$BASE/cimeika-unified-main"
INFRA="$BASE/ci_gitapi-main"
EDGE="$BASE/cimeika-backend-main"

echo "=== CIMEIKA CROSS-REPO VERIFY ==="
echo "BASE: $BASE"
echo

check() {
  local path="$1"
  if [ -e "$path" ]; then
    echo "[PASS] $path"
  else
    echo "[FAIL] $path"
    return 1
  fi
}

FAIL=0

check "$CORE/manifests/repo-role-manifest.yaml" || FAIL=1
check "$CORE/manifests/path-status-manifest.yaml" || FAIL=1
check "$CORE/manifests/repo-conflict-manifest.yaml" || FAIL=1
check "$CORE/manifests/freeze-plan.yaml" || FAIL=1
check "$CORE/manifests/repo-sync-policy.yaml" || FAIL=1
check "$CORE/manifests/unified-execution-manifest.yaml" || FAIL=1
check "$CORE/manifests/repo-ownership-manifest.yaml" || FAIL=1
check "$CORE/docs/processes/canonical-decision-record.md" || FAIL=1
check "$CORE/docs/processes/github-dev-contour.md" || FAIL=1
check "$CORE/docs/processes/delegated-execution.md" || FAIL=1
check "$CORE/.github/workflows/_reusable-ci.yml" || FAIL=1
check "$CORE/.github/workflows/dev-contour.yml" || FAIL=1
check "$CORE/.github/workflows/docs-drift.yml" || FAIL=1
check "$CORE/.github/workflows/repo-topology-check.yml" || FAIL=1
check "$CORE/.github/workflows/nightly-health-governance.yml" || FAIL=1
check "$CORE/.github/ISSUE_TEMPLATE/delegated-task.yml" || FAIL=1
check "$CORE/.github/dependabot.yml" || FAIL=1

check "$INFRA/manifests/repo-identity.yaml" || FAIL=1
check "$INFRA/manifests/repo-boundary.yaml" || FAIL=1
check "$INFRA/docs/processes/infra-role.md" || FAIL=1
check "$INFRA/.github/workflows/_reusable-infra-ci.yml" || FAIL=1
check "$INFRA/.github/workflows/registry-validate.yml" || FAIL=1
check "$INFRA/.github/workflows/failover-audit.yml" || FAIL=1
check "$INFRA/.github/workflows/control-plane-check.yml" || FAIL=1

check "$EDGE/manifests/repo-identity.yaml" || FAIL=1
check "$EDGE/manifests/repo-boundary.yaml" || FAIL=1
check "$EDGE/docs/processes/edge-role.md" || FAIL=1
check "$EDGE/.github/workflows/edge-ci.yml" || FAIL=1
check "$EDGE/.github/workflows/worker-dev-check.yml" || FAIL=1
check "$EDGE/.github/workflows/edge-health-smoke.yml" || FAIL=1

echo
if [ "$FAIL" -eq 0 ]; then
  echo "RESULT: PASS"
else
  echo "RESULT: FAIL"
  exit 1
fi
