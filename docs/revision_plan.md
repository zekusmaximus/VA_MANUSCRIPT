Verdant Accord — Revision Plan (v2, 90–95k target)

Scope

- Apply revisions and additions across `scenes/*.md`. Ignore `archive/`.
- Use the Scene Audit + index (see below) to map tasks to real files; this repo has more scenes than chapter count.

Word Count Plan

- Current: ~69.2k (scenes_inventory total)
- Target: 90–95k (+21–26k)
- Adds focus:
  - Nia subplot and flashbacks: +8–12k
  - Act II escalation set‑pieces (corridors, plateau, reactor thread): +6–8k (note: High Garden/plateau currently placed in Ch10; see Structure)
  - Climax (character‑driven seed run; council/corridor intercuts): +4–6k
  - Late‑act transformation with human‑level beats (Ch10–12, not a long tour): +4–6k
  - Tightening offsets (trim repetition/abstraction): −2–4k net

Scene Audit (Map Work to Files)

Create docs/scene_index.md (simple table) with the following columns and seed it with key anchors listed here; fill remaining rows from `scenes_inventory.md`:

- Columns: File | Chapter | Location | Function | Key Characters
- Example row: `scenes/ch04-sc02-shadows-in-the-grid.md | Ch4 | Reactor/Network | escalation | Amara, Kevin, Nia, Ravi`

Seed anchors (aligns tasks with existing files):

- Hands‑forward protocol: `scenes/ch05-sc07-fractured-alliances.md` | Ch5 | Hidden Garden (heart‑bed) | set‑piece + protocol codified | Nia, Amara, Elena, Maya, Seve, Lio (NIA‑HANDS‑FORWARD v1.0 present)
- Brightline pilot (proposal → pilot → debrief):
  - `scenes/ch08-sc02-growing-pains.md` | Ch8 | Brightline Tower (conference) | setup | Amara, Kevin, Marta, Kwan, Pilo
  - `scenes/ch08-sc03-growing-pains.md` | Ch8 | Brightline Corridor | set‑piece + escalation (closet clamp) | Amara, Kevin, Marta, Kwan, Pilo
  - `scenes/ch08-sc04-growing-pains.md` | Ch8 | Council Chamber | fallout + policy | Kwan, Marta, Concierge, Council
- High Garden (windows in wind): `scenes/ch10-sc02-resonance-patterns.md` | Ch10 | High Garden plateau bowl | set‑piece | Amara, Kevin, Kaito, High Garden crew
- Plateau clamp task force (Riya choice): `scenes/ch10-sc03-resonance-patterns.md` | Ch10 | Corridor plateau | set‑piece + escalation | Amara, Kevin, Riya, S‑SEC lead, Zara (beacons)
- Helios baseline snatch (heartbeat window): `scenes/ch06-sc02-the-corporate-agenda.md` | Ch6 | Helios / Council | set‑piece | Ravi, Jin, Amara (node cost, baselines captured)
- Reactor return (legacy handshake thread): `scenes/ch04-sc02-shadows-in-the-grid.md` | Ch4 | Reactor | escalation | Amara, Kevin, Nia, Ravi (expand with seed harmonic capture)
- Variance reservoirs/chorus (plan + usage):
  - Planning: `scenes/ch03-sc01/ch03-sc04-the-verdant-network.md` | Ch3 | Network | setup | Amara et al. (variance reservoirs called out)
  - Execution glimpses: `scenes/ch06-sc05-the-corporate-agenda.md`, `scenes/ch07-sc02/ch07-sc04-new-growth.md`

Also include the full list from `scenes_inventory.md` in `docs/scene_index.md` with empty Location/Function/Characters where unknown; fill progressively during the pass.

Structural Overview (Resolution Starts in Ch10)

- Act I (Ch1–2): Hook, anomaly, Solace permit, Sector 7 → Wasteland bridge.
- Act II‑A (Ch3–6): Network contact; ideological friction; hands‑forward protocol; reactor pursuit/drones; Helios baseline snatch; council/corridor prep.
- Act II‑B (Ch7–9): Brightline fallout and policy (Ch8); seed prep beats; global currents begin (tight vignettes in Ch9); Veltri doubt beats grow.
- Act III (Ch10–12): Climax and transformation. Note: High Garden bowl and Plateau clamp are currently in Ch10 as lead‑ins to the climax. Keep them in Ch10 (no need to move to Ch8–9) unless pagination demands earlier momentum.

