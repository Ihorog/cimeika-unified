# Orange Operator Axis MVP-1

**Status:** FACT / CONTROLLED SPEC  
**Date:** 2026-05-29  
**Repo:** `Ihorog/cimeika-unified`  
**Mode:** no-code planning artifact; this file defines the axis before executable implementation.

## 1. Core decision

Orange Pi is promoted from “device being researched” to **Orange Operator** — the local development-level Ci operator that holds one controlled axis for home/device/data orchestration.

**Canonical role:**

> Orange Operator = local sovereign control node that observes, normalizes, audits and routes authorized actions between voice/chat intent, AI consolidation, local devices, cloud bridges and storage.

This does **not** mean uncontrolled autonomy. It means one stable operator axis with permission layers, audit trail and explicit execution boundaries.

## 2. Current factual anchors

| Node | Current known state | Status |
|---|---:|---|
| Orange Pi 3 LTS | `orangepi3-lts` on local network | FACT |
| LAN IP | `192.168.1.132` observed for Orange Pi | FACT, may change by DHCP |
| Local API | `http://127.0.0.1:8000/health` returned operational state in prior test | FACT |
| LAN API | `http://192.168.1.132:8000` observed in node bootstrap | FACT, depends on LAN/IP |
| MCP tools service | local service `ci-orange-mcp-tools` on port `8798` returned health/status | FACT |
| Public MCP/tools bridge | `https://ci-tools.cimeika.com.ua/health` returned ok in prior test | FACT, should be rechecked before use |
| Cloudflare tunnel | tunnel exists; concrete identifier must stay in private config, not public docs | FACT / SECRET-HANDLING |
| Keenetic | router/storage/network bridge used for WebDAV/SMB/vault paths | FACT |
| Storage | Keenetic/WebDAV/SMB and Cimeika Vault are storage candidates | FACT + NEEDS CURRENT AUDIT |
| Samsung TV | used as display/audio/light panel; Tizen control explored | FACT |
| HDMI cable | Orange/TV physical media path exists conceptually as display/audio route | FACT / NEEDS CURRENT CHECK |
| Sonoff/eWeLink | channel 1 = TV power, channel 4 = separate light | FACT from user-defined home map |
| Supabase | external cloud data/service layer candidate | NEEDS CURRENT AUDIT |
| Cloudflare | public bridge, tunnel, DNS, workers possible | FACT + NEEDS CURRENT AUDIT |
| Voice conversation | primary intent input for controlling/manipulating data/devices through operator | CI-MODEL |

## 3. Operator boundary

Orange Operator must support three separate control layers:

| Layer | Purpose | Allowed by default |
|---|---|---|
| Observe | read status, ports, services, files, device state, logs | yes |
| Prepare | generate plan, command, patch, PR, issue, config proposal | yes |
| Execute | change device state, deploy, write config, switch power, run shell command, payment/action | only after explicit authorization |

Voice/chat intent enters the system as **intent**, not as automatic execution. The operator converts it into a controlled action packet.

## 4. Unified axis

All future Orange work must route through one axis:

```text
voice/chat intent
  -> Ci semantic normalization
  -> Orange Operator registry
  -> current-state audit
  -> permission check
  -> action packet
  -> execution bridge / tool / device API
  -> result verification
  -> memory node
```

No scattered manual control should become the default path. Manual terminal action remains fallback/debug only.

## 5. Registry model

Each node must become a stable registry item.

Minimum registry fields:

```yaml
id: stable machine-safe id
name: human-readable name
kind: device | service | port | storage | bridge | credential | action | activity
status: active | degraded | unknown | disabled
host: local/LAN/public address where applicable
port: port number where applicable
owner: user/local/system/external
permission_level: observe | prepare | execute
last_verified_at: timestamp
source: where the fact came from
risk: none | low | medium | high
notes: short factual note
```

## 6. Required first nodes

| ID | Kind | Role |
|---|---|---|
| `orange.node` | device | physical Orange Pi operator |
| `orange.api.local` | service | local Cimeika API |
| `orange.mcp.local` | service | local MCP/tools service |
| `cloudflare.tunnel.orange` | bridge | public tunnel to Orange tools/API |
| `keenetic.router` | network | router, LAN/DHCP/control surface |
| `keenetic.storage.webdav` | storage | WebDAV vault/storage path |
| `keenetic.storage.smb` | storage | SMB shares/vault path |
| `samsung.tv` | device | TV display/audio/control target |
| `hdmi.orange.tv` | cable/link | physical media route |
| `sonoff.ch1.tv_power` | power | TV power channel |
| `sonoff.ch4.light` | power | separate light channel |
| `ai.openai` | service | AI reasoning/consolidation layer |
| `ai.claude` | service | AI reasoning/consolidation layer |
| `supabase.project` | data | external data/backend candidate |
| `voice.intent` | input | spoken command/intention source |
| `github.repo.cimeika_unified` | memory/dev | controlled development memory |

## 7. Every correction becomes memory node

Rule:

> Every stable correction, fix, route, port, device state, command result or design decision becomes a versioned Orange memory node.

Memory node categories:

| Marker | Meaning |
|---|---|
| `FACT` | verified current fact |
| `EXPERIENCE` | repeated observed pattern |
| `CI-MODEL` | structured model / control logic |
| `SIMULATION` | proposed but not verified |
| `SECRET` | sensitive config/token/credential; never public |

## 8. Human participation target

The target user participation level is:

```text
one authorization click / one explicit spoken confirmation
```

Everything else should be prepared by the system: audit, plan, diff, rollback point, action packet and verification.

## 9. MVP-1 deliverables

MVP-1 is complete when the repo contains:

1. This operator-axis contract.
2. One Orange registry file with current known nodes.
3. One audit checklist for Orange/Keenetic/Cloudflare/Samsung/Sonoff/Supabase/storage.
4. One no-code action protocol for voice -> action packet -> authorization -> result.
5. One issue tracking implementation status.

## 10. Immediate next action

Create the first issue:

**MVP-1: Orange Operator Axis — registry, audit, authorization packet**

Acceptance criteria:

- Orange node registry exists.
- Public secrets are not exposed.
- Every known endpoint is marked as FACT / NEEDS CURRENT AUDIT / SECRET.
- Voice control is treated as intent input, not blind execution.
- Sonoff, Samsung TV, Keenetic, Cloudflare, MCP, storage and AI services are listed as operator nodes.
- No executable code is added until the axis and permission model are accepted.

## 11. Ci transition

| Було | Є | Буде |
|---|---|---|
| Orange as manually debugged device | Orange Operator as single controlled axis | authorized self-stabilizing local Ci operator |
| scattered ports and scripts | registry + audit + permission packet | voice-driven controlled execution bridge |
| manual memory in chat | repo-backed memory node | live adaptive device/data coordination |
