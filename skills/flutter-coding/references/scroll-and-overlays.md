# Scrolling, insets, and overlay contracts

Read for any scroll, sheet, dialog, popup, tab, keyboard-inset, or inner-screen layout change. Pair with [design fidelity](design-fidelity.md). Apply one shared implementation and test its representative callers.

## Own each inset once

Distinguish device safe padding, keyboard view insets, design spacing, and persistent chrome. The owner's baseline is a named 24px horizontal page/sheet inset, device bottom padding plus 8px, and a 16px inner-header/body gap. Current target design or explicit user values can override these centrally. Do not add another arbitrary bottom margin or count a SafeArea twice. Expose optional top/start/end handling on the shared safe-area component; keep keyboard avoidance separate so the keyboard and device insets are not double-counted.

For a scrolling body, put leading/trailing and bottom safe padding INSIDE the scroll content. The viewport extends to its intended edge and items scroll through the padded area. This applies to drawers, lists, sheets, horizontal prompt rows, tab strips, and page views. Wrapping a viewport with the same padding is observably different. Give horizontal scrolling its directional/device insets through content padding or equivalent slivers; do not crop its scrollable start/end region with an outer padded box.

The initial 16px below an inner header belongs to the scrolling body. When a tab/search/control becomes pinned, keep the specified 16px between that pinned control and the app bar. The gap AFTER the pinned tab/search belongs to the scrolling body and scrolls away: content should pass directly beneath the pinned control, with clipping/overlap ownership correct. Do not pin that trailing gap as a permanent empty band. Inspect long and short content, both scroll directions, and every tab.

For greeting/composer layouts, let flexible empty space shrink before enabling scrolling; do not reserve an unnecessary scroll region while ample space remains. Preserve the minimum shared gap once content meets. Keep save/actions in the appropriate scroll content unless explicitly pinned; any genuinely pinned action still uses the one bottom-safe-area contract.

## One sheet presentation path

Use one sheet launcher/route, surface, backdrop/barrier, radius, handle, header, close button, action layout, transition timing, and result contract. Auth, attach file/contract, new project, options, language, credits, feedback, and update flows must use that path or a deliberate reusable specialization. Never stack two drag handles or mix a native default sheet with a separately styled custom overlay accidentally.

Static short sheets default to content sizing, constrained by available height; long content scrolls. Loading-item sheets use the full-height contract below. Pin the title/close header and any search field beneath it while only the body scrolls. Use the same close icon component in auth and all other optional sheets. A centered brand header may be an explicitly supplied header variant. Body descriptions align with the title's start unless the supplied design specifies a different alignment. Place the overlay above the root shell so bottom navigation cannot cover language/options menus or block their last items.

For this owner's redesign workflow, use sheets for menus, selection popups, forms, and confirmations; preserve error/success/info alert dialogs with the new common alert style. An explicitly requested exception, such as release notes in an update sheet, wins. Preserve each original callback, selected value, typed return result, and permission condition. When asked for an app-wide migration, inventory every invocation and report converted surfaces with source links; do not migrate only the component class while leaving old launchers.

When confirm and cancel share a row, confirm takes the remaining width and cancel takes its content width. Preserve readable labels at supported text sizes and directional order; constrain or adapt only where necessary. Use shared button states, not feature-specific lookalikes.

## Loading-item sheets occupy the full available height

For this owner's workflow, sheets that load item collections occupy the entire available sheet viewport from its bottom boundary to the top safe area. Keep that same extent for initial loading, populated data, empty results, failure/retry, filtering, and refresh. **Fixed height here means full available height, not a fixed fraction such as 75% or 85%, and not a fixed-height list inside a shorter sheet.** This is the owner's explicit clarification of the earlier “fixed” request. Static short forms and simple choice sheets retain content sizing unless separately requested otherwise.

Compute the extent from the launcher's actual layout constraints after its single safe-area/keyboard adjustment. Do not multiply the physical screen height by a guessed percentage or count insets again inside the child. Keyboard opening, orientation, and window resizing can legitimately change available height; asynchronous item state must not. The surface itself reaches the top boundary, even with zero items.

Keep title/close and search pinned. Let the list fill the remaining bounded space and own its scroll, while required action buttons remain reachable. Expose an explicit expanded-body slot/variant in the existing shared shell for a picker with actions; do not put an Expanded into an unbounded SingleChildScrollView or invent a second sheet framework. Avoid reserving a guessed item height that leaves a large unused region or pushes confirmation offscreen. Audit all loading-item sheets, not just the example first reported.

## Tabs follow the page, including during a gesture

