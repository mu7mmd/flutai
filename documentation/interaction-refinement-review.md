# FlutAI 0.6.0: detailed interaction review

This review covers the original multi-part UI request in the current conversation, its full-height correction, and the instruction to generalize and publish. It preserves each requirement separately, including exceptions and rejected interpretations. It does not replace the earlier M01–M31 casebook or claim that automatic host context compaction can be disabled. The rules were derived from the visible user requests and inspected implementation/validation evidence, not from an assumed acceptance of every intermediate patch. No private transcript, app source, environment settings, credentials, or native configuration is included in this package.

## Sections and ownership

| Section | Cases | Maintained instruction owner |
| --- | --- | --- |
| Inline audio and focus lifecycle | C01 | [Interaction lifecycle](../skills/flutter-coding/references/interaction-lifecycle.md#inline-recording-preserves-the-editing-focus-contract) |
| Active icon colors and border semantics | C02, C06 | [Design fidelity](../skills/flutter-coding/references/design-fidelity.md#icon-foreground-and-outline-semantics) |
| Async sheets and viewport geometry | C03 | [Scroll and overlays](../skills/flutter-coding/references/scroll-and-overlays.md#loading-item-sheets-occupy-the-full-available-height) |
| Tab gestures, indicator progress, route synchronization | C04 | [Scroll and overlays](../skills/flutter-coding/references/scroll-and-overlays.md#tabs-follow-the-page-including-during-a-gesture) |
| Dismissal state and navigation ownership | C05 | [Scroll and overlays](../skills/flutter-coding/references/scroll-and-overlays.md#audit-dismissal-at-launchers-and-callbacks) |
| Archive collection identity, read-only state, and action parity | C07–C09 | [Interaction lifecycle](../skills/flutter-coding/references/interaction-lifecycle.md#read-only-state-and-menu-parity-across-entry-points) and design fidelity |
| Semantic copy and localization | C10–C11 | [Localization](../skills/flutter-coding/references/localization-and-config.md#copy-must-describe-the-actual-interaction-and-state) |
| Dialog/sheet backdrop and interactive movement | C12–C13 | [Scroll and overlays](../skills/flutter-coding/references/scroll-and-overlays.md#overlay-motion-has-one-progress-source) |
| Learning scope, evidence, and publication | C14 | [Casebook](../skills/flutter-coding/references/owner-feedback-cases.md#october-7-follow-up-c01c14), this review, and [precision](../skills/flutter-coding/references/precision.md#check-the-transition-not-just-its-final-appearance) |

## 1. Recording is an inline editing operation

The requirement contains two independent failure opportunities: starting the microphone and pressing recording actions. Removing an unfocus call fixes only one. If the editor is replaced by a recorder widget, the active editing connection can still disappear; an outside-tap handler can also misclassify a recording control as external. The general rule therefore protects editor lifetime, focus state, and the action hit region together.

The inspected app changed the shared composer so the editor remained mounted while recording and removed recording-start unfocus. A recorder factory enabled tests without real native capture. That is a useful test seam, not a mandated public API for every Flutter app. Permission prompts, navigation, true modal opening, and explicit sending retain their own contracts. Starting recording with a closed keyboard must not be interpreted as a request to force it open.

Acceptance: focus survives mic tap and inline pause/resume/conversion/cancel; text remains editable after conversion; starting without focus does not steal it. Include rapid cancel/re-record and cleanup when the recorder itself changes. Do not claim physical keyboard or microphone correctness from fake-recorder tests alone.

## 2. Color identifies both role and availability

The two icon requests must be reconciled rather than applied as independent global replacements. The normal enabled icon uses the main theme foreground, which reads as black/white according to the selected palette. Gray still has a legitimate disabled/muted role. An explicitly colored outlined icon uses that semantic color for its border, while a normal foreground icon retains its neutral default outline. A contrasting filled action remains governed by the existing borderless-fill rule.

The implementation used the theme and shared icon/border helpers so drawer and composer callers inherited the change. The durable lesson is one semantic owner, not hardcoding white/black at every call site or recoloring all borders. Explicit destructive/accent states, disabled states, and supported caller overrides need separate verification.

Acceptance: inspect enabled normal, disabled normal, accent outline, destructive outline, and contrasting filled actions in both palettes. Equivalent callers must resolve the same roles without losing purposeful differences.

## 3. “Fixed” was explicitly clarified as full height

The first implementation reserved 85% for some list sheets, 75% for live thinking, and a 40%-screen project list. Those values made state changes more stable but did not satisfy the user's intended geometry. The correction explicitly requires the whole sheet to extend to the top. This is the central precedence decision of this review and is written into the operative sheet rule, not hidden in a historical note.

Full height is the available route viewport after safe-area and keyboard ownership. Loading, populated, empty, error, retry, search, and refresh do not select a different surface height. Keyboard or window changes can change the viewport itself. Static short forms remain content-sized; there is no authorization to make every modal full screen.

The project picker required a bounded list body between search and actions. Merely wrapping its previous inner fixed-height list in a larger surface would leave unused space and misplace actions. The shared shell was extended to allow the list to fill remaining space; the list owns scrolling, and its header/actions remain reachable. This is a layout ownership lesson, not a reason to build a new generic overlay framework.

Acceptance: measure top and bottom bounds with a top safe area and a nonzero keyboard inset in loading/data/empty/error states; scroll to the last item and reach confirmation. Avoid invalid fixture states that omit data required by the production pagination invariant.

## 4. Tab visuals must represent page progress

The user asked for default Flutter-like coordination and hand switching across tabbed views. An integer selected tab plus an independent indicator tween only approximates the final position. During a finger drag, the indicator must follow fractional page position; after reversal/cancel it must return with the page. Views that only replace one body through AnimatedSwitcher do not provide this contract.

The app connected real TabControllers to the shared tab bar and swipeable views in project, billing, contract detail/collections, files, calendar, and attachment flows. Main navigation required guarding programmatic synchronization separately: a route update during build must not trigger another route change, and a route update caused by a swipe must not jump the page to its integer position while the finger is still down.

Preserve independent tab queries/state and valid permission gates. Form value choices and buttons that open a separate activity route are not interchangeable with content tabs; classify them by their actual contract, and explicitly audit all requested tabbed views rather than silently excluding inconvenient callers. The earlier scoped immediate main-tab tap behavior is not the same as disabling finger switching.

Acceptance: pointer remains down at a fractional page value while indicator and page agree; test both directions, RTL/LTR, tap, reversal, settle, route identity, and retained drafts. Nested PageViews require selectors that identify the intended owner.

## 5. Optional, busy, and required are separate facts

A rename sheet may render an enabled X and a handle, while a constant launcher flag prohibits route dismissal. Inspecting only the button misses the cause. The request explicitly asks to audit sibling sheets, which makes caller coverage part of the task.

The app removed unconditional dismissal locks from rename and other optional idle forms. Existing request-state guards remained. The audit also found a callback that popped a second time after the shell already popped, risking departure from the parent screen. That finding supports one navigation owner per dismissal, not a blanket ban on cancel callbacks used for non-navigation cleanup.

Fetching selectable items does not automatically mean the user must remain in the sheet. Committing an operation may require a temporary lock; a truly required flow has a separate explicit product rule. Do not infer permanent mandatory status merely from auth or billing context.

Acceptance: close, cancel, outside, drag, and system back work while idle, block for the actual protected operation, unlock as appropriate on failure, and dismiss exactly one route. Keep required flows explicit and avoid advertising unusable exits.

## 6. Archive behavior spans collection, detail, and mutations

Three requests describe one mode contract: the collection identifies itself correctly, its title/search stay pinned, and an archived conversation has no input card and uses the same actions as its list entry. Fixing only the archive header leaves a detail composer capable of sending; fixing only the detail menu can lose the mode on refresh.

The app carried archive state into details, hid the full composer, guarded dispatch, shared icons/destructive styling, and updated an open detail after restore/archive or deletion. The reusable rule is end-to-end mode propagation and action parity. The concrete policy that archived chats are read-only remains Bayin-specific, and an app's real authoritative model/API must be consulted before designing another product's archive behavior.

Acceptance: list entry -> detail -> refresh preserves mode; no hidden alternate mic/attachment/send path remains; list and detail menus have the same valid actions for the same role/state; restore updates controls and collections; deletion leaves a valid destination. Check headers and search position while long lists scroll beneath them.

## 7. Wording is part of the interaction contract

A debounced search does not require pressing Search, even if a keyboard submit action is still supported. Remove that misleading instruction across the search family's callers and locales without silently changing debounce timing, clear handling, or valid manual submission. Prevent duplicate requests when debounce and submit meet.

Likewise, “Project context is ready” asserts a status that the requested neutral label “Project context” does not. All translations must reflect the same revised meaning. Update source catalogs and use the configured generator; do not hand-edit generated getters, rename API/storage fields, or hardcode language branches. The exact Arabic phrase is retained only as a scoped case.

Acceptance: no press-to-search requirement remains in debounced hints or locale fallbacks; readiness wording is removed from the relevant label in supported catalogs; actual search/submission semantics remain intact.

## 8. Backdrop timing is visible behavior

The user observed background filtering starting after the dialog appeared and asked for the same synchronized behavior during sheet dragging. A full-strength BackdropFilter hidden by an opacity animation is not necessarily the same as progressively changing its blur strength. Delayed timers or independent easing produce an observable mismatch even if the settled screenshot is correct.

The shared backdrop now receives progress for tint and blur. Dialog/sheet route progress drives opening/closing, and live sheet displacement contributes during drag. Cancelling returns both surface and backdrop together; dismissing continues in the release direction. A size read during build caused a regression during the implementation and was moved to a gesture-safe phase. This becomes a targeted lifecycle caution, not a mandate for a particular state-management or animation library.

Acceptance: compare intermediate frames of entry, exit, drag, cancellation, and a busy-state change; avoid bouncing to zero before dismissal. Profiling or a device run is still necessary before claiming smoother frame timing.

## Validation and release scope

The application work in this conversation reported 151 passing app tests before the final height clarification and seven focused passing sheet tests after that correction, with focused analysis clean for the height change. These are evidence about the app implementation and test harness, not evaluations of future model behavior under FlutAI 0.6.0. Earlier failed runs exposed real route/build-timing issues and an invalid fixture/native-test isolation issue; their corrections informed the acceptance cases above rather than being hidden as successful first attempts.

This release changes maintained instructions and their review documentation only. Validate manifest version/identity consistency, unchanged assets/default prompts/marketplace audience, skill frontmatter, local reference files and anchors, C01–C14 coverage, and whitespace. Preserve existing unrelated rules and historical precedence. Read back the published commit, tag, and GitHub Release separately. Installation/host reload and app/runtime validation are distinct claims; do not conflate them with publication.
