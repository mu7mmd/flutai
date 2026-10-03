# Core ownership and component catalog

Read when building the foundation or deciding where shared behavior belongs. The inventory comes from Bayin and Jawwab; the owner's current explicit preferences refine the examples. In particular, new public UI components go in separate files even where an older example puts several classes together. For the complete tree and creation order, use [project-blueprint.md](project-blueprint.md).

## Constants, themes, and styles

| Owner | Responsibility and consumer contract |
| --- | --- |
| `constants/app_colors.dart` | Fixed brand/status colors used across components. Theme-varying semantic fields come from the resolved palette. Do not place geometry, network config, or typography here. |
| `themes/colors/themed_colors.dart` | Shared palette contract. `light_colors.dart`/`dark_colors.dart` contain complete direct values for supported modes. Select the concrete palette once at the theme boundary. |
| `constants/app_sizes.dart` | Repeated design dimensions: screen padding, button heights/radii/icon sizes, field heights, sheet/dialog radii, gaps. Use meaningful names; do not copy another app's numeric design scale. Keep a truly local one-off measurement local. |
| `constants/app_fonts.dart` | Registered family identifiers and the required locale-to-font choice. Typography calls it; ordinary widgets and theme assembly do not independently set font families. Avoid mutable global current-font state. |
| `styles/text_styles.dart` | Ready-to-use role → size → weight tokens, such as `TextStyles.text.md.bold`, and purpose aliases such as `field`, `fieldHint`, `appBar`, `label`, or `callout` when used. Private size/weight builders and line-height/spacing conversion live here. |
| `styles/font_weights.dart` | Shared named weight values; keeping this with text styles is acceptable when it is a tightly coupled private implementation. |
| `themes/app_theme.dart` | Compose Material component themes from ready palettes, typography, sizes, and shape/decoration owners. Bind text, button, field, app bar, dialog, sheet, tab, selection, and other used component defaults. Do not create raw typography here. |
| `constants/app_assets.dart` | Typed/named image, SVG, animation, and custom icon references. Consumers use the correct wrapper, not repeated raw strings. Declare actual resources in `pubspec.yaml`. |
| `constants/app_locales.dart` | Supported/default locale decisions consistent with generated catalogs and device fallback. Locale-dependent style resolution follows the selected locale. |
| `constants/storage_keys.dart` | Shared persisted preference/session key names. Feature widgets do not invent their own spelling. |
| `api/constants/api_keys.dart`, `api_endpoints.dart` | Transport key/endpoint vocabulary, used by models and repositories. Existing combined files are acceptable; environment base URLs belong in configuration. |
| `constants/key_enums.dart` | Genuine shared typed choices/extensions. Feature-only business enums remain within their feature. |

Read [design-tokens.md](design-tokens.md) for palette selection and typography rules. A theme-mode boolean can be resolved once at the outer boundary; it must not be passed through every color getter or widget. Existing valid token owners may be reused in a same-project redesign; organize newly introduced palettes and sizes separately from the theme builder.

## Shared UI families

These are families to implement as needed, not one file containing a family of public classes. Use plural names below in a new app and existing equivalent spellings in an established one. Reuse from the second use; an app's deliberate shared controls can be established with the first screen.

| Folder | Separate component files and owned behavior |
| --- | --- |
| `widgets/buttons/` | Primary/elevated button, outlined button, text button, icon button, async-state button, label/icon row. Own common dimensions, shape, padding, loading/disabled behavior, semantics, and icon alignment. Named `.small`, `.text`, `.custom` constructors share one component's implementation. |
| `widgets/text/` | Strut text, directional text, repeated caption/value labels, price/currency text when required. Own truncation, text direction, line-layout behavior and named default style. Avoid one wrapper for every text occurrence. |
| `widgets/text_fields/` | Base field, search field, mobile/price/date variants. Reuse shared decoration, formatters and validation; own focus/controller lifecycle explicitly. Formatting is distinct from business validity. |
| `widgets/images/` | Asset bitmap, SVG, network image/SVG, placeholder, logo. Own sizing/fit/loading/error/tint contracts. Keep asset identifiers separate from rendering. |
| `widgets/cards/` | Base card, tap/ink surface, circle/icon card, common list surface. Own decoration, clipping, interaction and disabled semantics. Feature entity cards stay in feature presentation. |
| `widgets/scaffolds/`, `app_bars/` | Shared frame, background/layout shell, app bar, back action. Prefer complete child/header/body/action/bottom slots, specialized wrapper widgets and meaningful constructors. |
| `widgets/navigation/` | Shared bottom navigation/drawer/navigation rail and its items, when required. Router state owns destination selection; each feature does not recreate navigation state. |
| `widgets/feedback/` | Loading, empty, error/retry, shimmer, snackbar content. State builders reuse these and preserve retry/refresh contracts. Avoid making a generic error widget understand a particular API operation. |
| `widgets/overlays/` | Dialog card/title/actions, confirmation/result dialogs, flexible sheet, keyboard/safe-area handling. One public component per file. Context helpers open/close them; business actions remain with the caller/provider. |
| `widgets/dropdowns/`, `sheets/` | Static/future/paginated selection, dropdown presentation, selected-item rows. Preserve single versus multiple results and typed pop values. |
| `widgets/layout/` | Reused spacing, directional boxes, responsive grids, expandable page views, refresh wrappers. Use normal Flutter layout directly when a helper adds no clear value. |
| `widgets/media/` | Media card/gallery/player and capture-related controls. Generic capture mechanics return bytes/files; feature code decides what to share/store. |

