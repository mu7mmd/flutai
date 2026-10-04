# Creating a project or complete redesign

Read before creating a Flutter app, replacement app, full redesign, or alternate source tree. This is the owner's required creation workflow, not an optional cleanup after drawing screens. It incorporates the reported failure where an alternate tree placed screens at feature roots and combined shared controls in `core/widgets.dart`.

## Establish the real boundary

Resolve the destination, package name, SDK constraints, supported platforms/locales, supplied design, and source of data. Inspect the target before generating files. Reuse existing configuration and dependencies when working in a repository; do not select package versions from these reference snapshots.

Choose the mode supported by the request and files:

| Mode | Required behavior |
| --- | --- |
| New standalone project | Create its own connected foundation, feature layers, assets/localization configuration, and entry point. It must run without imports from the reference apps or another checkout. |
| Same-project redesign / `lib2` | Preserve the architecture inside the new tree. Reuse existing data, state, integrations, locale catalogs, or typography through explicit imports when their behavior remains valid. Give every reused capability a concrete owning path. New screens/widgets still use the required directories. |
| Independent copy of an existing app | Bring the required foundation and authorized resources into the destination; update package/import paths, entry point, generated-code configuration, assets, and route ownership. Do not leave hidden dependencies on the original checkout. |
| Focused feature/change | Add the needed slice using [feature-blueprint.md](feature-blueprint.md); preserve the rest of the app. |

An alternate entry point does not authorize a second initialization of Firebase, storage, sockets, or analytics. Reuse the existing bootstrap/container or factor the smallest shared bootstrap with a clear owner. A redesign is not permission to invent successful API actions or discard existing auth, localization, validation, permissions, payments, or navigation contracts.

## Plan owners before screens

Derive a concise responsibility map from the actual scope: entry point, app composition, tokens, preferences, router, features, data sources, and integrations. For each capability record its destination or exact reused owner. This is part of implementation planning, not a user approval gate or a project-local FLUTAI instruction file. Resolve ordinary naming choices yourself.

Use this default tree for a **new** project. Items marked `when used` require a real capability; do not fill them with empty files. Existing equivalent Bayin/Jawwab names are supported as described in [project-structure.md](project-structure.md).

```text
lib/
  main.dart
  app.dart
  core/
    config/
      app_config.dart
    constants/
      app_colors.dart
      app_sizes.dart
      app_fonts.dart
      app_assets.dart                    # when assets are used
      app_locales.dart
      storage_keys.dart                  # when preferences/session persist
      key_enums.dart                     # actual shared enums only
    themes/
      app_theme.dart
      colors/
        themed_colors.dart
        light_colors.dart
        dark_colors.dart                 # when dark mode is supported
    styles/
      text_styles.dart
      font_weights.dart
    extensions/
      context_extension.dart
      go_router_extensions.dart          # when shared parameter access is used
    helpers/
      focus_helper.dart                  # when forms use shared unfocus
      map_helpers.dart                   # when parsing data
      exception_handler.dart             # when mapping operation errors
    services/
      preferences_service.dart           # default small persistence owner
      share_service.dart                 # when sharing is required
      media_picker_service.dart          # when picking media is required
    providers/
      shared_prefs_provider.dart          # or the established equivalent
      user_preferences_notifier.dart
      user_preferences_state.dart
      secure_storage_provider.dart       # when credentials persist
    api/                                 # when the app has API-backed features
      api_service.dart
      constants/
        api_endpoints.dart
        api_keys.dart
      models/
        response_model.dart
        future_state.dart                # if this state abstraction is used
      providers/
        api_request_provider.dart        # if shared command feedback is used
        api_response_provider.dart       # if global response handling is used
    models/                              # real cross-feature value objects
      nullable_value.dart                # when copyWith must explicitly clear
    routes/
      app_routes.dart
      go_router_provider.dart
      route_not_found_screen.dart
      screens_export.dart                # optional export-only router barrel
    utils/
      form_validator.dart                # when forms are present
      input_field_formatters.dart         # formatters actually needed
      decorations.dart                   # common field/card decoration policy
      custom_edge_padding.dart           # if useful for the supplied design
    widgets/
      buttons/
        app_button.dart
        app_icon_button.dart
        app_outlined_button.dart         # when used
        app_state_button.dart            # when async controls are used
      text/
        strut_text.dart                   # or app_text.dart with required behavior
      text_fields/
        app_text_field.dart              # when forms/search are present
        search_text_field.dart           # when used
      images/
        app_asset_image.dart             # when used
        app_asset_svg.dart               # when used
        app_network_image.dart           # when used
      cards/
        basic_card.dart                   # when card surfaces are used
      scaffolds/
        app_scaffold.dart
      app_bars/
        app_app_bar.dart
      feedback/
        loading_widget.dart
        retry_widget.dart
        empty_state_widget.dart
      overlays/                          # dialogs/sheets, one public widget per file
      layout/                            # repeated layout/spacing components
      navigation/                        # shared navigation controls/shell UI
    pagination/                          # only for paginated data
      data/models/
      data/repositories/
      providers/
      widgets/
    firebase/                            # only for configured Firebase capabilities
    socket/                              # only for a real socket integration
    kernel/                              # substantial cross-feature flows only
  features/
    <feature>/
      data/
        models/
        repositories/
      providers/                         # or established controllers structure
      presentation/
        screens/
        widgets/
  generated/l10n/                        # generated, never hand-written
assets/
  l10n/
    <locale>.arb
  fonts/                                 # actual supplied/authorized font files
  images/                                # actual assets
  icons/                                 # actual assets
test/
  core/                                  # meaningful infrastructure checks
  features/                              # relevant behavior checks
pubspec.yaml
l10n.yaml
```

