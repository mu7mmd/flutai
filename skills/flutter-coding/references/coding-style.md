# The owner's coding style

## Simple code with one owner for repeated behavior

Implement only what the current requirement needs. Prefer direct methods, small widgets, and clear data flow over a generic framework. A short function is enough when a service adds no useful ownership or lifecycle. Reuse an existing service when the behavior already belongs there.

At the second use of shareable logic or UI, extract or extend its common implementation and update both callers. Do not wait for a third copy. Keep the abstraction close to its uses: a private method for one class, a feature helper/widget for one feature, and an existing shared/core location for cross-feature use. Reuse an existing package/workspace boundary when present; do not create a new package or migrate unrelated apps for a small task.

Choose the smallest API that expresses the current differences. Pass data, labels, or a callback where that is sufficient. Do not add unused options, parallel implementations, a factory hierarchy, or a collection of mode flags for imagined future callers. Preserve distinct public actions while sharing their internal work.

Sharing must preserve the actual contract, return type, lifecycle, evaluation order, and side effects. Check these before combining two pieces of code. If the requested degree of reuse conflicts with those semantics, explain the concrete conflict and propose a solution for the owner to approve; do not silently weaken the DRY rule or merge incompatible behavior.

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

The owner's default is to give each variant its own ready values or behavior, then choose it once at the boundary. Avoid passing a mode/boolean into an object and branching repeatedly inside its fields or methods. For a genuine common contract, prefer a small abstract class with concrete implementations; for example, `ThemedColors` → `LightColors` and `DarkColors`. Consumers receive the selected object and use the same API without knowing its mode.

For UI differences, prefer composition: a shared scaffold/card accepts a complete `Widget` or a narrowly scoped builder where context is required. A feature supplies the specialized widget. An optional slot lets callers omit that content; the shared widget handles its presence in one place. Do not pass a flag and make the scaffold construct several feature-specific widget trees internally.

Give recurring specializations a small named widget or a meaningful named constructor that supplies the slot/defaults to the same base implementation. A wrapper is useful when it owns real variant composition, not merely to rename a one-line call. A named constructor should supply the actual configuration instead of setting a mode enum that is switched on throughout `build`.

Prefer `const` constructors and constant configuration when possible. Keep constant values/default widgets in constructors when Dart allows it. When deriving a variant's UI requires runtime context, styles, or other non-constant work, consider a small separate `StatelessWidget` with a `const` constructor and do that work in its `build`; this can preserve a const-configurable shared scaffold and surrounding widgets. A runtime argument still makes that particular invocation non-constant. Do not remove reactivity or force invalid `const` expressions to satisfy the preference.

Apply the same approach to services/classes when selecting a specialized implementation makes the operation clearer. Do not build a class hierarchy for a one-off trivial difference. A localized optional-child check, real enabled/loading state, validation guard, or simple branch is appropriate when splitting into more widgets/classes would make the code substantially harder to follow. Prefer fewer conditions and clear ownership, not zero conditions at the expense of simplicity.

## Async intent and completion

The owner chooses `void`, `Future<void>`, and whether to `await` according to how the operation is used. Do not convert every `void async` method or await every future as a style exercise. Preserve an intentional self-contained `void async` action when no caller needs completion and the action handles its own asynchronous failures and side effects. A returned future may intentionally be left unawaited when its completion is independent of subsequent work and error handling is accounted for.

Keep the language semantics precise: `Future<void>` exposes completion/error with no useful value; it does not force a caller to await. Not awaiting lets the caller continue, but synchronous work before the async function's first `await` still runs immediately. A caller's synchronous `try/catch` does not handle a later failure from an unawaited operation. `unawaited(...)`, if used by the project, only expresses intent; it does not handle errors.

Trace the actual caller before changing the contract. No response payload does not imply no completion dependency: dismissing a loader, navigating after saving, or refreshing dependent data may require completion even for a write-only action. When an existing contract hides completion needed by the requested behavior, explain the concrete issue and propose the smallest correction. Do not add scheduling, delays, wrappers, or error-swallowing code merely to implement fire-and-forget.

Language references: [Dart async execution](https://dart.dev/libraries/async/async-await), [unawaited semantics](https://api.dart.dev/dart-async/unawaited.html). These explain behavior; they do not replace the owner's case-by-case policy with a blanket style rule.

## Organization and reusable owners

For file placement and cross-layer work, read [project-structure.md](project-structure.md). It carries the Bayin/Jawwab conventions inspected on 2026-10-03 and routes to detailed guidance for design tokens, components/services, data/state, and localization/configuration. Use that bundled guidance without requiring the reference checkouts or project-local FLUTAI files.

Preserve the target's current architecture and public contracts. The owner's newest explicit instructions take precedence over conflicting historical patterns. Keep source edits scoped; do not reproduce incidental bugs or force a repository-wide migration simply because another project has a different layout.
