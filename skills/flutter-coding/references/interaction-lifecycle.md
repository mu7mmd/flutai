# Interaction, navigation, and state lifecycle

Read for auth, chat/composer, audio, asynchronous lists, session changes, and behavioral redesigns. Use existing service/provider owners and [routing](routing.md); preserve the user's latest semantics literally. Concrete Bayin policies are scoped in [feedback cases](owner-feedback-cases.md).

## State identity is not visual identity

Share search UI and debounce mechanics, but isolate queries, pagination, selection, and controllers by independent context: drawer, projects page, project picker, attached-file picker, and project-specific lists. A family argument/scope should represent the real identity. Refresh affected collections after a mutation without overwriting another surface's query. Prevent an earlier request or page from overwriting a newer query/refresh/session; preserve retry and existing-data error behavior. Add sequencing guards only for actual races, not speculative infrastructure.

Use keys only for a concrete identity, reconciliation, animation, restoration, or test need. Do not sprinkle `UniqueKey`/`ValueKey` throughout ordinary static widgets or use random keys to reset state. Keep necessary route/page keys and reset entity-owned controllers/providers deliberately when the identity changes. New chat must not reuse the last chat's messages, ID, title, attachment, or pending send event.

Navigation is a contract: distinguish selecting a main tab, sliding between local detail tabs, opening an inner route, and replacing an already-open detail entity. Bottom navigation belongs to main screens; details and new chat use the inner stack when requested. Detail tabs such as chats/files/members slide within the same screen and retain the intended state. Do not push a new route per tab. When replacement is requested, replace an active chat/project detail of that kind; preserve normal entry/back behavior from other destinations. Do not use a global replace-everything shortcut.

Pass known title/model metadata immediately when opening details; reconcile it with authoritative loaded data. Support external links with only an ID and proper loading/error fallbacks. Returning to an already-current destination from an overlay may only need to close that overlay. Never infer an action from the mere presence of draft text on route entry, rebuild, or provider refresh; submission needs an explicit user event or an intentionally consumed one-shot launch action.

## Focus and keyboard transitions

Reuse the existing focus helper. Outside taps unfocus; prompt taps that fill the composer retain focus. For media/mode/model/credits overlays, capture whether the composer was focused, hide the keyboard, then restore only if that same live composer should regain it after closing. Do not force focus onto a changed/disposed route or keep the keyboard frozen beneath a modal.

Treat keyboard visibility, focus, and opening/closing direction separately. System back may hide a keyboard while the field retains focus. When the user requires immediate layout changes at dismissal start, react to focus loss or the first decreasing inset, not only `viewInsets.bottom == 0`. Keep that closing state through unchanged intermediate frames; handle a reversal to opening. Do not add an AnimatedSize delay to an explicitly immediate change. Validate actual intermediate frames in both Home and new-chat callers, not only the helper's final boolean.

Prompts use the real cached API data. When requested, show at most two horizontal rows with the keyboard closed and one row while opening/open. Horizontal scroll padding belongs inside the content. Preserve typing and prompt selection. Keep the field/actions gap token shared, and check composer translucency/halo in dark mode as well as light.

## Inline recording preserves the editing focus contract

Starting recording inside a focused composer must keep the keyboard open, and inline recording actions must not dismiss it. Apply this to mic tap/hold, pause/resume, stop/preview, conversion, and cancel/delete when those actions remain within the composer. Do not call the global unfocus helper simply because recording starts. Do not request focus when the keyboard was initially closed; preserve the user's starting state.

Trace both event handlers and widget lifecycle: replacing the focused text editor with a recorder disposes its editing connection even if no unfocus call remains. Keep that editor/controller/focus node alive through recording (for example offstage when appropriate), without showing duplicate fields or changing the draft identity. Include inline action hit regions in the editor's tap region so the outside-tap handler does not treat them as external interaction.

This is distinct from opening a genuine modal, navigating away, an explicit send policy, or a system microphone-permission dialog. Preserve the existing modal hide/restore contract and native permission semantics rather than forcing keyboard visibility across unrelated routes. Check focus while the action happens, not merely after reopening the editor. Test with an injectable recorder/service seam so native resources from one test cannot stall the next recording session.

## Authentication and session ownership

Differentiate an explicit login/register CTA from a protected-feature invitation. Direct login/profile entry takes the user directly to login; a protected feature can show the shared optional invitation sheet with login and create-account actions. Guest affordances requested by the owner remain actionable so they can explain the benefit, rather than becoming unexplained disabled controls. Include drawer, projects, new-chat More, and profile entry points in the caller audit.