The tree specifies ownership, not a demand to create every optional service. A standard app foundation includes the entry point/app, config, colors/sizes/fonts/typography/theme, locale support, context access, router, shared shell/controls, and preferences when settings are part of the app. Implement helpers and services for the actual shared work from the beginning; do not push that work into screens and call those folders unnecessary. If persistence is absent, do not add a preference SDK solely to fill the example tree. If a capability is outside scope or reused, state that with its reason/path in the completion report. An empty directory or `UnimplementedError` stub does not satisfy a capability.

`themes/` is the default new-project spelling; `theme/` in Bayin and `styles/app_theme.dart` in Jawwab are established equivalents. Do not create competing theme owners. Likewise, preserve `core/config/` versus an existing `lib/config/`, and existing `button/` versus `buttons/`. The layer boundaries and separation matter; renaming equivalent directories across an existing app does not.

## Build and connect the foundation

1. **Configuration:** one typed `AppConfig` owns environment-dependent values. Use the existing Envied setup when extending it; a small new app may use a typed compile-time configuration. Keep real credentials out of generated examples. Add only required dependencies and font/assets declarations. Do not copy baseline endpoints, keys, app IDs, or branding.
2. **Tokens:** implement colors, sizes, font identifiers, text styles, and theme in their owners. Theme palettes have a shared contract and direct concrete values. Select a palette once; widgets consume the selected palette. Typography owns `AppFonts`, role/size/weight definitions, and locale-dependent resolution. Read [design-tokens.md](design-tokens.md).
3. **Reusable UI:** implement the controls actually used by the first flow in the family folders, then consume them from that flow. Separate button, icon button, text, fields, images, cards, scaffolds, and feedback files. Do not create a single mixed `core/widgets.dart`, `common.dart`, or `components.dart` implementation. Existing `widgets.dart` barrels remain exports only.
4. **Localization/preferences:** create the requested ARB catalogs and generator configuration; bind delegates, supported locales, and active locale in the app. Own persistence in the existing provider/service, and apply theme/locale changes reactively. Do not use widget-level language booleans or handwritten translation dictionaries. Read [localization-and-config.md](localization-and-config.md).
5. **Infrastructure:** connect initialized dependencies to the provider scope, install the required API/error/form/async/pagination owners, and place actual SDK operations in services. A real repository consumes those owners; screens do not perform transport/storage setup.
6. **Routing:** define paths and argument contracts in `AppRoutes` and create the GoRouter in its provider, wired to `MaterialApp.router`. Compose shells through child slots. Retain a navigable missing-route state. Read [routing.md](routing.md).
7. **Features:** implement the first real end-to-end slice before scaling out more screens. Its typed data → repository → state → UI and navigation must be connected. Apply [feature-blueprint.md](feature-blueprint.md) to every further feature.

Use the project's actual SDK syntax and generator versions. A sample in the reference apps is evidence of responsibility, not a reason to change the target's package versions or introduce every integration the apps happen to use.

