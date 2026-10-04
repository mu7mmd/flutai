# Shared widgets, helpers, extensions, and services

Read this reference for UI composition or reusable utility/integration work. Use the target's existing equivalent before creating a new owner. Names below are concrete Bayin/Jawwab examples, not compulsory dependencies or an instruction to copy their files.

## Widgets and visual primitives

For new code, the file layout is part of the contract: `core/widgets/buttons/app_button.dart`, `core/widgets/buttons/app_icon_button.dart`, `core/widgets/text/strut_text.dart`, and equivalent family folders. Keep the existing `button/`, `text_field/`, or `image/` spellings in an established project. Put independently reusable public components in separate files, including public loading-button and app-bar-action components. A private `State` or tightly coupled private implementation may stay beside its owner; named constructors share their owning class. Historical files containing several public widgets are not templates for new multi-widget files. See [core-catalog.md](core-catalog.md) for the family map.

Build screens from project controls. Keep their colors, typography, disabled/loading states, shape, padding, and repeated interaction behavior in the shared implementation. A screen supplies its labels, data, callbacks, and genuine visual differences.

Follow strict [Design Linking](design-tokens.md#design-linking): search the actual component and representative callers before adding UI; reuse matching defaults or extend their owner for a real variant. Match established spacing, padding, shape/borders, colors, typography, size, icon treatment, and animation when creating a missing component. Keep common dialogs and sheets linked through shared presentation shells and launch helpers, including title placement, action-button design/layout, insets, and transitions. Optional parameters must preserve the overall system rather than introduce arbitrary local drift.

Apply **Extend Over Conditions (EOC)**: separate callers with distinct behavior and compose them through a shared parameterized layout. A common scaffold/form/card receives its title, subtitle, action label, callback, and complete content/footer slots as needed; each specialized screen/widget owns its controllers, submit action, and private listener helpers. Reuse recurring specializations too: `YWidget` configures `XWidget`, and `ZWidget` may configure `YWidget` when it reuses that same design/behavior. Pass the remaining differences through parameters at each layer. Do not make the base repeatedly branch on login/register/verify or analogous modes. See [EOC rules](coding-style.md#separate-variants-before-adding-conditions) and [private helpers](coding-style.md#keep-build-focused-with-private-helpers) before implementing these variants.

| Need | Observed reusable owner |
| --- | --- |
| Buttons | Bayin `CustomElevatedButton`, `StateElevatedButton`, and outlined/text variants; Jawwab `JawwabButton`, `JawwabStateButton`, `CustomOutlinedButton`, and `CustomIconButton`. Named forms such as `.small`, `.custom`, and `.text` share their underlying implementation. |
| Cards and surfaces | `BasicCard`, ink-well variants, shared app bars/scaffolds, and named circle/square/full-radius shapes. Extend these instead of rebuilding material, clipping, decoration, and taps at each call site. |
| Text | `TextStyles` tokens; Jawwab `StrutText`, `SmBrownText`, and other small purpose wrappers where the repeated typography/behavior warrants them. Preserve truncation, direction, and line-layout behavior. |
| Images and icons | Asset constants with `CustomAssetImage`/`CustomAssetSvg` in Jawwab and corresponding image/SVG wrappers in Bayin; shared network image/placeholder/media components. |
| Form fields | `CustomTextField`, specialized mobile/date/price/search fields, `FieldDecoration`, formatters, and `ValidationForm`. Reuse their existing controller and validation contracts. |
| Overlays | Existing custom dialogs, flexible sheets, action rows, selection sheets, and context helpers own common dismissal, keyboard/safe-area padding, and result behavior. |
| Async UI | `ProviderBuilder`, `FutureProviderBuilder`, `FutureStateProviderBuilder`, loading/retry components, and pagination list/grid widgets. Preserve the local callback signatures and refresh semantics. |
| Repeated layout | Existing spacing/padding utilities, directional primitives, shared grids/page views, and refresh wrappers when they fit the requested layout. Do not replace a normal small layout with a generic engine. |

Prefer a named constructor or thin wrapper over repeated setup, while sharing the implementation underneath. Pass a label/model/callback instead of adding booleans for unrelated behaviors. State-dependent controls may still use necessary conditions for loading, enabled, and selection behavior; the preference for fewer conditions does not remove real states.

For a scaffold with optional content, use a slot such as `Widget? header` rather than a `showSpecialHeader` flag. A caller can omit it, pass its complete widget, or use a specialized wrapper/named constructor that supplies it. Keep feature-specific decisions out of the shared scaffold. The base may use one presence check to insert an optional slot; this is not a reason for a new hierarchy.

Illustrative composition, with class names adapted to the actual project:

```dart
class HeaderScaffold extends StatelessWidget {
  const HeaderScaffold({super.key, required this.body});

  final Widget body;

  @override
  Widget build(BuildContext context) => CustomScaffold(
    header: const FeatureHeader(),
    body: body,
  );
}
```

Here `CustomScaffold` is the shared implementation and `FeatureHeader` is the complete slot content. If the header needs runtime context, its own `build` resolves it while its constructor can remain `const`. A named constructor on the shared widget is another option when it can directly supply the variant without knowing feature business logic. Follow the full decision guidance in [coding-style.md](coding-style.md#separate-variants-before-adding-conditions).

Keep generic machinery generic. In Jawwab, `WidgetToImage` owns capture mechanics and returns image bytes; the referral screen supplies the child and calls `ShareService.file`. Reuse that responsibility split for analogous tasks. Verify the actual event/callback contract when adapting a component; its class name or comment alone is not proof of behavior.

Choose local hooks/stateful widget state for UI-owned controllers, focus, expansion, and animation according to the existing pattern. Put shared/reactive business state in its provider. Respect who creates, listens to, updates, and disposes each controller; do not create a controller in every build or dispose one supplied by the caller.

## Helpers, extensions, and utility classes

Keep small transformations small. Both apps use functions such as `fromMapOrNull`, `modelListFromMap`, `primaryUnfocus`, `futureDelay`, and `exceptionHandler`. Jawwab adds reusable equality/hash, date/count/price formatting, and UUID helpers. Reuse the relevant function instead of repeating parsing, mapping, formatting, or focus setup inside widgets and repositories.

Use an extension when the operation naturally belongs to the receiver: context access, controller text, collection operations, date comparisons, enum lookup, or string direction. Both apps' context extensions supply `locale`, theme access, safe-area values, and overlay/navigation conveniences. Alias repeated access locally and do not retain a context-derived value across locale/theme changes.

Use an existing utility class for an owned object or policy, such as `FormValidator`, `PhoneFieldController`, `InputDecoration`, an input formatter, or a reusable border. Keep error translation in the existing exception handler and request error model. Retain server-field validation alongside local rules; do not convert an API error to a successful empty result for convenience.

Keep domain-specific validators and formatters scoped to their real users. Do not transfer Jawwab's bank/survey rules, Bayin's subscription rules, or either app's thresholds into unrelated apps. Do not duplicate an existing helper under a second name.

## Services and integration ownership

Services own SDK setup and reusable external operations; feature callers express intent. The smallest existing form is preferred: static methods for a stateless facade, or an instance/provider when dependencies, state, initialization, or lifecycle need ownership. Do not impose a singleton, repository interface, dependency-injection framework, or static-only rule on every service.

- `ShareService` owns share payloads and presentation origin. Its public file/URL actions share the common send operation.
- `MediaPickerService` owns picker calls and common format/size checks. Feature callers supply the allowed formats and limits required by their use case.
- `ApiStorageService` owns the signed-URL/upload/confirmation sequence and shared progress handling. Feature repositories supply endpoint/request differences.
- Location, device-info, URL-launch, social-auth, downloader, review, and speech services keep SDK calls out of repeated feature handlers. Reuse only capabilities actually present in the target.
- AppsFlyer, Firebase messaging/analytics, and sockets use existing provider/service owners. Register callbacks and dispose resources through the owner's lifecycle; avoid initializing the same client in several screens.
- Existing analytics methods and typed event parameters own event names and mappings. Add task-required events through that API, without duplicating raw SDK/event setup in the UI.

Read actual success, cancellation, permission, and error behavior before reuse. Do not adopt ignored errors, arbitrary delay/retry timing, identifier assumptions, or copied SDK credentials from a reference project. The native/configuration approval boundary in the main skill still applies.

## Source anchors

Inspected on 2026-10-03: both apps' `lib/core/helpers` and `lib/core/services`; Bayin `lib/core/widgets/{provider_builder,basic_card}.dart` and `button/custom_elevated_button.dart`; Jawwab `lib/core/widgets/{provider_builder,app_cards,validation_form,widget_to_image}.dart`, `button/jawwab_button.dart`, `text/{strut_text,sm_brown_text}.dart`, and `image/{custom_asset_image,custom_asset_svg}.dart`. Shared widget APIs were inventoried across both `core/widgets` trees; representative implementations and their feature callers establish the patterns above.
