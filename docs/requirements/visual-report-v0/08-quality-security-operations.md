# Video Visual Report V0 — Quality, Security, and Operations

## Implementation grade, allowed-use boundary, safety floor, deferred controls, and promotion triggers

V0 is a `G1 PROTOTYPE` for one owner and one local rights-restricted fixture. It
may prove rendering and visual value only. The safety floor is local-only data,
escaped text, contained asset paths, visible validation failures, zero external
requests, preserved attribution, and no changes to frozen P0-B history. Hosted
security, operational, commercial, and customer controls are deferred because no
service exists. Promotion to V1 requires explicit owner acceptance and authority.

## Service, customer/tenant, and target commercial-maturity model

No service, customer, tenant, account, commercial release, or support model.
Claims are limited to a locally reproducible prototype and owner-reviewed visual
quality.

## Workload and data-volume envelope

| Dimension | Normal | Peak | Growth horizon | Evidence |
|---|---|---|---|---|
| Concurrent users | 1 local owner | 1 | V0 only | Product boundary |
| Concurrent renders | 1 | 1 | V0 only | Synchronous CLI |
| Reports/run | 1 | 1 | V0 only | Fixed task |
| Plan size | 3–5 sections, bounded blocks | First report plus component fixture | Revisit for V1 | Schema/tests |
| Used images | 2–4 JPEG keyframes | 4 | Revisit for V1 | User requirement |
| Source video | Fixed about 34:53 fixture | Same | Future intended videos 10–30 min | Manifest and explicit exception |

## Latency and responsiveness

- On the owner's current Mac, validated plan/assets to HTML should complete in at
  most five seconds for the fixed fixture.
- A duration above ten seconds is a defect signal requiring diagnosis, not a
  reason to add queues, caching, or infrastructure.
- Browser layout should become usable immediately from local files; there is no
  deferred content loading or skeleton UI.

## Service levels, error/degradation budget, availability, correctness, freshness, durability, RPO, and RTO

| SLO ID | User workflow/indicator | Workload/window | Target | Measurement | Owner | Miss consequence |
|---|---|---|---|---|---|---|
| `Q-VR0-001` | Valid fixed-fixture render | One local run | Exit 0 and complete HTML | Command + integration test | Implementer | Remain in implementation |
| `Q-VR0-002` | Factual traceability | Final plan | 100% factual blocks have valid source refs | Contract/content review | Implementer/owner | Reject candidate |
| `Q-VR0-003` | Offline page | One desktop/mobile load | Zero automatic external requests | Browser inspection | Implementer | Reject candidate |
| `Q-VR0-004` | Responsive integrity | 1080 px and about 390 px | No clipping or horizontal overflow | Screenshots/browser | Implementer | Iterate design |
| `Q-VR0-005` | Prior artifact preservation | Induced failed rerender | Prior valid HTML not replaced by partial output | Recovery test | Implementer | Fix before review |

There is no availability percentage, RPO, RTO, durability, or service error
budget for a local prototype. Regeneration is the recovery method.

## Capacity controls, saturation, scale triggers, dependency degradation, and single points of failure

No capacity control or scaling layer. Missing local Python/uv, FFmpeg, source
files, or browser blocks the corresponding development step with a visible error.
The fixed local machine and source files are accepted prototype single points of
failure. They are not hidden behind fallbacks.

## Accessibility and compatibility

- Chinese-first semantic HTML with ordered headings and meaningful landmarks.
- Body text remains readable without shrinking to force a fixed height.
- Text/background contrast targets WCAG AA for normal text.
- Every informative frame has accurate Chinese alt text; purely decorative SVG
  is hidden from assistive technology.
- Keyboard focus is visible on any interactive element.
- `prefers-reduced-motion` disables any incidental transition; meaningful motion
  is not required.
- Verify the owner's installed Chromium-class browser or equivalent at 1080 px
  and about 390 px. Broad browser certification is not claimed.

## Privacy and compliance

The talk is public and is recorded as having no expected sensitive personal data,
but the local copy has no explicit open license. V0 therefore remains local and
non-public. No personal profile, analytics, tracking, remote processing, or new
regulated data is collected.

