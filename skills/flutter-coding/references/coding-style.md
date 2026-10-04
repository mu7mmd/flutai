# The owner's coding style

## Dart imports

Apply these rules to new Dart files and imports in files touched by the task. Keep unrelated files and generated output out of an import cleanup.

- Use direct `package:flutter/...` imports for Flutter SDK libraries and direct `package:<dependency>/...` imports for external dependencies. Import the library that owns the needed API; do not introduce a catch-all barrel just to shorten imports.
- Use relative paths for the project's own files within the same source tree, including core and other features: `../../core/...`, `../repositories/x_repo.dart`, or `x_model.dart`. Do not use `package:<current_project>/...` or absolute filesystem paths for these imports. Derive each path from the importing file's directory, not from an assumed feature root.
- Keep nonempty groups in this order, with exactly one blank line between them: Dart SDK (`dart:`), Flutter SDK (`package:flutter/...`), external packages, then project-relative imports. Omit empty groups. Keep an `as` prefix or conditional import attached to its directive.
- Within the project-relative group, put the farthest paths first: sort by the number of leading `../` segments, descending. Put paths with no leading `../` after parent paths, and files in the current directory last. Use `x_file.dart`, not `./x_file.dart`, for those files. Do not insert blank lines between distance levels. Preserve existing order for equal-distance imports; use a consistent order for new ties. Do not let alphabetical sorting override the farthest-to-nearest order.
- Prefer `show` when only one or two names, or a small clear set of names, are needed from a broad library. Keep an unrestricted import when many APIs are used and a long `show` list would reduce readability. Use `hide` when excluding a specific conflicting or unwanted name is clearer than listing everything needed. Apply this judgment to Flutter, dependency, and project imports. Include any extension names required for extension resolution, and keep intentional `as` prefixes for disambiguation. Remove unused or duplicate directives without dropping APIs the file uses.
- Respect actual Dart package boundaries: external or separate workspace packages still use `package:`. Use the app's public `package:` API when importing it from outside its `lib` source tree, such as a test; do not traverse into another package with `../`. Preserve generated `part` directives and required conditional-import syntax.

For example, keep Flutter, dependencies, and project files in separate groups, with the nearest project file at the bottom:

```dart
import 'package:flutter/material.dart';

import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:firebase_core/firebase_core.dart' show Firebase;

import '../../../../core/widgets/text/bayin_heading.dart';
import '../../constants/auth_page.dart';
import '../widgets/bayin_social_sign_in.dart';
import 'x_file.dart';
```

Verify paths and selected names against the real source, then run focused analysis when available. Importing fewer names controls namespace visibility; do not claim `show` or `hide` alone reduces app size. If an existing lint or import organizer conflicts with this approved ordering, report the specific conflict rather than silently rewriting the rule or changing project/tooling configuration.

## Dot shorthands

Prefer Dart's [dot shorthand syntax](https://dart.dev/language/dot-shorthands) wherever supported, across Flutter, dependency, and project APIs in new/touched code. Check the effective language version first: this syntax requires Dart language version 3.10 or later, including the package SDK lower bound and any file-level language override. An installed newer SDK alone does not enable it for an older language version.

Use `.value` for enums and eligible static fields/getters, `.named(...)` for named/factory constructors or eligible static methods, and `.new(...)` for unnamed constructors when the expected type resolves the intended member. Preserve constant contexts, explicit `const` where required, generic types, and evaluation behavior.

```dart
Text(
  label,
  overflow: .ellipsis,
  textAlign: .center,
);

EdgeInsets spacing = .all(12);
const Duration pause = .new(milliseconds: 300);
```

Resolve against the expected type, not an arbitrary namespace or subtype. Keep `Colors.red` and `TextStyles.authWordmark` when the expected types are `Color` and `TextStyle`; those members belong to different classes. Similarly, a general `Widget` context cannot infer a specific `Text` constructor. Keep explicit names when context is absent, ambiguous, or insufficient, such as an untyped `final` initializer. Keep comparison shorthands directly on the right of `==`/`!=` with a suitable left-hand type; standalone expression statements cannot start with a dot.

