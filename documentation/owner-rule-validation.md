# Owner-rule release review: 0.5.0

This release updates instructions, not the Flutter application. The review used 31 original owner-message records, including amended messages and adjacent architecture/dependency context, plus four stages of the app's design/migration Git history. The [casebook](../skills/flutter-coding/references/owner-feedback-cases.md) maps every record to its effective requirements. Private transcripts, app source, environment overrides, and credentials are not included in the plugin.

Two manual edits were explicitly attributed by the owner: removing accent-button borders and removing a redundant user-provider reset while moving persisted-user cleanup to session teardown. Source/history support those behaviors. Other changes were reviewed as code evidence without assuming who typed each line. A current local environment override is not adopted as a new coding convention.

## Instruction acceptance scenarios

These are manual checks of the written rules, not claims of model-evaluation runs or runtime Flutter tests.

| Scenario | Required outcome covered by the rules |
| --- | --- |
| Full archive redesign with existing backend | Exact design reference; real integrations retained; only unavailable behavior stays static with TODO. |
| Same search in drawer and projects | One search component/debounce; independent query and pagination state; old responses cannot overwrite current data. |
| Repeated row/header/action designs | Same concrete owner/defaults; actual differences passed as parameters; full-surface ink and matching heights. |
| Filled accent versus white social versus idle mic | Borderless accent; shared visible outline for low-contrast fill and outlined controls. |
| Short/long optional sheet, then submit | Content height until constrained; header/search pinned; X/outside/drag/back work idle and block during required loading. |
| Scroll beneath a pinned tab/search | Initial body gap scrolls away; pinned top clearance remains; no permanent blank band after the pin. |
| Drawer and horizontal prompt safe spacing | Viewport reaches its edge; safe/device padding is internal content, applied once. |
| Keyboard starts closing with focus retained | Two-row prompts restore on first decreasing nonzero inset without a resize delay. |
| Prompt tap versus mode/credits overlay | Prompt retains focus; modal hides keyboard then restores the eligible prior composer. |
| Active detail changed versus main tab changed | Requested same-kind replacement; separate main-shell and inner routes; local project tabs slide without routes. |
| New chat opened after an existing draft | New identity; no inferred submit; immediate known title then authoritative metadata reconciliation. |
| Cancel recording and immediately record again | Correct cleanup sequencing; obsolete callbacks ignored; conversion and send remain distinct. |
| Logout server fails or user request finishes late | Immediate local logout remains final; no best-effort error UI; old response cannot restore the user. |
| Authenticated 401 and repeated failures | Central listener tears down once before showing an error; guest/new-session paths do not loop. |
| Guest feature versus explicit login | Feature opens invitation; explicit login/profile opens login; register is separately available. |
| Loading card or message | Skeleton shares actual geometry, theme, RTL, and reduced-motion treatment. |
| IAP next subscription versus backend plan | Existing store helper and source conditions; Bayin-specific policy stays scoped. |
| Original version 1.2.03 versus 1.2.0 | Multi-digit zero prefix survives parsing for the scoped policy; single zero does not suppress by itself. |
| Promote lib2 and rename shared classes | One canonical tree/token owner; exception preserved; no storage/API/brand contract rename. |
| Native dependency mismatch in historical context | Diagnose it; do not silently change deployment settings or treat an error log as approval. |
| Learn from a manually edited commit | Explicit attribution or evidence required; latest user decision wins; no inferred acceptance from silence. |

## Package and publication checks

Validate both manifest versions/identity and preserve default prompts, branding assets, and marketplace identity. Validate local links/anchors, skill frontmatter, package inventory, whitespace, and full M01–M31 coverage. Existing coding/architecture rules remain linked; new task-specific references are required from the main skill. Validate the committed package again before publication.

Verify Git remote main, tag, and published Release separately. Verify installed version and enabled state separately from publication. A new host session/restart is required to load refreshed installed instructions. Package validation and these instruction checks do not prove future generated UI, live APIs, native audio, real-device performance, or that every independent client has refreshed.
