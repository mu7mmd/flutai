# Creating and extending features

Use for every new feature/flow, including a redesign or a feature added to a prototype. Read the task and existing consumers first, then implement the required layers. Simplicity means direct responsibilities and small components; it does not mean flattening all files into the feature root.

## Feature shape

```text
features/<feature>/
  data/
    models/
      <entity>_model.dart
      <action>_request.dart             # only when there is a distinct request
    repositories/
      <feature>_repo.dart
  providers/
    <entities>_provider.dart
    <entity>_details_provider.dart      # when detail fetching is distinct
    manage_<entity>_provider.dart       # shared command coordination when needed
    <feature>_state.dart                # separate state value when needed
  presentation/
    screens/
      <feature>_screen.dart
      <entity>_details_screen.dart
    widgets/
      <entity>_card.dart
      <entity>_form.dart
      <feature>_header.dart
      <action>_sheet.dart
      <section>/                       # cohesive large section, when needed
        <section>.dart
        <child>_widget.dart
```

For existing Bayin neighborhoods, use `controllers/providers` and `controllers/notifiers` where that is already the owner. Existing newer Bayin features and Jawwab use `providers`. Choose one state organization for a new feature according to the surrounding app, not a mixture created accidentally. Feature-only `helpers`, `utils`, `constants`, or `services` are allowed for genuine feature-owned work. Do not force everything into core.

Screens and widgets are sibling directories inside `presentation`; widgets do not go inside the `screens` directory. Models and repositories are sibling directories inside `data`. Public screen/component classes live in individual files named in `snake_case`; do not implement a group of screens in `screens.dart` or cards/fields/buttons in `widgets.dart`. A barrel with those names may contain exports only if the target uses it.

## Implement an actual vertical slice

For a list/detail/form capability:

| Owner | Implement here | Keep out |
| --- | --- | --- |
| Model | Typed fields, immutable constructor where suitable, `fromMap`, nested mapping, required `toMap`/`copyWith`, derived business values shared by callers. | Screen rendering, SDK setup, duplicated route navigation. |
| Request | Body/query serialization for a real operation with different input semantics. | A copy of the response model with no actual distinction. |
| Repository | A named operation using shared `ApiService`/storage, named endpoint/key definitions, typed result mapping, propagated errors. | Loading widgets, `BuildContext`, dialogs, ad hoc clients or fake success fallbacks. |
| Provider/notifier | Dependencies, state transitions, command coordination, refresh/invalidation, lifecycle and cancellation as required. | Shared field decoration, inline HTTP setup, per-screen copies of pagination. |
| Screen | Route inputs, high-level layout, watch the required state, compose widgets, dispatch actions. | Raw map parsing, service initialization, widget catalog, font construction, mixed screen variants. |
| Feature widget | Focused card/section/field/sheet with model/label/slot/callback inputs; watch its own narrow state if that is its responsibility. | Other features' business decisions or a giant boolean-driven component. |
| Core widget/service | Behavior shared across features or already part of the app's common vocabulary. | Hardcoded business names, endpoints, eligibility rules, or feature-specific data assumptions. |

The data-backed path is screen → provider/notifier → repository → shared API/service → typed model. A generic pagination provider can own the repository operation; configure it once instead of adding a pass-through feature repository method only for ceremony. In that case name the reused pagination repository in the responsibility map.

Repository providers can remain in the repository file when that is the established pattern (`WalletRepo` plus `walletRepoProvider`). A request DTO can live beside a tightly coupled model in existing code; prefer separate named files for independently used types in newly created features. Do not introduce interface/implementation pairs, domain entities, use cases, or dependency injection frameworks solely because a feature has several layers.

## State and form conventions