Use focused analysis to verify actual resolution. Do not upgrade SDK constraints, add language overrides, alter public types, or change lint configuration solely to enable shorthand. Apply compatible syntax and report a concrete tooling conflict when necessary; avoid unrelated or generated-file cleanup.

## Selective source comments

Comment code when a developer needs an explanation to understand it or change it safely: a complex algorithm or condition, a value with a non-obvious meaning, required ordering, a workaround, or a choice made for a particular constraint. Explain why the code has that form, the relevant assumption, or the consequence of changing it. Keep the comment concise and immediately above or beside the code it explains.

Do not add comments above every class, method, widget, callback, or straightforward statement. Avoid narrating obvious code, redundant section labels, and generic generated explanations. Improve names or extract a private helper when that makes the code self-explanatory; retain a comment when a real reason still needs explanation. Use `///` for a public contract that requires explanation, without mechanically documenting every symbol.

Verify the explanation against actual behavior and update or remove stale comments with the code. Keep longer developer explanations, requirements, configuration, settings, and version guidance in project-root `documentation/`, following [documentation.md](documentation.md); an important local warning or rationale should still be visible at its relevant code.

## Simple code with one owner for repeated behavior

Implement only what the current requirement needs. Prefer direct methods, small widgets, and clear data flow over a generic framework. A short function is enough when a service adds no useful ownership or lifecycle. Reuse an existing service when the behavior already belongs there.

At the second use of shareable logic or UI, extract or extend its common implementation and update both callers. Do not wait for a third copy. Keep the abstraction close to its uses: a private method for one class, a feature helper/widget for one feature, and an existing shared/core location for cross-feature use. Reuse an existing package/workspace boundary when present; do not create a new package or migrate unrelated apps for a small task.

Choose the smallest API that expresses the current differences. Pass data, labels, or a callback where that is sufficient. Do not add unused options, parallel implementations, a factory hierarchy, or a collection of mode flags for imagined future callers. Preserve distinct public actions while sharing their internal work.

Sharing must preserve the actual contract, return type, lifecycle, evaluation order, and side effects. Check these before combining two pieces of code. If the requested degree of reuse conflicts with those semantics, explain the concrete conflict and propose a solution for the owner to approve; do not silently weaken the DRY rule or merge incompatible behavior.

## Keep build focused with private helpers

Keep `build` readable as reactive inputs followed by UI composition. Move blocks that occupy substantial space or express a separate responsibility into named private methods below `build` in the same widget: listener registration, handling success/error transitions, submit actions, navigation sequences, or nontrivial calculations. Use names that communicate their purpose, such as `_listenToAuth`, `_submit`, or `_saveSession`. A helper is useful even when called only once if it makes the surrounding code easier to follow; do not wait for duplicated code.

Prefer a private widget method for widget-owned work. Use a small local function inside `build` when it meaningfully simplifies access to current controllers, validator, or other build-local values. Pass current inputs explicitly when extracting a method; do not add widget fields, caches, or mirrored state just to make extraction possible. Keep a short expression inline when a helper would only rename it.

For Riverpod widgets, call a registration helper such as `_listenToAuth(context, ref)` synchronously during `build`, and place the `ref.listen(...)` body in that helper. Extracting the code changes its organization, not when registration happens. Do not move `WidgetRef.listen` into an event callback, `useEffect`, async continuation, or `initState` as a style cleanup. If registration genuinely belongs outside `build`, use the installed Riverpod version's supported lifecycle API (such as `listenManual`) and its subscription/disposal contract. See [Riverpod refs](https://riverpod.dev/docs/concepts2/refs).

Keep `ref.watch` reactive and keep hooks unconditional and in a consistent order during build. In particular, do not hide controller hooks inside ordinary private widget methods or create every variant's controllers in the shared scaffold. Extract pure state derivation when it helps readability, while keeping its watched inputs current. Preserve transition checks, async sequencing, error handling, context validity, and listener ownership; do not add duplicate listeners to a screen and its shared layout.

## Expressions, variables, and conditions

Resolve repeated stable access once in the same block:

```dart
final locale = context.locale;
final themedColors = context.themedColors;

return SomeExistingCard(
  title: locale.hi,
  subtitle: locale.you,
  color: themedColors.color3,
  borderColor: themedColors.color5,
);
```

