---
name: flutter-coding
description: Create, redesign, extend, debug, and review Flutter/Dart projects in the owner's Bayin/Jawwab architecture. Use layered features, organized core components, complete theme palettes, named style tokens, Extend Over Conditions (EOC), Design Linking, precise scrolling/overlay contracts, and state-safe interactions.
---

# Flutter coding with FLUTAI

Write code the owner can understand immediately: direct, concise, connected through reusable components, and only as complex as the current behavior requires. Precision and readable code are both requirements; do not trade correct behavior for fewer lines. Use the host's project and development tools; this plugin supplies instructions, not a Flutter SDK or repository/device access.

## Start with the bundled rules and relevant source

Before a project answer, source edit, or project task:

1. Resolve the intended project root and follow applicable `AGENTS.md` instructions. Do not silently switch to a previously inspected project.
2. Use this skill and its bundled references as the FLUTAI rules. Do not search for, require, create, or update a project-local FLUTAI instruction folder as an initialization or learning step.
3. Read [coding-style.md](references/coding-style.md). Inspect the relevant source and nearby callers before selecting a pattern. Check the current project's SDK, dependencies, and generator configuration when relevant.

## Choose the task mode before writing files

**Creating a project, a replacement app, or a complete redesign is an architecture task as well as a UI task.** The owner requires the Bayin/Jawwab organization; fewer files is not a reason to flatten it. These requirements also apply to an alternate source tree such as `lib2` and to a visually focused prototype unless the user explicitly requests a different structure.

- **New project / complete redesign / alternate entry point:** read [project-blueprint.md](references/project-blueprint.md), [project-structure.md](references/project-structure.md), [core-catalog.md](references/core-catalog.md), [design-tokens.md](references/design-tokens.md), [localization-and-config.md](references/localization-and-config.md), and [routing.md](references/routing.md) before implementation. Read [feature-blueprint.md](references/feature-blueprint.md) and [data-and-state.md](references/data-and-state.md) for its features. Implement and connect the applicable foundation; a folder list or several visual screens is not a complete app foundation.
- **New feature / new feature flow:** read [feature-blueprint.md](references/feature-blueprint.md) and [project-structure.md](references/project-structure.md), plus the relevant ownership references below. Put screens in `features/<feature>/presentation/screens`, feature widgets in sibling `presentation/widgets`, models in `data/models`, repositories in `data/repositories`, and state in the established `providers` or `controllers` branch. Do not put screens directly in the feature root.
- **Focused edit / debugging / review:** inspect the relevant callers and retain the target's established ownership; do not migrate unrelated files. The minimum required fix still belongs in its proper layer.

For new shared UI, `core/widgets/` is a directory. Group families such as `buttons/`, `text/`, `text_fields/`, `images/`, `cards/`, and `scaffolds/`; follow an existing equivalent singular spelling when extending a project. Give each public reusable component its own file. `widgets.dart` can be an export-only barrel, never the implementation of all controls. The same separation applies to constants, styles, themes, services, helpers, config, and routes.

The bundled [project-structure.md](references/project-structure.md) describes the owner's Bayin/Jawwab organization. Read it when placing new code or working across layers, then use the relevant detailed reference:

- Any UI creation/redesign/consistency change: [design-fidelity.md](references/design-fidelity.md). Read [scroll-and-overlays.md](references/scroll-and-overlays.md) for scrolling, insets, sheets, dialogs, popups, tabs, or keyboard layout. Read [interaction-lifecycle.md](references/interaction-lifecycle.md) for navigation, focus, auth/session, search state, or audio behavior. These are required task-specific extensions of Design Linking. The scoped [owner feedback cases](references/owner-feedback-cases.md) preserve detailed decisions, exceptions, and superseded requests; use them for the corresponding features, not as another app's business specification.
- Themes, constants, fonts, and text styles: [design-tokens.md](references/design-tokens.md).
- Widgets, helpers, extensions, and services: [shared-components.md](references/shared-components.md).
- API, models, Riverpod state, and pagination: [data-and-state.md](references/data-and-state.md).
- Route paths, router ownership, navigation, and deep links: [routing.md](references/routing.md).
- Translation, configuration, assets, and startup: [localization-and-config.md](references/localization-and-config.md).
- Project documentation and selective source comments: [documentation.md](references/documentation.md). Read when implementing or changing code, requirements, configuration, settings, or version constraints.

