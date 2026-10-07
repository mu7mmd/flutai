# Localization, configuration, assets, and startup

Read this reference for user-facing text, asset/font registration, environment configuration, app initialization, or locale/theme preferences.

## Translation and direction

Both reference apps store source messages in `assets/l10n/*.arb`, configure generation in `l10n.yaml`, expose `AppLocalizations`, and consume it through `context.locale`. Alias repeated lookup with `final locale = context.locale;`. Use generated getters/methods and real keys; do not scatter user-facing string literals, language ternaries, or a separate hand-written translation map through widgets.

The inspected template differs: Bayin uses `en.arb`, Jawwab uses `ar.arb`. Inspect the target's generator configuration rather than assuming English or Arabic. Update the source catalogs relevant to the supported locales and preserve placeholder names/types and message metadata. Do not hand-edit `lib/generated/l10n` or invent translated copy without accounting for all requested locales.

Distinguish app UI translation from API-provided localized content. Jawwab's `LocalizedTextModel`/`LabelValueModel` provide a translation accessor such as `.tr(context.langCode)` for data labels. Preserve their actual fallback and identifier semantics; these models do not replace ARB UI translations.

Use the project's directional padding, alignment, arrow/text helpers, and current safe-area/keyboard accessors. Preserve intentionally LTR content such as a URL or identifier inside an RTL layout. Reuse shared date/count/price formatters when their semantics match the requirement instead of repeating formatting in the UI.

Locale preferences are owned by the existing user-preferences provider and `StorageKeys`. Preserve updates to app locale, persistence, API language, and any existing server preference flow. Resolve locale-dependent fonts in the text styles layer as described in [design-tokens.md](design-tokens.md).

Audit all supported catalogs and the complete language-picker list when adding copy. Keep directional arrows in a shared helper and verify their actual glyphs; retain intentionally LTR identifiers. See [design-fidelity.md](design-fidelity.md#geometry-surfaces-and-icons) for icon and brand-asset rules. A source rename must not change translated branding or persisted/API values.

## Constants, assets, and config

Keep stable shared values in their specific owner, not a generic catch-all file:

| Value | Owner pattern |
| --- | --- |
| Colors, geometry, typography | `AppColors`/resolved palette, `AppSizes`, `TextStyles`, `AppFonts`, existing decoration/shape owners. |
| Asset references | Existing `AppImages`, `SvgIcons`, animation/icon definitions; Jawwab wraps paths in `AppImage`, `SvgIcon`, and `JsonAnimation`. |
| API contracts | Existing `ApiEndpoints`, `ApiKeys`, typed enums/models, and request serialization. |
| Persisted preference/session key names | `StorageKeys`, with the current shared-preferences/secure-storage providers. |
| Environment-dependent integration config | Existing `AppConfig` and environment injection/generation. |

Use named asset values with existing image/SVG widgets; avoid raw asset paths scattered in screens. Register new asset/font resources through the target's actual `pubspec.yaml` structure when required. Use its registered font family and weight mappings rather than copying either baseline app's font or branding.

Both apps use an Envied-backed `AppConfig`, with different fields and locations. Extend the current mechanism instead of adding another config service or reading environment values independently in feature widgets. Keep credentials and generated secret-bearing values out of examples and plugin instructions. Existing hardcoded integration values in a reference app are not a pattern to reproduce.

## Initialization and app composition

Document implemented configuration, environments, generation/setup requirements, settings, and affected version constraints in the relevant project-root `documentation/` files. Explain actual owners, keys/defaults, and commands; keep essential non-obvious rationale near its code. Follow [documentation.md](documentation.md) and update the explanations with configuration changes.

`main.dart` owns required initialization order and provider overrides for initialized dependencies such as preferences/storage. `app.dart` composes `MaterialApp.router`, the router provider, locale/delegates/supported locales, the theme, and app-level response listeners. Reuse those owners when adding a dependency or app-wide preference; do not initialize integrations in each feature's build method.

Keep global request/error listeners attached to their intended provider scope. Preserve the app's existing authentication, socket, messaging, and deep-link lifecycle when touching initialization. Await only what later steps depend on, following the async contract guidance in [coding-style.md](coding-style.md). SDK or native configuration changes remain subject to the main skill's concrete approval boundary.

## Source anchors

Inspected on 2026-10-03: both `main.dart`, `app.dart`, `pubspec.yaml`, `l10n.yaml`, ARB structure, constants, context extensions, and user-preferences implementations; Bayin `lib/core/config/app_config.dart`; Jawwab `lib/config/app_config.dart` and `lib/core/models/localized_text_model.dart`. These paths document the baseline and are not prerequisites for future tasks.