This is illustrative: use actual project components and generated localization keys. Follow the same pattern for repeated model paths and computations. Keep one-use expressions inline unless a name explains their meaning, avoids a side effect, or is needed for control flow/type promotion. Use descriptive short names rather than chains of aliases for the same value.

An alias is a local value, not a new cache. Recompute context-derived values in the appropriate build/callback scope; do not retain locale, theme, reactive state, or a notifier across a boundary where it can become stale. Do not replace `ref.watch` with `ref.read` to remove repetition. Calls that are meant to observe different moments or produce separate effects must not be collapsed into one evaluation.

When a condition is necessary, use a straightforward early return, collection `if`/`for`, or simple ternary that makes the branch immediately understandable. First consider the variant-separation preference below. Use a named predicate when it is reused or carries business meaning. Avoid nested ternaries, inverse aliases of the same condition, and repeated checks already guaranteed by the current branch. Keep necessary input, lifecycle, and error checks.

When several values vary with the same mode, prefer selecting one complete configuration and passing it to its consumers. Do not spread the same condition across individual fields or hide it in per-field getters. For themes, colors, typography, and related visual values, follow [design-tokens.md](design-tokens.md).

Pay attention to argument/local shadowing, equality targets, `&&` versus `||`, null versus empty, default versus absent values, and state transitions. A short expression must still implement the exact condition requested.

## Separate variants before adding conditions

Apply the owner's **Extend Over Conditions (EOC)** principle throughout the code: express differences through supplied parameters and specialized reusable components, minimizing internal conditions. Give each variant its own ready values or behavior, then select it once at the boundary when a runtime choice is required. Avoid passing a mode/boolean into an object and branching repeatedly inside its fields or methods. For a genuine common contract, prefer a small abstract class with concrete implementations; for example, `ThemedColors` → `LightColors` and `DarkColors`. Consumers receive the selected object and use the same API without knowing its mode.

Build reusable specializations in layers when actual callers need them:

1. Make `XWidget` own its common implementation and accept the differing values, text, child widgets, and callbacks as parameters.
2. Make `YWidget` compose `XWidget` with the concrete parameters for a recurring design or behavior. Expose only the remaining differences its callers actually need.
3. Make `ZWidget` compose `YWidget` when it reuses that specialization and supplies its remaining differences. Compose `XWidget` directly when the intermediate specialization does not fit.
4. Reuse the deepest existing component that matches the behavior, keeping shared implementation in its existing owner. Extract repeated specializations from the second use; add layers only for real reuse or distinct responsibility.

For Flutter widgets, implement these extensions by composing the existing widget in `build`. Use Dart inheritance where an actual class contract requires it. Keep each public reusable widget in its own file, and keep wrappers close to their real feature or cross-feature users.

Apply EOC inside callbacks, listeners, argument expressions, and texts as well as widget trees. Pass a concrete `onPressed`/`onTap`/`onSuccess`/`onError`, label, style, or child instead of having the base choose it by variant. A specialized caller supplies that behavior directly. If a shared listener owns identical transition mechanics, it can accept specific handlers while keeping registration and lifecycle with the correct owner. Do not merely relocate variant switches into closures, helper functions, getters, or expressions passed as parameters; resolve variant responsibilities into their specialized components.

Apply this as a general composition rule to screens, widgets, cards, forms, dialogs, and other reusable code. When the same mode controls several independent places (heading, fields, footer, submission, or listener navigation), split the behavioral variants into specialized callers. Moving those branches into `_titleForMode`, `_submitForMode`, or per-field getters does not satisfy this rule.

Share the actual common layout in a widget such as `XScaffold`. Give it the parameters the current callers need: `title`, `subtitle`, `actionLabel`, `onPressed`/`onTap`, `body`/`content`, and optional complete widgets such as `header` or `footer`. Use typed data or a narrowly scoped builder only when needed. Do not pass a page/mode enum or flags that make the shared widget choose feature-specific fields, actions, or navigation. The layout renders the supplied values and slots; the caller decides what they mean. Reuse or extend an existing scaffold when it already owns that layout.