These references carry the learned conventions. Do not require access to the original Bayin/Jawwab checkouts or copy their source into each task.

Do not report missing project-local FLUTAI files or ask the owner to supply them. Read a separately supplied instruction file when the user or applicable project instructions explicitly direct you to it. If required source exists but is inaccessible, obtain access before making dependent changes. Ask for the project location if no target is available.

Follow the instruction hierarchy and current user request. Historical code is evidence of style, not proof of correctness. The user's explicit preferences take precedence over an inferred pattern.

## Owner's working rules

- Follow the [Dart import rules](references/coding-style.md#dart-imports): direct Flutter/dependency imports, relative project imports ordered farthest to nearest, one blank line between groups, and purposeful `show`/`hide`.
- Prefer [Dart dot shorthands](references/coding-style.md#dot-shorthands) wherever the effective language version and context support them: `.ellipsis`, `.center`, named constructors, `.new(...)`, and eligible static members. Apply this to Flutter, dependency, and project APIs in new/touched code. Preserve the resolved type, member, generics, and `const`; keep explicit qualification where shorthand cannot resolve correctly.
- Add source comments selectively for non-obvious logic, complex conditions/algorithms, meaningful values, and implementation choices made for a specific reason. Explain the reason or constraint near the relevant code; avoid comments above every class, method, widget, or straightforward statement. Maintain developer documentation for all new/changed implementation in the project-root `documentation/` folder, split by topic when useful, such as `config_doc.md`, `code_doc.md`, `settings_doc.md`, and `versions_doc.md`. Follow [documentation.md](references/documentation.md).
- Use the simplest sufficient implementation. Avoid speculative features, future-proof layers, new dependencies, extra state, wrappers, or defensive machinery without a concrete present need.
- Apply DRY from the **second use**. Search for existing reusable code first. Share repeated behavior, validation, mapping, UI, configuration values, and calculations through the smallest suitable function, method, widget, service, model member, or constant. Update the relevant callers so later changes have one owner.
- Within the same block, alias repeated access: `final locale = context.locale;` followed by `locale.hi` and `locale.you`. Apply this to other repeated stable expressions too. Keep the alias local to the scope where the value remains valid.
- Introduce variables when they remove repeated work or access, communicate meaning, or safely hold a needed value. Avoid redundant aliases, repeated flags, mirrored derived state, and elaborate condition chains. Keep branch behavior and evaluation timing intact.
- Keep `build` focused on reactive inputs and UI composition. Extract lengthy listeners, event handlers, state-transition handling, and calculations into clearly named private methods below `build` in the same widget, or small local functions when build-local captures are needed. Call listener-registration helpers synchronously from `build`; keep hooks and reactive reads in their valid lifecycle. See [coding-style.md](references/coding-style.md#keep-build-focused-with-private-helpers).
- Apply **Extend Over Conditions (EOC)**: extend reusable behavior through explicit parameters and specialized composition instead of internal variant conditions. Let `XWidget` receive concrete text, values, widgets, and callbacks; let reusable `YWidget` configure `XWidget`, and reusable `ZWidget` configure `YWidget` when it shares that specialization. Apply EOC to screens, widgets, callback bodies, listeners, argument expressions, and text selection. Each specialized caller owns its fields/controllers and flow-specific actions/listeners. Remove conditions that can be expressed through these supplied values and behaviors; retain only necessary intrinsic runtime-state, validation, and lifecycle checks. Preserve `const` where possible. See [coding-style.md](references/coding-style.md#separate-variants-before-adding-conditions).
- Keep the latest explicit correction and its exceptions authoritative. For a broad redesign, maintain a requirement/caller ledger, inspect original references and manual changes, and verify all reachable states, including guests and loading/error/empty UI. Share visual/interaction owners without sharing unrelated state. See the [feedback precedence table](references/owner-feedback-cases.md#final-decisions-where-feedback-evolved).
- Apply **Design Linking** as a strict UI consistency rule. Before adding/changing UI, search existing components, representative callers, theme/token definitions, dialogs, and sheets. Reuse the matching component with its established defaults; supply genuine content/behavior differences through parameters. If no match exists, build from the established spacing, padding, radii, borders, colors, typography, sizes, icon treatment, and animation rules. Keep repeated styling owned by shared components/tokens, with explicit reusable variants for real design differences. Follow [Design Linking](references/design-tokens.md#design-linking) and [shared-components.md](references/shared-components.md).
- For themes and visual styling, read [design-tokens.md](references/design-tokens.md). Select a complete light/dark palette at the theme boundary, consume named text style tokens, and keep font and visual definitions in their owning classes/files. Design Linking applies across screens and overlays, including title placement/size, action layout, and transitions.
- Choose async return types and awaiting case by case. Preserve intentional self-contained `void async` and unawaited actions when their callers need no completion/result and the operation owns its errors. Do not impose a blanket `Future<void>` migration or add/remove `await` mechanically; trace required sequencing first. See the async contract guidance in the coding-style reference.
- For a new project or redesign, use the required bundled architecture. In existing code, preserve established equivalent owners; an accidentally flattened generated tree is not a precedent that overrides the user's requested structure. Do not copy another app's business rules or infer the owner's style from unattributed Flex code.
- Use [precision.md](references/precision.md) before finishing code changes. Read [debugging.md](references/debugging.md) for debugging/build failures and [review.md](references/review.md) for requested reviews.

Keep reuse work tied to the requested change and its affected callers. A local feature request does not require deduplicating the whole repository.

## Native and configuration boundary

Prefer a correct Flutter/Dart solution when it meets the actual requirement. Do not modify native or platform build settings merely because a native workaround is convenient.

Before changing native code, Android/iOS/macOS/Windows/Linux configuration, manifests, permissions, entitlements, signing, Gradle, Podfiles, deployment targets, native SDK settings, or CI settings controlling native builds:

1. Complete the relevant investigation and any independent Flutter work.
2. Explain the exact proposed files/settings, why the change is needed, the Flutter alternatives considered, and their practical limitations.
3. Obtain the user's approval for those changes before applying them, unless the user has already explicitly approved that same concrete change.

Also respect this boundary for generators or dependency operations that would rewrite native settings. Drafting a proposed patch separately is allowed; applying it to the project requires the same approval. Do not modify unrelated project/tooling settings or silence diagnostics to make validation pass. An impossible Flutter-only solution must be explained, not fabricated.

## Validate and report

For project creation/redesign and new features, perform the completion checks in [project-blueprint.md](references/project-blueprint.md#completion-checks) and [feature-blueprint.md](references/feature-blueprint.md#feature-completion-checks). Run the bundled read-only [structure checker](scripts/check_structure.py) for the affected source root or feature; its documented limits and usage are in [project-blueprint.md](references/project-blueprint.md#structure-checker). Fix structural violations in the code being created. Do not present an empty directory, a barrel, or an unused stub as an implemented layer. Report explicitly reused owners for a same-project redesign and genuinely unavailable integrations.

Run checks appropriate to the actual changed behavior and the project instructions. Format affected Dart files, run focused analysis and relevant existing tests, and add a meaningful regression check for changed logic when needed. Inspect the final diff and run `git diff --check` in a Git checkout. Avoid unnecessary tests or repeated broad checks for straightforward edits.

Report the behavior achieved, checks actually run, and material limits. Static analysis is not device, visual, performance, live API, or publication proof. If SDK/cache access or unavailable tools block validation, report that accurately. Never promise perfect performance or bug-free AI output; support confidence with the relevant evidence.

## Suggestions and approved feedback

Apply the owner's explicit instructions directly. If you think a different coding approach or architecture would be better, show a concrete example, benefit, and tradeoff. Keep it a suggestion until the owner agrees; silence is not agreement. Do not silently add unapproved philosophy changes to the plugin, project rules, or project code. Normal implementation choices within approved rules do not need repeated permission.

Apply approved feedback to the current task. When the user requests a lasting FLUTAI rule change, update the relevant bundled skill/reference instead of writing project-local FLUTAI memory. Keep project-specific business rules out of the general rules; an explicitly requested learning audit may retain them as clearly scoped examples in the bundled casebook. Only publish plugin changes when the user authorizes that update; verify the saved release separately from host behavior.
