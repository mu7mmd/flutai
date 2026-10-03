# Project organization learned from Bayin and Jawwab

Use this reference when choosing where new code belongs or connecting several layers. It captures the owner's required baseline from source inspected on 2026-10-03. For creation/redesign, start with [project-blueprint.md](project-blueprint.md); for a feature, use [feature-blueprint.md](feature-blueprint.md). Apply the bundled guidance directly. Preserve established equivalent names in an existing app, but do not adopt a flattened generated structure as the baseline. The source apps need not exist on the task's machine.

## Responsibilities and locations

| Responsibility | Established location and ownership |
| --- | --- |
| App initialization | `main.dart` initializes required SDKs/storage and provider overrides; `app.dart` composes router, locale, theme, and app-level listeners. |
| Shared design definitions | `core/constants` owns colors, sizes, assets, font identifiers, storage keys, and enums. Typography/theme live in `core/styles` in Jawwab, and `core/constants/text_styles.dart` plus `core/theme` in Bayin. |
| Feature data | `features/<feature>/data/models` contains typed data/request objects; `data/repositories` contains that feature's API operations. |
| Feature state and actions | Jawwab commonly uses `features/<feature>/providers`; Bayin uses existing `controllers/notifiers`, `controllers/providers`, and some `providers` folders. Extend the actual neighborhood. |
| Feature UI | `presentation/screens` assembles the screen; `presentation/widgets` contains feature-specific cards, sheets, sections, and forms. |
| Cross-feature widgets | `core/widgets/`, with family folders for buttons, text fields, images, text, cards, scaffolds, overlays, dropdowns, and selection sheets. One public reusable component per file; export barrels contain no implementations. |
| Reusable non-UI work | `core/services` for integration ownership; `core/helpers` for small shared functions; `core/extensions` for operations naturally attached to an existing type; `core/utils` for validators, formatters, decorators, and controllers. |
| Shared infrastructure | Existing `core/api`, `core/pagination`, `core/routes`, `core/socket`, and `core/firebase` modules own their corresponding infrastructure. Bayin keeps some providers in `core/controllers`. |
| Shared modules with their own flow | Jawwab's `core/kernel` contains modules such as location, agreement, and app tour, each with only the data/state/presentation parts it needs. Use this pattern for a real cross-feature module, not every helper. |
| Configuration and localization | Existing `config/app_config.dart` or `core/config/app_config.dart`; `assets/l10n/*.arb`, `l10n.yaml`, and generated localization output. |

Scope controls which capabilities are implemented, not whether their files are correctly organized. A complete new app needs the connected foundation in the project blueprint. A data-backed feature needs its model, repository, state, screen, and widget ownership. A static screen does not need a fake repository, and an existing reused repository does not need an empty duplicate. Do not scaffold empty layers, copy every SDK from the reference apps, or migrate unrelated existing code. An additional domain/use-case/interface layer is not a default part of this baseline.

## How a feature connects

The usual flow is screen/shared widget → provider/notifier action → feature repository → shared API service. Repositories map transport responses into models; providers coordinate loading, result state, refresh, and callbacks; screens compose presentation. SDK-specific work goes through its existing service. A simple action may use the existing request guard without creating a new notifier for ceremony.

Move repeated visual behavior into the smallest shared widget and repeated non-visual work into its actual owner. Keep feature business decisions in the feature. Do not make a shared capture widget understand referral rewards, a media picker understand a profile update, or a generic pagination service understand survey eligibility.

Use named constructors or a small variant API when they share one implementation. Keep the internal implementation private when it is not a consumer API. Preserve the target's direct relative imports, selective `show`/`hide`, purposeful re-exports, and existing barrel conventions; do not add a global export barrel or rewrite imports across unrelated files.

## Read the relevant detail

- Visual values and fonts: [design-tokens.md](design-tokens.md).
- Widget composition, small helpers, and SDK services: [shared-components.md](shared-components.md).
- Data, state, pagination, and route contracts: [data-and-state.md](data-and-state.md).
- Translation, assets, configuration, and startup: [localization-and-config.md](localization-and-config.md).
- Complete project and alternate-tree creation: [project-blueprint.md](project-blueprint.md).
- New feature placement and implementation: [feature-blueprint.md](feature-blueprint.md).
- Detailed core owners and reusable families: [core-catalog.md](core-catalog.md).
- Router contracts and lifecycle: [routing.md](routing.md).

## Evidence and limits

Concrete flows include Bayin's `features/auth/presentation/screens/login_screen.dart` → `presentation/widgets/auth_scaffold.dart`, Bayin's notifications screen/repository, Jawwab's `features/wallet/providers/manage_bank_account_provider.dart` → `data/repositories/wallet_repo.dart`, and Jawwab's referral screen → `core/widgets/widget_to_image.dart` → `core/services/share_service.dart`.

These projects are examples of organization, not bug-free templates. The owner's current requests take priority over incidental duplication, nested conditions, direct font calls, global context access, stale comments, or unsafe assumptions found in them. Transfer the useful responsibility boundaries, not brand values, business policies, credentials, or every existing implementation detail.