Nia Subplot (Major Arc + Flashbacks)

Goal: Elevate Nia to a co‑protagonist in Act II, deepen stakes, add 8–12k of character‑driven science, sacrifice, and history.

Subplot Spine

- Past: Junior bio‑systems researcher during first build; clashed with early “acceptable variance” after a clinic’s bio‑layer was “rounded to zero.” Antagonist can be Veltri’s deputy or Veltri (match continuity as you draft).
- Present Wounds: Energy‑pulse injury damages her bio‑interface (pain on calibration; risk of permanent loss of her “botanical ear”).
- Agency: Nia originates “hands‑forward” and insists it becomes a formal playbook (NIA‑HANDS‑FORWARD v1.0); later scales it during the climax.
- Relationship Web: Apprentices (Maya/Seve/Lio) amplify her legacy; Elena counterbalances; Amara/Nia trust grows via triage/co‑design.
- Moral Turn: Choose between self‑preservation and leading a high‑risk live calibration for a pediatric/elder ward; she leads seated, with guardrails—codifying humane rules.
- Payoff: In the climax, Nia is the linchpin who keeps botanics breathing during the dampener wave; apprentices carry cadence when she must stop—legacy in action.

New Scenes/Expansions

- Flashback 1 (Ch3–4): “Pearl” district memory—bio‑layer mislabeled as fault; clinic dims to satisfy optics. Origin of her ethics.
  - Target: add as `scenes/ch03-sc08-nia-flashback-pearl.md` (or `ch04-sc05-...`), and cross‑reference briefly in `ch03-sc01` or `ch04-sc01`.
- Flashback 2 (post hands‑forward, Ch5): Early lab win; Veltri praising “trellis, not control.” Contrast later standardization.
  - Target: `scenes/ch05-sc08-nia-flashback-trellis.md` placed after `ch05-sc07`.
- Present‑line set‑piece (Ch5): Expand the heart‑bed (`ch05-sc07`) with a near‑syncope/tremor; codify on‑page guardrails: leader sits if wounded; add an in‑text protocol card kept on site.
- Pre‑climax (Ch6–7): Add an emergency “bio‑layer variance chorus” template that watchful communities can execute without specialists (kids’ shawls, elder watchers, janitor/concierge).
  - Target: `scenes/ch06-sc06-variance-chorus-template.md` (or `ch07-sc08-...`).
- Climax (Ch10): Nia orchestrates botanics across three districts via the chorus; cost = pain and temporary sensory loss; apprentices keep cadence when she must stop.
  - Anchor: weave into `ch10-sc03` intercuts and/or new `ch10-sc04` seed‑run scene (see Climax Redesign).

Veltri Arc (Foreshadow → Stand‑Down)

Micro‑beats to add:

- Ch4: Privately bookmarks the “UI glitch”/harmony spike; small frown. (Target: `ch04-sc02`)
- Ch5: Quietly overrides one minor clamp, logs “temporary; monitor.” (Target: `ch05-sc05` or `ch05-sc06`)
- Ch6: Watches Arc‑9 knot code on a split screen; whispers “acceptable… for whom?” (Target: `ch06-sc02`/`sc03`)
- Climax: Stands down countermeasures (no speech). Later, ties an “all’s well” knot under the rail; epilogue patch = variance amplifiers (“no keys”). (Present cue already in `ch07-sc02`: stands down Helios/council; reinforce in Ch10–12 epilogues.)

Climax Redesign (Character Action → Transformation)

Keep S7‑HELIOTROPIC.SEED as causal trigger (introduced conceptually in Ch2; make explicit in Reactor/Helios threads). Make the seed run the causal fulcrum, not a surprise awakening.

Team roles and existing anchors:

