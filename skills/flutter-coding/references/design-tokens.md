# Themes, text styles, and visual tokens

Read this reference when implementing or changing themes, colors, typography, or shared visual definitions. Follow the target project's existing names and actual design values; this plugin defines coding rules, not an app's brand palette or font sizes. Keep the change limited to the requested work and affected callers.

## Design Linking

Apply the owner's **Design Linking** principle as a strict consistency requirement: every occurrence of the same component or visual role uses its shared implementation and established design rules. A button, text field, tile, dialog, or sheet must not drift in padding, shape, colors, icon treatment, typography, size, spacing, or animation just because it appears on another screen. Link designs through their actual component/theme/token owners, so a deliberate shared change reaches their callers coherently.

Before any UI addition or change:

1. Search the existing shared/core and feature components, theme configuration, visual tokens, and representative usages. Inspect the actual matching implementation and its callers instead of recreating an approximation from memory.
2. Reuse the matching component and its default design. Pass differing content, models, labels, controllers, callbacks, or supported optional parameters. Keep common visual defaults with their existing owner.
3. If a real design difference is required, extend the existing component with the smallest useful parameter or EOC specialization. Use a named reusable variant for a recurring specialization; do not scatter one-off style overrides across screens.
4. If no component exists, inspect comparable existing UI and build the smallest reusable component from that same design system. Match its token scale, geometry, typography, color roles, icon family, layout rhythm, and interaction states. Put it in the correct widget family/feature owner and use it for the affected callers.
5. Compare the result with the reference usages before finishing. Trace every deliberate change to its shared component/token or a genuine specified variant. Arbitrary local styling is a consistency defect.

Keep these contracts together in their actual shared owners:

| Family | Linked design contract |
| --- | --- |
| Buttons | Height, padding, radius, label style, icon treatment, loading/disabled/pressed states, and semantic action variants. |
| Text fields | Background, content padding, border/radius, labels/hints, input text, prefix/suffix icons, focus/error/disabled states, and validation layout. |
| Tiles/cards | Insets, leading/trailing icon geometry, text hierarchy, item gaps, border/radius, surface/shadow, and selection states. |
| Layout | Page insets, gaps between controls, sections and actions, alignment, and the established responsive spacing rules. |
| Icons | Existing icon/asset family, size/stroke treatment, color roles, and directional behavior. |
| Dialogs | Surface/radius, insets, title placement/style, title/body/action gaps, button styles/order/alignment, and entry/exit animation. |
| Sheets | Surface/top radius, handle/header/title layout, content/action padding, safe-area/keyboard spacing, button treatment, and transition duration/curve. |

Use one shared dialog presentation/shell and one shared sheet presentation/shell, or their existing equivalents, with parameters for titles, content, and actions. Reuse the existing overlay launch helpers too, so transition and presentation defaults remain linked. Confirmation, error, and feature-specific overlays compose those owners instead of each building their own title/padding/buttons. Keep `OK`/confirm and cancel actions consistent with the app's established action roles and layout; preserve result, dismissal, keyboard, and navigation contracts.

Optional style parameters serve genuine supported differences; their presence does not authorize arbitrary padding/radius/color overrides at each call. Give recurring variants one owner through EOC. Distinct semantic roles, themes, responsive states, and explicitly supplied designs can have their own coherent variants; keep each variant consistent wherever used. Do not flatten those distinctions or silently adopt inconsistent historical call sites as a second design standard.

For a new app, establish its required tokens and shared component families from the requested design before repeating UI. For an existing app, retain its established design system and keep the work scoped to the requested changes and affected callers. If existing examples conflict, identify the canonical shared owner and relevant design intent; ask only when a material design decision is genuinely unresolved. Do not launch an unrelated app-wide redesign.

Record actual component owners, defaults, and supported variants in project-root `documentation/` when introduced or changed, following [documentation.md](documentation.md). Verify rendered appearances against representative usages when preview/device tools are available, including relevant theme/locale/responsive states. Source or token checks alone do not prove visual consistency; report what could actually be checked.

For concrete geometry, border exceptions, whole-surface ink, verified glyphs, and skeleton parity, also read [design-fidelity.md](design-fidelity.md). For viewport ownership, shared sheets, and dismissal contracts read [scroll-and-overlays.md](scroll-and-overlays.md). These rules refine Design Linking; matching token names alone is insufficient.

## Select the mode once

Define complete light and dark color sets with the same semantic fields in their owning class or file. The owner's preferred shape is an abstract palette contract with separate concrete light and dark classes, such as `ThemedColors`, `LightColors`, and `DarkColors`. Use constant instances where possible. Each class contains its concrete values; its fields and getters do not branch on brightness. An existing equivalent immutable palette/theme-extension design can be retained without an unrelated migration, but do not introduce a boolean-driven palette that switches each field internally.