## Consent, withdrawal, protected records, and support access

No end-user consent or support-access workflow applies. Source-use withdrawal is
handled by stopping use and deleting derived V0 media/report artifacts. Frozen
P0-B evidence remains protected from mutation; legal deletion authority would
require a separate owner decision.

## Authentication, authorization, tenancy, secrets, and audit

Local filesystem access is the only authorization boundary. There is no login,
tenant, secret, token, or provider credential. The implementation task and status
history provide development evidence; no runtime audit system is added.

## Threats, abuse controls, and high-impact actions

| Threat/action | Control |
|---|---|
| Script/markup injection from plan text | Escape on every renderer path; tests with hostile strings |
| Path traversal or remote asset load | Relative contained paths only; reject URLs, absolute paths, `..` escapes |
| Broken output replacing a good report | Validate/render temporary sibling, replace only on success |
| Unsupported metric presented as fact | Source refs plus direct verification; omit ambiguity |
| Unauthorized publication | No hosting/export workflow; explicit local-only notices and task boundary |
| P0-B evidence contamination | Protected scope and diff review |

There are no financial, destructive, or external high-impact product actions.

## Cost budget and enforcement

Incremental provider/cloud cost is exactly zero because V0 permits no provider or
hosted infrastructure. Local compute and owner time are accepted prototype costs.
No metering system is added.

## Observability

| Signal | Measure | Trigger/symptom | Owner action |
|---|---|---|---|
| Render result | Exit code, elapsed time, counts, output path | Non-zero, >10 s, unexpected count | Diagnose and rerun explicitly |
| Contract quality | Targeted test results | Invalid case accepted or valid case rejected | Fix smallest contract/renderer issue |
| Visual integrity | Desktop/mobile screenshots | Overflow, weak hierarchy, illegible relation | Iterate CSS/component/plan |
| Offline integrity | Browser network inspection | Any automatic external request | Remove dependency/request |
| Content integrity | Source-ref/content review | Contradiction or ambiguous metric | Correct plan and rerender |

## Runtime events, append-oriented audit, redaction, and correlation

No runtime event system. The CLI prints concise operational facts without report
body, credentials, or media bytes. Task evidence is append-oriented by date and
uses the task ID as correlation. Historical failure entries are preserved.

## Alerts, runbooks, support, and incident response

No alerts or support operation. The runbook is the failure/recovery section in
the functional specification and bounded task. A local failure blocks owner
review until explicitly fixed; it is not a customer incident.

## Customer/tenant provisioning, entitlements, suspension, offboarding, export, and deletion

Not applicable. Local artifact deletion is the only offboarding action. Export or
publication of this fixture is prohibited.

## Service tiers, trials/sandboxes, quotas, metering, billing/refunds, and contractual commitments

Not applicable to `G1 PROTOTYPE`.

## Support severity, hours, response/restoration, escalation, and customer communication

No support commitment exists. The owner and implementation session collaborate
directly; unresolved authority/scope conflicts stop work for owner direction.

## Maintenance, release communication, compatibility, deprecation, and data portability

The V0 schema is provisional until the first accepted visual report. Changes
update plan/assets/tests/docs together. Release communication is the task/status
update and owner review. There is no external consumer compatibility or formal
deprecation. JSON and HTML remain locally inspectable.

## Backup, restore, and maintenance

Version control protects code/docs. Local ignored artifacts may be regenerated
from retained plan/assets/source; backup is owner-controlled. No scheduled
maintenance or restore drill is required.

## Performance, spike, soak, degradation, resilience, security, rollback, and restore test targets

- Record fixed-fixture render elapsed time; investigate above ten seconds.
- No spike or soak test beyond one report because concurrency is fixed at one.
- Induce invalid plan, missing asset, unsafe path, and output-failure cases.
- Verify repeat render determinism and prior-artifact preservation.
- Verify hostile authored strings remain inert.
- Verify final HTML at desktop/mobile and with zero automatic network requests.
- Verify source code diff does not alter protected P0-B contracts/history.
