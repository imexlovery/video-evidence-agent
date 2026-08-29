# P1 Data, Sources, State and Memory

## 1. Existing asset inventory

| ID | Status / location | Format / scale / quality | Owner, rights, allowed change, reuse | Gap / lifecycle |
| --- | --- | --- | --- | --- |
| ASSET-P1-001 | available: `eval/p0b/questions.jsonl`, `eval/p0b/gold.jsonl`, `eval/p0b/corpus.jsonl` | JSONL; 12 questions, 3 public technical videos; R3-evaluated | local Owner; source URLs/licenses recorded in corpus; read-only | reuse regression; hash in manifest; never relabel in place |
| ASSET-P1-002 | available: `artifacts/p0b-ingest/*/segments.jsonl` and manifests | 127 UTF-8 `VideoSegment`; frozen local derived data | local Owner; derived from authorized source videos; read-only | reuse, no ASR rerun; missing/hash drift blocks |
| ASSET-P1-003 | available: `reports/p0b-r3-retrieval-eval.*`, `docs/tasks/p0b-r3/final-report.json`, `artifacts/p0b/p0b-r3/` | R3 baseline/report/run artifacts; known fixed-set limitation | local Owner; immutable historical evidence | regression/baseline only; no rescore/overwrite |
| ASSET-P1-004 | expected from TASK-P1-010: P1 candidate/Gold manifest | 1..4 candidates; format defined by IN-P1-002 | Engineer drafts, Owner approves; new P1 revision only | delivery before B1 Headroom; absent blocks TASK-P1-020 |
| ASSET-P1-005 | no operational database/store | not applicable | DB/Redis/object store prohibited in P1 | G2 trigger only |
| ASSET-P1-006 | no new brand/creative assets | not applicable; existing source MP4 is data evidence, not UI creative | source media read-only; no editing | no creation/migration task |

## 2. Data-source register

| ID | Authority / rights | Contract, coverage and quality | Trust/freshness/lineage | Failure/reconciliation/lifecycle |
| --- | --- | --- | --- | --- |
| SRC-P1-001 Frozen segments | highest answer-evidence authority; local Owner; authorized technical-video derivation | `VideoSegment` vP0; one video/run; 127 across corpus; ASR/boundary errors known | prompt content is untrusted data; manifest sha256 is freshness; MP4→ASR→segments lineage | unavailable/hash drift stops; no second source fills gaps; immutable per revision |
| SRC-P1-002 Frozen question/Gold | question drives run; Gold highest scoring authority, never model context | JSONL contracts; 12 regression + 1..4 candidate; small/non-independent set disclosed | owner-approved freeze time/hash; poisoning risk from reverse-written candidates prevented by provenance review | malformed/conflict blocks freeze; correction creates new revision; retained with reports |
| SRC-P1-003 Text provider result | observation only, never policy/source authority | OpenAI-compatible structured action/proposal; exact model/config snapshot | external/untrusted; collected at run time; prompt/tool/version lineage in Trace | timeout/malformed fails revision; no auto retry; new authorized revision only |
| SRC-P1-004 P0 R3 reports | historical baseline authority | checked-in report plus artifacts; R3 fixed set near saturation | current checkout/hash recorded | contradiction resolved in favor of raw manifest/artifact; history retained |

Conflict rank: manifest/raw segment and Gold contracts > deterministic scorer/Gate > provider
output > narrative report. Gold disagreement or correction never mutates an evaluated revision.

## 3. Logical model and dictionary

- `DATA-P1-001 RevisionManifest`: revision ID, source commit, dependency lock hash, dataset/source/
  Gold hashes, prompt/model/tool/policy versions, budgets, authorization reference, created_at.
- `DATA-P1-002 RunState`: IN-P1-001 identity, canonical STATE, call count, normalized queries,
  seen segment map, trace step refs, terminal reason. Owner is runtime; one run only.
- `DATA-P1-003 ToolObservation`: action ID, validated args, source snapshot, ordered segment IDs,
  scores/relations, timing/status/error.
- `DATA-P1-004 EvidenceEligibility`: derived union of successful observation segment IDs with first
  seen step/source; cannot be written by model.
- `DATA-P1-005 ReviewRecord`: per-question correctness/support/refusal/dynamic-recovery labels,
  reviewer, rubric version, immutable acceptance time.

Every record is single-owner, single-project and non-sensitive. There is no tenant column because
multi-tenancy is prohibited rather than implicitly global.

## 4. Lineage

```text
authorized source MP4
 -> frozen P0 ASR/segmentation manifest
 -> SRC-P1-001 VideoSegment snapshot + sha256
 -> IN-P1-001 current-video question
 -> search/inspect validated observations
 -> DATA-P1-004 eligible evidence
 -> provider AnswerProposal/action
 -> deterministic Gate hydration
 -> OUT-P1-001 + OUT-P1-002
 -> scorer-only SRC-P1-002 Gold comparison
 -> Owner ReviewRecord
 -> OUT-P1-004 terminal decision
```

## 5. State, memory, retention and deletion

| Class | P1 use | Storage/lifetime | Access/deletion/recovery |
| --- | --- | --- | --- |
| Request context | question + current observations | in process; one run | runtime only; discarded after artifact commit |
| Session state | not applicable | none | no resume/cross-question context |
| Durable app data | not applicable | no DB | G2 promotion only |
| Cache | process-local TF-IDF computation allowed if semantically transparent | replaceable, run/revision scoped | key includes video/source/profile; delete anytime; no shared cache |
| Audit history | manifests, Trace, reports | append-oriented local files | Owner read/export; frozen acceptance history not overwritten |
| Conversation history | not applicable | none | not sent to model |
| Agent working memory | DATA-P1-002 run state | in memory + Trace; run lifetime | no hidden memory; failure does not resume |
| Long-term agent memory | not applicable | none | cross-run learning prohibited |

No credentials, hidden reasoning, whole concatenated transcript, Gold, user profiles, account data,
sensitive/regulated data, embeddings or model-training feedback are stored. No backup/restore
service is promised; reproducibility relies on Git contracts, local frozen assets and manifest
hashes. Owner-initiated cleanup may delete disposable failed/dev artifacts, but accepted frozen P0/
P1 evidence is protected by project governance and requires explicit archival decision.

## 6. Artifact contract

- `ART-P1-001 BaselineManifest`, `ART-P1-002 CandidateManifest`, `ART-P1-003 FormalManifest`,
  `ART-P1-004 RunBundle`, `ART-P1-005 FinalEvidencePack`.
- Each official manifest must include artifact type/version, sha256, run/revision, input snapshot,
  producer/tool/model/rule versions, MIME/size, validation status and relative path.
- Atomic write then manifest commit defines official status. Temporary/incomplete files are labeled
  partial and never included as successful evidence.
- Contract drift in question/Gold/segment/tool/prompt/model/policy hash stops the run. Reprocessing
  always emits a new revision, preserving old artifacts.

Consent/withdrawal and protected-record exceptions are not applicable because P1 prohibits
sensitive/regulated/customer data and has no other principal. If G2 introduces such data, consent
revision must enter cache/context/artifact keys and withdrawal must stop processing and propagate
to derived data before promotion.