Bayin's concrete pattern is `ThemedColors` with `LightColors.instance` and `DarkColors.instance`; consumers use `context.themedColors`. Its shared derived gradients use the selected object's fields. Carry this ownership pattern forward, not its exact color values or numbered field names. Jawwab currently supplies a light theme; do not add dark-mode behavior to an app merely to reproduce Bayin's capabilities.

Select the appropriate complete theme/palette at the theme boundary, then pass or expose that resolved object to consumers. A shared theme builder receives the selected palette, not an `isDark` flag that it rechecks for every color. When the app already uses `theme`, `darkTheme`, and `themeMode`, let that boundary perform the selection instead of adding another brightness switch. Respect the app's existing system/manual theme behavior.

Theme assembly and widgets read semantic fields such as `colors.surface` and `colors.onSurface`. Do not scatter `isDark ? ... : ...` across widgets, constructors, text styles, or palette getters. Resolve any other mode-dependent token group at its owning boundary in the same way. Keep context-derived access reactive so changing the active theme updates the UI.

## Consume named text style tokens

Define reusable typography in a dedicated `TextStyles` class/file. Use the owner's established role → size → weight structure where it fits. Jawwab exposes `TextStyles.text.md.bold`, `TextStyles.display.xs.regular`, and purpose aliases `TextStyles.field`, `TextStyles.fieldHint`, and `TextStyles.appBar`. Bayin uses `TextStyles.body.medium?.light` and `TextStyles.display.medium?.bold`. Follow the target's names; do not invent a second `AppTextStyles` API beside an existing `TextStyles`.

Roles such as `label`, `display`, and `callout` and weights such as `light`, `regular`, and `bold` belong in this layer when required by the design. Add only actual variants. A simpler role → weight shape is sufficient when no size variants are needed. Preserve meaningful optionality in existing APIs; newly defined required tokens should be usable without unnecessary nullable access.

Consumer syntax from Jawwab's existing token API:

```dart
Text(title, style: TextStyles.display.xs.bold);
Text(message, style: TextStyles.text.md.light);
Text(label, style: TextStyles.text.sm.bold);
```

These are ready-to-use style tokens. Do not require consumers to instantiate a styles class, construct `TextStyle(...)` inline, or recreate a role through repeated `copyWith(fontSize: ..., fontWeight: ...)`. Theme assembly also uses these tokens when mapping the app's typography into `TextTheme`; placing raw text style definitions inside a theme is not sufficient centralization.

Construct `TextStyle` values inside the text styles implementation, where their font family, size, weight, height, and spacing are owned together. Resolve `AppFonts` directly in that layer, not independently in widgets or the theme builder. If text colors vary by theme, compose the styles from the resolved palette in this layer without internal brightness conditions. A caller may apply a truly local semantic override through the existing token API; repeated variants become named tokens.

Jawwab's private `_TextStyleSizes` and `_TextStyleWeights` provide ready values; `_unifiedStyle` applies `FontWeights`, `AppFonts`, and the project's line-height/letter-spacing conversion once. Preserve that conversion when adapting those tokens; do not feed the raw design numbers directly into consumer styles or normalize them twice. Keep font-family identifiers in `AppFonts` and font weights with the typography definitions or existing dedicated file.

The owner's current instruction supersedes the inspected themes' repeated `AppFonts.fromLangCode(...)` and `copyWith(fontFamily: ...)` calls. Move font resolution into the typography owner when changing that code. For locale-dependent fonts, resolve/update the style set with the active locale; a one-time static value must not retain the previous locale's font. Do not copy `AppFonts.current` merely because it exists in the source.

## Keep related definitions together

Use the same ownership principle for shared radii, spacing, shadows, asset references, and other visual definitions that the task introduces or reuses: define them in the appropriate existing class/file and consume their named values. Extend the current owner before adding another wrapper or competing constants file. Preserve actual design values and avoid creating unused tokens, generic registries, or a repository-wide design-system migration for a focused change.

Observed owners include `AppColors`, `AppSizes`, `AppShadow`, `FieldDecoration`, `FieldOutlinedBorder`, `SuperellipseBorder`, and `CustomEdgePadding`. Component defaults stay in the shared component/theme; feature callers pass only genuine differences. Fixed brand colors remain direct constants, while colors that vary by mode come from the resolved palette.

## Source anchors

Inspected on 2026-10-03: Bayin `lib/core/constants/{app_colors,text_styles,app_fonts,font_weights}.dart` and `lib/core/theme/app_theme.dart`; Jawwab `lib/core/styles/{text_styles,app_theme}.dart`, `lib/core/constants/{app_fonts,app_sizes}.dart`, and `lib/core/utils/{decorations,custom_edge_padding,superellipse_border}.dart`. These are provenance, not files that must be rediscovered before applying this reference.