Group a substantial cohesive component under its own folder with internal `widgets` or state only when it actually needs them (Bayin's main app bar/drawer are examples). Do not merge unrelated public controls into `app_widgets.dart`, and do not relocate feature business providers into core just because their view looks generic.

Separate public components, but keep private `State` classes and a tightly coupled private implementation with their owning widget. A component's named constructors do not need separate files. Use const constructors/defaults where legal; put runtime context resolution in a dedicated widget's build when that preserves a useful const call site. Do not use a long flag list to simulate unrelated widget variants.

## Helpers, extensions, and utilities

Choose the owner by responsibility, not file length. A helper is a small operation; a service owns an integration; an extension naturally operates on a receiver; a utility owns a reusable object or policy.

| Area | Source examples and transfer rule |
| --- | --- |
| `helpers/map_helpers.dart` | `fromMapOrNull`, `fromMapOrDefault`, map conversion/equality/hash. Preserve required/optional data semantics; do not turn malformed required data into silent defaults. |
| `helpers/list_helpers.dart` | `modelListFromMap`, nullable list parsing, string list conversion, list equality/hash, list query encoding. Reuse constructor tear-offs and existing backend list-parameter conventions. |
| `helpers/focus_helper.dart` | Shared primary unfocus. Keep UI event intent at the caller. |
| `helpers/future_helpers.dart` | A shared delay or provider-retry hook when the behavior is required. Do not copy arbitrary waits or disable retries globally just because the helper exists. |
| `helpers/string_helpers.dart`, `date_time_helpers.dart` | Date/count/price formatting, relative time, parsing. Preserve locale, timezone, plural and rounding semantics; prefer the target's localization contracts over copied business formatting. |
| `helpers/exception_handler.dart` | Map existing typed errors into localized feedback. Keep one translation/mapping owner; do not expose credentials or copy arbitrary raw exceptions into UI. Do not require a global navigator context when the caller can supply current locale/context safely. |
| `helpers/uuid_helper.dart` | Reuse the established identifier generator only where the operation requires it. Do not add per-call IDs blindly to unrelated requests. |
| `extensions/context_extension.dart` | Reactive `locale`, theme/palette, size, direction, insets and common overlay/navigation access. Use `final locale = context.locale` for repeated access within a valid scope. Do not store context-derived values globally. |
| Other extensions | Enum lookup, strings/direction, dates, collection transformations, text/page controller operations, GoRouter parameters. Keep methods receiver-specific and avoid duplicate helpers with different names. |
| `utils/form_validator.dart` | Local plus server-field validation with actual error shape, current locale and form ownership. Domain-specific rules stay scoped instead of copying a baseline's survey/bank constraints. |
| `utils/input_field_formatters.dart`, `phone_field_controller.dart` | Input representation, cursor/controller behavior, formatting. Controller ownership/disposal is explicit; numeric parsing still needs valid-data handling. |
| `utils/decorations.dart`, `superellipse_border.dart`, `custom_edge_padding.dart` | Shared shape/decoration/padding policy using tokens, directional insets and safe areas. Runtime variants need current context; static variants retain const constructors. |
| `utils/custom_exception.dart`, logging utilities | Typed operation errors and the app's actual debug/reporting boundary. Do not add global suppression, secret logging, or a new logging stack for a small change. |

## Services and integration modules

Put each actual service in its own named file. Use a small static facade for stateless calls or an instance/provider for stateful dependencies/lifecycle. Select strategy variants at the integration boundary rather than passing mode flags through each operation. Do not impose an interface and implementation pair on every service.

| Integration | Ownership requirements |
| --- | --- |
| Preferences / secure storage | One initialized preference owner and provider override; stable keys in `StorageKeys`. Secure credentials use the established secure storage owner. Separate ordinary settings from authentication material. |
| `ApiService` | Shared client/config, request/response mapping, language/auth headers, timeout and actual token-refresh coordination. Feature repositories express operations and return typed results. Reuse concurrency/error behavior; do not create one client per screen. |
| `ApiStorageService` | Shared signed-URL/upload/confirmation/progress flow. Feature code supplies endpoint/request differences. Do not equate picking a file with uploading it. |
| `ShareService` | URL/file payloads, MIME/name handling and presentation origin. Generic capture widgets return bytes; feature callers invoke sharing. |
| `MediaPickerService` | Picker APIs, cancellation, format/size/count validation. Callers provide actual permitted formats/limits. Avoid copying silent error-to-empty results or assuming every platform provides local file paths. |
| Location | Service availability, permission request/result, current position and settings APIs in a service; feature/gate owns UX callbacks. Preserve cancellation/mounted behavior. Do not copy unbounded recursive permission retries. |
| Device info | SDK field retrieval and platform choice in a service. Verify actual identifier semantics when required; comments claiming persistence/uniqueness in sample code are not an API guarantee. |
| Social sign-in | Provider SDK operation/token exchange ownership, cancellation/error mapping, and auth-provider handoff. Keep credentials/configuration centralized. |
| URL launcher, review, downloader, speech | Small named services only when the app has the respective feature. Own callbacks/progress/cancellation and lifecycle; do not install or initialize them just to reproduce a catalog. |
| Firebase | Dedicated initialization/options and messaging/events owners under `core/firebase`. Typed event methods/parameters replace repeated raw SDK calls. Preserve subscription disposal and app lifecycle. Never copy another app's project credentials. |
| AppsFlyer / deep links | Service/provider setup, event callbacks and readiness handoff. Navigation uses the single router/container; handler registration does not mean that the router is already mounted. |
| Socket | Socket service/provider, connection state, event/key constants and shared connection-status view. Own connect/auth/reconnect/dispose once; feature handlers subscribe through that owner. |

Bayin has broader integrations than Jawwab. Their presence is evidence of where to put a requested capability, not authorization to add analytics, payment, microphone, location, notifications, or new native permissions to an unrelated app. The main skill's existing native/configuration boundary remains in force.

## Shared data/state and substantial reusable flows

- Shared value types such as nullable-update wrappers, localized text, file/media descriptors and result messages belong in `core/models` (or the established owning module). Feature entities stay in `features/<feature>/data/models`. Keep serialization and equality semantics with the value object.
- Shared preference/session/lifecycle/loader providers stay under the current `core/providers` or `core/controllers`. API request/response state stays under `core/api` when that is the established organization. Do not duplicate global request listeners across screens.
- Pagination is a cohesive module: request/response models, repository, provider, list/grid rendering. Feature providers supply the endpoint/parser/filter configuration. Preserve family keys, current data, retry/refresh behavior and real request ordering.
- `core/kernel/<module>` is for a substantial reused flow with its own data/state/presentation, such as location gating, agreement, or app tour. It is not a destination for every helper or an excuse to add domain layers everywhere. Keep specialized controller/animation/overlay ownership where the module actually needs it.
- Barrels are optional public import surfaces in the target's style. They contain exports only, should not create import cycles, and must not conceal feature implementations inside a core catch-all file.

## Source coverage and precedence

The structural inventory covered the handwritten `lib` trees of Bayin and Jawwab. The maintained rules use inspected startup, route declarations/providers/extensions, preferences, tokens/themes, helper/service implementations, request state, model/repository flows, pagination, validation, and representative widget implementations/callers. Individual implementation details must still be validated in a target app. Do not treat this catalog as proof that every historical class is correct or should be copied.

Concrete anchors include Bayin `core/{constants,theme,controllers,routes,services,helpers,widgets}`, auth/notifications/project features, and Jawwab `core/{styles,constants,api,pagination,providers,routes,kernel,services,helpers,widgets}`, wallet/profile/community flows. The reference checkouts are provenance only; this plugin must carry the rules without requiring future access to those checkouts.