Every actual tabbed content view supports both tab taps and hand swipes unless the current user explicitly requires a restriction. Sharing a tab-shaped visual alone does not implement a tab view. Inventory detail, collection, billing, attachment, and other reachable tabbed views; do not fix one TabBarView while equivalent views still replace children with AnimatedSwitcher or disable horizontal scrolling.

Use one controller/animation source for page position and tab indicator progress. A custom indicator follows the controller's fractional animation value during drag, tap animation, cancellation, and settling. An integer selected index plus a separate AnimatedPositioned animation visibly lags or jumps and is not equivalent to Flutter's default TabBar/TabBarView contract. Preserve text direction and state/controller disposal.

Distinguish tabbed content from a form choice or an action that opens another route. Preserve actual validation/permission gates; do not convert an activity action into an empty swipe page. This distinction must follow the control's behavior, not be used to exempt a requested tabbed view. Check the full caller inventory and disclose any genuinely blocked interaction.

For route-backed main pages, separate user swipes from programmatic page synchronization. Updating the selected route must not call back into navigation during build, create duplicate history, or snap a finger-driven page to its integer position halfway through a swipe. The owner's earlier immediate main-tab tap behavior is a separate contract: keep it where still applicable while adding hand switching and continuous indicator progress.

## Overlay motion has one progress source

Drive the dialog/sheet surface and its background effects from the same presentation progress. Begin blur and tint with opening, reverse them with closing, and include the user's current sheet-drag displacement. Do not wait for the dialog to appear before starting an independent filter animation, or fade a permanently full-strength backdrop filter through a separate opacity layer and assume its blur strength is interpolated.

For an interactive sheet, derive visibility from route progress and the visible fraction of the dragged surface. Restore the backdrop and surface together on a cancelled drag; continue from the released displacement on dismissal. Do not reset upward before closing. Guard all phases against live busy/required-state changes. Read laid-out dimensions during layout/gesture-safe phases, not through context.size during build; release animation controllers/listeners with their owner.

Use a localized animation builder so each animation frame updates only the relevant effects/transform. Avoid an extra independent easing/timer for the blur. Synchronization is a correctness requirement, not proof of device performance: verify intermediate frame values and gesture reversal in tests, then profile device rendering when a smoothness claim matters.

## Optional, required, and busy are different states

An optional idle sheet shows a title, shared X, and one drag handle; X, outside tap, downward drag, and system back dismiss consistently. A handle must correspond to a working gesture. A required sheet must not advertise a dismissal it cannot perform.

During a transaction that must finish before leaving, derive one live dismissal guard from its actual loading state. Apply it to X, barrier taps, drag start/update/end, system back, and programmatic exits that would abandon the flow. Disable conflicting duplicate actions. Restore dismissal on completion/failure as the flow requires. Do not make a new-project sheet permanently nondismissible just because it can submit. Recheck the guard when a drag ends because loading may start during the gesture.

A drag must settle from its current offset in the release direction, respecting velocity and dismissal threshold. Once dismissal is chosen, continue down; do not first reset to zero, animate up, then reverse the route down. An upward release should restore the sheet when appropriate. Keep the handle gesture usable when the body is scrollable, and coordinate gestures without stealing normal content scrolling. Prefer existing route/animation mechanics where sufficient; do not stack competing animations.

## Audit dismissal at launchers and callbacks

When an idle rename/edit sheet shows X, Cancel, or a drag handle but will not close, inspect the invocation as well as the shared shell. A constant isDismissible: false can override a correct busy-state PopScope. Apply the same audit to sibling sheets and their separate entry points; removing one flag from one drawer caller is insufficient when list/detail callers use different launchers.

Separate loading the list from committing a transaction. Fetching choices does not by itself make an otherwise optional sheet mandatory. Determine which actual operation must complete before dismissal, and unlock after failure when retry/edit/cancel is valid. Keep genuinely required flows explicit rather than inferring “required” because a form belongs to auth or billing.

Assign exactly one owner to the navigation pop for cancel/close. If the shared shell pops, its caller's callback must not also pop the parent route. Preserve callbacks that perform other cleanup and return values. Test X, Cancel, outside tap, drag, and system back through idle, busy, and failure states; test that dismissal leaves the intended underlying screen.

## Verify the actual visual contract

Check small screens, safe insets, keyboard open/closing, RTL, long localized labels, light/dark, short content, and overflow content. Assert the last item is reachable and overlay z-order is correct. Exercise idle dismissal, in-flight blocking, completion/error unlock, and drag-release direction. Widget/source checks do not certify device keyboard timing or gesture smoothness; disclose unavailable device evidence.