- Amara + Kevin: Infiltrate Helios/Solspire and plant the seed/harmonic key (Add new scene `scenes/ch10-sc04-seed-run.md`).
- Jin + Ravi: Time insertion to the dampener vulnerability window (heartbeat); pull/capture baselines (cost: a node goes dark). Anchors in `ch06-sc02`.
- Nia: Holds botanics stable through the dampener wave; executes variance chorus protocol at scale (intercut into `ch10-sc03` + new `ch10-sc04`).
- Riya Mandal (S‑SEC junior): Opens a micro‑window inside the lock; kills clamp nodes; uploads orders log (optics clause). Anchor in `ch10-sc03`.
- Veltri: Stands down countermeasures (chooses not to stop them) — reinforce in Ch10–12.

Stakes intercuts to show sensor‑level consequences (minimize abstraction):

- Arc‑9 med warmers; Brightline pilot corridor; a Tenebra pediatric cove; Hawkline valve heat trending down if chorus holds.
- Resolve with tangible telemetry: compressor load dips; tags tremor; shawls glow; infant stable.

Act II Escalations (Additions/Confirms)

- High Garden bowl (present in `ch10-sc02`): teach “windows” in wind; five‑beat windows for altitude storms; first drone pressure; elder Kaito’s ledger; child passes a “come back” knot. (Keep in Ch10 as lead‑in.)
- Plateau clamp task force (`ch10-sc03`): S‑SEC “stability enforcement” locks the corridor; Riya’s choice; watchers’ knot signals reach council; corridor learns around the lock; Solace logs become “too perfect to be true.”
- Brightline pilot (`ch08-sc02`–`sc04`): Concierge/Pilo/Kwan; closet clamp exposed; codify “windows are not faults” policy; watchers stipend; legacy key audits.
- Reactor return (expand `ch04-sc02` by 1–1.5k): Emphasize S7‑seed harmonic capture; show Amara + Kevin recording/validating thresholds; define seed as “legacy handshake to teach breath.”

Global Currents (Curate + Threaded Lead‑Up to Ch10)

- Goal: Preserve more of Ch9 while making each vignette carry either (a) direct lead‑up to the Ch10 climax, or (b) focused character development that pays off in Ch10–12. Target 1.6–2.2k net (from ~4.3k), by curating and rethreading, not flattening.
- Thematic threads to carry through Ch9 vignettes:
  1) Seed‑run prep signals: heartbeat window calibration, Helios baseline learnings propagating to field teams.
  2) Variance chorus dissemination: communities adopting kids’ shawls/root hubs/vent chorus with minimal guidance.
  3) Riya’s fracture: brief S‑SEC backchannel beats that establish her values and the ‘optics clause’ conflict.
  4) Veltri’s doubt: private observations of living systems choosing stability—silent micro‑choices that make her stand‑down credible.
  5) Stakes queue: Tenebra pediatric cove, Hawkline valve heat, Brightline corridor “window hours,” Arc‑9 med warmers—all trending and logged.
- Curated Ch9 mapping (proposed functions per file):
  - `ch09-sc01-global-currents.md` (setup): New Singapore crystal towers exchange light‑dream protocols with Luminara; Ravi/Jin use this to refine heartbeat vulnerability timing for seed‑run (explicit telemetry handoff).
  - `ch09-sc02-global-currents.md` (variance chorus): Tokyo tide‑islands + Wind Tribe: template uptake without specialists; brief call/response that echoes Nia’s upcoming Ch10 orchestration.
  - `ch09-sc03-global-currents.md` (Riya POV shard): S‑SEC internal memo + a ground‑level moment that exposes her discomfort with “forced baseline for optics.” Keep to ~200–300 words.
  - `ch09-sc04-global-currents.md` (Veltri micro‑beat): Watches knot‑code adoption and logs a “temporary allow” for a noncritical clamp elsewhere; no speech. (~200 words.)
  - `ch09-sc05-global-currents.md` (stakes queue): Montage of Tenebra/Hawkline/Brightline/Arc‑9 sensor deltas with one human beat each (concierge ‘all’s well’ knot; Asha prep; elder timing vent taps). (~400–600 words.)
  - `ch09-sc06-global-currents.md` (High Garden link): Message from Kaito offering five‑beat windows for altitude storms; Amara/Kevin accept and schedule route—direct hand‑off into Ch10 High Garden set‑piece. (~250 words.)
  - `ch09-sc07-global-currents.md` (closing tether): Short Network stand‑up aligning clocks, roles, and signals for Ch10; end on the heartbeat window. (~200–300 words.)