- Prefer the established Riverpod annotations, families, generated `part` arrangement, and `Ref` lifecycle. Keep generated files beside their source. Do not write `.g.dart` manually or blindly use a different Riverpod major API.
- Let `ref.watch` drive reactive UI/dependencies; use `read` for commands and deliberate snapshots; use `listen` at the existing side-effect boundary. Own a controller/subscription in one place and dispose it there. Do not cache a context-dependent locale or theme in a long-lived field.
- Reuse the current `FutureState`/`AsyncValue` and `ProviderBuilder`/pagination builders. Preserve loading, retry, empty, error, previous-data, and refresh behavior. A feature's `isLoading` is real state; the fewer-conditions rule targets scattered mode decisions, not genuine state transitions.
- Use the shared request guard for a command when the project already owns its global loading/error/success flow. Keep success callbacks, error ownership, and operation sequencing intentional; do not mechanically convert all `void async` or all callbacks.
- Keep form controllers/focus/temporary expansion with the form's UI owner, and server/business state with providers. Use `ValidationForm`, `FormValidator`, shared fields and formatters. Preserve server-field errors instead of replacing them with local-only validation. Do not copy Bayin/Jawwab's OTP, banking, subscription, or survey thresholds into another feature.
- Model an explicit null update when needed (`NullableValue` or the target equivalent). Do not accidentally turn “clear value” into “keep old value.”
- Reuse the pagination request/provider/list/grid contract. Check equality/cache arguments, filter/reset behavior, duplicates, refresh, loading more, and disposal for the actual data flow; never mix Bayin and Jawwab pagination constructor signatures.

## Composition and variants

Prefer complete children/slots, named constructors, or small specialized widgets. For example, the common scaffold takes `header`, `body`, and `bottomBar`; `SearchResultsScaffold` supplies a `SearchHeader` and reuses the same shell. Avoid `isSearch`, `isWallet`, `showSpecialHeader`, and repeated internal branch chains.

Keep const constructors and const default children where possible. Resolve locale/theme/runtime values inside the relevant widget's `build`. When a redirecting constructor would lose const because it eagerly constructs runtime children, use a small const-constructible `StatelessWidget` to own that composition when it remains simpler. Do not force unnecessary inheritance or split a trivial genuine condition into several artificial classes.

Extract shared code from the second use. Feature widgets used only within one flow stay with that feature; controls reused across feature boundaries move to the proper `core/widgets/<family>` owner. Helper functions should perform non-widget transformations; reusable visual composition should normally be a widget with its own identity/const opportunity, not a collection of `buildX()` functions.

## Routes, strings, and integrations are part of the feature

Add route declarations/builders and typed arguments through [routing.md](routing.md). Update ARB catalogs with real message keys/placeholder metadata, use `context.locale`, and use directional layout and registered token fonts. Add real assets to the appropriate constants and `pubspec` declarations. Add task-required SDK calls to their service owner, with initialization and disposal wired once.

When no backend exists, distinguish local form state from persisted records. Keep the requested UI organized and use an explicit unavailable state. Do not invent a repository contract, fake a successful save, or silently fall back to hardcoded records. A purely static screen needs presentation and shared tokens, not an empty repository/provider just to match the diagram.

For a same-project redesign, reuse existing typed data and state with explicit paths, but create new UI in the required `presentation` directories. For a standalone new app, implement its own foundation/data contracts instead of importing the source app by package name.

## Feature completion checks

1. Inspect actual paths and imports: data/state/presentation ownership, separate public UI files, appropriate core reuse, and no accidental cross-feature internals.
2. Trace a real success and failure from a user action to the owner and back; verify the applicable loading/empty/retry states, validation, refresh, and nullable-update semantics.
3. Check route input/result types, direct navigation, back behavior, strings/locales, and token use.
   Apply [Design Linking](design-tokens.md#design-linking): inspect and reuse matching components, keep dialog/sheet presentation linked, and compare new UI with established spacing, geometry, colors, typography, icons, and transitions.
4. Run the bundled structure checker with `--feature <name>`; use `--requires-data` for a data-backed feature, and explicit `--shared-root` if owners are reused in an alternate tree. Review any generic pagination exception manually and report its real owner, not a dummy repository.
5. Format/analyze the changed slice and run meaningful behavior checks. Verify generated imports resolve. Report exactly what was validated.
6. Update project-root `documentation/` to explain the implemented feature/flow and affected requirements, configuration, settings, and versions. Use selective comments for non-obvious local logic or rationale. Follow [documentation.md](documentation.md).

## Observed source examples

Bayin auth uses `data/models/auth_requests.dart`, `data/repositories/auth_repo.dart`, `controllers/notifiers/auth_notifier.dart`, and `presentation/{screens,widgets}`. Its notifications and project features retain the same data/presentation split with `providers`.

Jawwab wallet separates `data/models/bank_account_model.dart`, `data/repositories/wallet_repo.dart`, `providers/manage_bank_account_provider.dart`, `presentation/screens/wallet_screen.dart`, and `presentation/widgets/bank_account_card.dart`. `transactions_provider.dart` configures shared pagination instead of writing another list-fetch engine. These are structural examples, not mandatory feature names or portable business logic.