## Same-project redesign without flattening

For a new source root such as `lib2`, keep `features/<feature>/presentation/screens` and `presentation/widgets`, and organize new shared controls below `core/widgets/<family>/`. New token/theme files belong in their corresponding directories; new route assembly belongs in `core/routes/`.

Reuse an existing repository/model/service directly when that is intentional. For example, a new `lib2/features/profile/presentation/screens/profile_screen.dart` may consume a provider whose owner remains `lib/features/profile/providers/`; record that dependency. Do not create duplicate unused repositories, fake models, or forwarding files just to make the tree look complete. If the requested result is independent, complete the migration/copy needed for independence instead of silently treating it as an alternate entry point.

Separate ownership of navigation state, shell UI, and auth guards. Do not create two unrelated navigator keys or initialization containers accidentally. If old feature flows are embedded temporarily, make their adapter a focused file, retain required inherited/provider scope, and disclose exactly which views remain reused. A new visual shell alone is not a complete redesign of every screen.

For unavailable backend capabilities, keep typed local form state and organized presentation. Do not fabricate endpoint URLs, record lists, saves, balances, or successful network operations. Implement the data layer when its actual contract is available; report the missing contract precisely.

## Completion checks

Before saying a project/redesign is finished:

- Compare the actual file tree to the responsibility map. Screen, widget, state, repository, model, service, config, token, locale, route, and startup responsibilities must have concrete owners. Account for every applicable foundation item through an implemented path or a deliberately reused path.
- Trace at least one actual user flow through navigation, screen composition, provider, repository, and shared infrastructure. For a UI-only scope, verify honest disabled/unavailable behavior instead of claiming a connected service.
- Confirm no feature-root screen files, no combined shared-widget implementation, no screen-owned API/storage configuration, and no handwritten generated outputs.
- Confirm styles/fonts/sizes/assets are consumed from their owners. Check light/dark and locale/font changes when supported, as well as directional layout, long text, and narrow layouts in affected UI.
- Check [Design Linking](design-tokens.md#design-linking): repeated components and overlays share their implementation and design defaults; new components match established tokens, layout rhythm, icon treatment, states, and transitions. Compare representative usages and verify rendered consistency when available.
- Verify router arguments, back/pop results, signed-in/out destinations, and direct detail links where applicable. Do not infer runtime protection from an initial route alone.
- Run formatting, focused analysis, required generation, and meaningful existing behavior checks. Run the structure checker below; review its warnings and its untested boundaries.
- Maintain project-root `documentation/` for implemented architecture/features, requirements, configuration/settings, and actual version constraints. Split independent topics, verify explanations against source, and keep comments selective. Follow [documentation.md](documentation.md).
- Report implemented/reused modules, concrete validation results, and remaining integration/device limitations. A successful screenshot or bundle build does not prove architecture, and directory presence does not prove the implementation works.

## Structure checker

Run the bundled script via its resolved skill directory, not a copied project-local FLUTAI folder:

```sh
python3 <skill-dir>/scripts/check_structure.py /path/to/project --source-root lib
python3 <skill-dir>/scripts/check_structure.py /path/to/project --source-root lib2 --shared-root lib
python3 <skill-dir>/scripts/check_structure.py /path/to/project --feature wallet --requires-data
```

The default is a project foundation and placement check. `--feature` limits checks to that feature and does not demand rebuilding the app foundation. `--requires-data` requires model/repository/state implementation files for that feature; `--shared-root` can point to deliberately reused owners inside the same project with the same feature name. Declare `--requires-data` for a data-backed new feature; use the manual capability map to check every data-backed feature in a complete app. For a verified generic-pagination repository reuse, pass `--repository-owner lib/core/pagination/data/repositories/pagination_repo.dart`; this records the explicit owner without demanding an empty feature repository. The flag checks that file's presence, not its wiring. Cross-feature reuse with different names still needs a manual owner/import review.

Exit 1 means structural findings; exit 2 means invalid arguments/paths. The checker never creates or moves files, installs dependencies, or contacts services. It recognizes generated-file suffixes and established naming variants. Its lightweight declaration scan produces **review warnings**, not Dart semantic proof. It cannot verify actual imports, token reactivity, route guards, business behavior, missing service contracts, or a correct implementation hidden behind an existing filename. Perform those completion checks separately; do not create dummy files merely to satisfy it.