For example, separate `LoginScreen`, `RegisterScreen`, and `VerifyOtpScreen`, each using the same `AuthScaffold` in the feature's `presentation/widgets/`. Each screen supplies its own heading, form, action label, submit callback, and footer. Login owns its login action and any social sign-in listener; registration owns name/identifier fields and registration action; OTP owns its OTP controller, form, verification action, and verification listener. Adapt the exact fields and actions to the target app. Keep each screen's private listener/helper methods below its `build`. If a route still receives a legacy page enum, resolve it to the appropriate concrete screen once at the route boundary and update affected callers.

Keep controllers, hooks, validators, provider subscriptions, and route-specific side effects with the specialized screen that uses them. The shared layout can receive already-built fields or a validator needed by an existing form contract, but must not create unrelated controllers or register every flow's listeners. Share identical session-saving or other repeated behavior through its smallest existing owner when used by more than one screen; do not duplicate it merely because the screens are now separate.

An optional widget slot lets callers omit content; the base handles its presence in one place. Keep actual state checks such as loading/disabled, selected identifier type, validation, errors, and mounted checks where that state is owned. Distinguish runtime state within one flow from switching the screen's responsibility between unrelated flows.

Give recurring specializations a small named widget or a meaningful named constructor that supplies the slot/defaults to the same base implementation. A wrapper is useful when it owns real variant composition, not merely to rename a one-line call. A named constructor should supply the actual configuration instead of setting a mode enum that is switched on throughout `build`.

Prefer `const` constructors and constant configuration when possible. Keep constant values/default widgets in constructors when Dart allows it. When deriving a variant's UI requires runtime context, styles, or other non-constant work, consider a small separate `StatelessWidget` with a `const` constructor and do that work in its `build`; this can preserve a const-configurable shared scaffold and surrounding widgets. A runtime argument still makes that particular invocation non-constant. Do not remove reactivity or force invalid `const` expressions to satisfy the preference.

Apply EOC to services/classes too. Keep only conditions intrinsic to the component's actual changing state or contract that cannot be cleanly expressed through supplied ready values, child widgets, or behavior: optional-slot presence, real loading/enabled state, validation, state transitions, and lifecycle/error guards. Before retaining a design/variant condition, try a parameter, concrete implementation, or existing specialization. Do not add a hierarchy for a trivial one-off difference that a direct parameter already solves, and do not remove checks required for correct behavior.

## Async intent and completion

The owner chooses `void`, `Future<void>`, and whether to `await` according to how the operation is used. Do not convert every `void async` method or await every future as a style exercise. Preserve an intentional self-contained `void async` action when no caller needs completion and the action handles its own asynchronous failures and side effects. A returned future may intentionally be left unawaited when its completion is independent of subsequent work and error handling is accounted for.

Keep the language semantics precise: `Future<void>` exposes completion/error with no useful value; it does not force a caller to await. Not awaiting lets the caller continue, but synchronous work before the async function's first `await` still runs immediately. A caller's synchronous `try/catch` does not handle a later failure from an unawaited operation. `unawaited(...)`, if used by the project, only expresses intent; it does not handle errors.

Trace the actual caller before changing the contract. No response payload does not imply no completion dependency: dismissing a loader, navigating after saving, or refreshing dependent data may require completion even for a write-only action. When an existing contract hides completion needed by the requested behavior, explain the concrete issue and propose the smallest correction. Do not add scheduling, delays, wrappers, or error-swallowing code merely to implement fire-and-forget.

Language references: [Dart async execution](https://dart.dev/libraries/async/async-await), [unawaited semantics](https://api.dart.dev/dart-async/unawaited.html). These explain behavior; they do not replace the owner's case-by-case policy with a blanket style rule.

## Organization and reusable owners

For file placement and cross-layer work, read [project-structure.md](project-structure.md). It carries the Bayin/Jawwab conventions inspected on 2026-10-03 and routes to detailed guidance for design tokens, components/services, data/state, and localization/configuration. Use that bundled guidance without requiring the reference checkouts or project-local FLUTAI files.

Preserve the target's current architecture and public contracts. The owner's newest explicit instructions take precedence over conflicting historical patterns. Keep source edits scoped; do not reproduce incidental bugs or force a repository-wide migration simply because another project has a different layout.