Preserve login/register/OTP transitions and their specified animation. If a nonexistent account redirects to registration, explain why and preserve entered identity. Include independently clickable privacy/terms links where requested. Keep OTP country indicator and phone rendering, stable resend/countdown geometry, and stable email/phone field metrics. Transaction loading must use the common dismissal guard.

For local-first logout, capture the old session credential and repository before clearing the session. Clear local auth/user state immediately without a blocking spinner; send best-effort server logout using the old credential. A failed request must not restore the session or surface an error when the user explicitly requested silent best effort. This exception does not license swallowing normal API failures. Do not issue a logout request using a newly authenticated session's token.

Before explicitly resetting a provider, inspect reactive dependencies: if its build already watches auth, a second manual reset may duplicate work. Ensure persisted user removal belongs to session teardown, and pending user loads cannot repopulate data after logout or overwrite a new session. Do not remove real cleanup merely because `ref.watch` appears somewhere in the file.

For the requested authenticated-401 policy, reuse the app-level response listener. End the local session first, clear incompatible loading/overlays, navigate as required, then show the styled error dialog from a live context. Avoid repeated dialogs/logout loops from the same expired request or simultaneous failures; a guest 401 must not trigger another authenticated teardown. Respect any existing refresh/recovery contract and explicit policy before deciding which failure is terminal. Do not add a second per-screen interceptor or accidentally log out a new session because an old request completed late.

## Audio controls and async ownership

Correct recorder lifecycle before polishing it. Model the reachable states clearly: idle, starting/permission, recording, paused, stopped/playable, converting, sending, error/disposed. Tap starts a persistent recording; hold starts and release performs the requested stop/convert behavior. Support pause/resume, cancel/delete, stop/preview, and send as distinct user intents. Do not let a hold-release also trigger tap-send.

When requested, the lower stop/transcribe action stops recording and converts to editable text WITHOUT sending a message. Show conversion loading on that action. The upper playback control becomes play and the recording remains available until conversion completes. Explicit send is separate. Cancel followed immediately by record must await/serialize actual recorder stop/dispose where required, clear only its own state, and ignore obsolete callbacks. Avoid disposing native audio resources while a new operation still uses them; check mounted/liveness after awaits. Preserve recoverable text/audio on failure where appropriate.

Use the existing recording/transcription/playback services and shared icon/button states. Native recording, permissions, interruptions, and performance require real-device evidence; widget tests can verify callbacks/state races but not certify native audio behavior. Existing message playback may receive a translucent visual update without rewriting working playback logic.

## Read-only state and menu parity across entry points

A restricted mode must travel with the entity from collection entry into its detail state, survive relevant refreshes/rebuilds, and be updated when a mutation changes that mode. Do not infer it only from the collection title, a one-time widget flag that is lost on navigation, or a locally styled disabled button. Use the app's authoritative model/provider where available and preserve ID-only link loading; do not invent a backend status field.

Where the requested archive contract is read-only, hide the entire composer/input card, including attachments, microphone, send, and auxiliary input controls, and guard the send event boundary too. Re-entering, restoring, or archiving an already-open entity must produce the right controls; deleting the open entity must not leave an actionable deleted detail. Refresh affected collections without overwriting another collection's query state.

Use one action definition/behavior owner for the same entity mode in a row, drawer, and detail More menu. Keep icons, labels, ordering, destructive foreground, permissions, confirmations, and side effects consistent. Different roles still receive their valid action subset. A read-only archive policy belongs to the requesting app: some products legitimately allow editing archived items, so do not export Bayin's business policy as a universal meaning of “archive”.

## Conditional features and verification

Trace conditions from existing models/services rather than deriving entitlement, role, or subscription behavior from a label. Keep in-app billing management with the existing store helper; distinguish it from backend cancel/renew actions. Keep nullable versus required mode selection explicit in callers. Preserve descriptions and permission gates across all entry points.

Treat lexical and numeric version information separately when the app's update policy needs both. Leading-zero policies require the original version string before normalization. Test boundary values and required/optional/silent states without transplanting an app's release policy to another app.

Investigate lag with concrete traces and relevant profile/release/device checks when available. Avoid repeated expensive work, duplicate requests, whole-screen rebuilds, and competing animations in affected paths. Do not promise smoothness from debug runs or blame debug mode without measurement. Focused tests should exercise stale responses, re-entry without auto-send, isolated searches, overlay dismissal/focus restoration, and immediate keyboard-closing frames where relevant. Report exactly which evidence exists.