- Editing approach: reduce general “systems dream/celebrate” language; convert to causal, sensory beats that (a) teach something used in Ch10, or (b) deepen a character choice that lands in Ch10–12.

Tighten/Expand Pairs

- Tighten: Abstract transformation passages repeating “systems dream/play/celebrate.” Replace with concrete causal beats (rails warm, compressor down, knots tied, valves cool).
- Expand: Nia flashbacks + present‑line costs (+3–5k); action sequences (plateau, seed run, corridor holds) (+5–7k); human‑level stakes in climax (+1–2k); 2–3 epilogue vignettes (concierge, Asha, watcher/janitor kids) (+0.8–1.2k).

Per‑Chapter Intent (With Adds)

- Ch1–2: Keep hook; clarify S7‑HELIOTROPIC.SEED capture as concept in S7 thread; seed watchers/knot visually.
- Ch3: First Network entry; hold Kevin reveal until later in the scene; Nia/Elena skepticism; plant Flashback 1 teaser (Nia/Pearl).
- Ch4: Reactor stir; drones; Veltri 1st doubt beat; begin faction friction (Zara vs Serra vs Jin); expand reactor harmonic capture (seed basis).
- Ch5: Hands‑forward set‑piece expanded; NIA‑HANDS‑FORWARD v1.0 codified; Flashback 2 (Veltri praising trellis) added.
- Ch6–7: Helios baselines snatch; Brightline pilot + council debrief policy; Veltri 2nd doubt beat; add “variance chorus” template scene (`ch06-sc06` or `ch07-sc08`).
- Ch8–9: Keep Brightline fallout/policy (present). Curate Ch9 as threaded lead‑up: seed‑run prep, variance chorus dissemination, Riya fracture, Veltri doubt, and stakes queue—ending on heartbeat window sync.
- Ch10: Lead‑in set‑pieces (High Garden + Plateau) present; add seed‑run scene; intercut Nia’s chorus and district stakes; Riya choice; Veltri stands down.
- Ch11: Immediate aftermath (not a tour): Brightline breathes; Arc‑9 watchers; knot code enters policy.
- Ch12: Resolution (personal): Amara/Kevin (“city breathes without our hand”); Veltri variance amplifier patch (“no keys”); 2–3 human‑scale epilogues.

Continuity & Logic

- Watchers/knot code: Introduced early → formalized Ch5 → used Ch6–Ch10 → policy in Ch8 debrief and Ch11 aftermath.
- S7‑seed: Introduced in Ch2 conceptually → referenced during prep (Ch4/Ch6–Ch9) → deployed in Ch10 seed run.
- Costs visible: GHOST‑3/4; Nia pain/limits; a lost node; “we owe new eyes/relay.”
- Drones’ evolution: mimic → cope → participate.
- Constants/casing: S7‑HELIOTROPIC.SEED, GHOST‑3, NIA‑HANDS‑FORWARD v1.0.

Pass Plan

1) Scene index (docs/scene_index.md) seeded with anchors above + full list from scenes_inventory.
2) Nia subplot pass (add two flashbacks; expand heart‑bed costs; add variance‑chorus template; climax orchestration).
3) Escalation pass (confirm High Garden/Plateau placement in Ch10; expand Reactor harmonic/seed).
4) Brightline + policy pass (closet clamp; watcher stipend; “windows not faults” statute).
5) Climax rewrite (add seed run scene; intercuts; Riya/Veltri beats; tangible sensor‑level outcomes).
6) Global Currents curate (rethread seven scenes into 5–7 tight vignettes with explicit hooks into Ch10; aim for 1.6–2.2k total, prioritizing prep, character beats, and stakes).
7) Aftermath/resolution (Ch11–12 pacing; epilogue vignettes).
8) Trim redundancy (abstract passages) to offset additions; final continuity and word count (hit 90–95k).

Definition of Done

- Resolution begins in Ch10 (not earlier); Act II carries escalations and the Nia arc.
- Climax is character‑causal (seed run), not deus ex machina.
- Veltri’s turn is earned via earlier beats; stand‑down is a choice, not a speech.
- Nia subplot delivers emotional/thematic heft with real costs and legacy.
- Added word count meets 90–95k; tightening balanced with tangible new story.
