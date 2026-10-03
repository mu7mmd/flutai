# Routing, navigation, and application composition

Read when creating a project/feature or changing navigation. The reference apps use GoRouter owned through Riverpod, named route constants/builders, context/GoRouter extensions, and `MaterialApp.router`. Preserve existing compatible contracts and the installed API versions.

## Files and owners

For a new app, use:

```text
core/routes/
  app_routes.dart
  go_router_provider.dart
  route_not_found_screen.dart
  screens_export.dart            # optional, export-only
  <integration>_provider.dart     # only if deep-link integration is used
core/extensions/
  go_router_extensions.dart      # shared parameter decoding when useful
  context_extension.dart         # common navigation/overlay conveniences
```

`AppRoutes` owns literal paths, route segments and parameterized destination builders. `PathParameters`, `QueryParameters`, or `ExtraParameters` own repeated argument keys when used. Keep the actual destination names meaningful. Do not scatter `'/feature/$id'` strings or repeat query construction in screen callbacks.

`go_router_provider.dart` owns router creation, navigator key, route hierarchy, builders, redirects, error handling, and the lifecycle needed by the app. A focused shared transition helper can live there or in its own routing file when reused. Routing imports screen classes; it does not implement the screens or a catalog of shell widgets.

Jawwab follows this location directly. Bayin's existing GoRouter provider/screens-export files live under `core/controllers/providers`, with path constants in `core/routes`. Extend that existing organization when working in Bayin's original tree; a new standalone app uses the complete `core/routes` group instead of inheriting split locations by accident.

## Path and argument contracts

- Distinguish absolute top-level paths from relative nested segments. A path template such as `items/:id` and a builder for a concrete destination have different responsibilities. Encode user-supplied path/query values rather than concatenating unsafe text.
- Keep required identifiers in path/query values when the destination must survive a direct link or app restart. `extra` is an in-memory optimization or additional typed argument; do not require it for every independently addressable details screen.
- A details route may use a correctly typed passed model immediately and otherwise load by ID. Validate missing/malformed arguments and show the existing not-found/error state; do not blindly cast every `extra` or force-unwrapping every ID.
- Keep typed overlay/navigation results intact: `push<T>`/`pop<T>` and single item versus list selection are distinct APIs. Follow the caller's actual result needs.
- Preserve `go`, `push`, replacement and pop behavior intentionally. Do not replace one with another merely to shorten a handler; it changes stack/back semantics.
- Use the target's route/state extensions for repeated decoding. Keep feature-specific navigation helpers near that feature or its established owner; generic context extensions should not become a dump of unrelated feature business logic in a new app.

## Auth, shells, and provider lifecycle

Select signed-in/out or other route variants at one clear boundary. Share the relevant redirect/guard logic instead of repeating auth checks inside every screen's build. The initial route alone is not an authorization guard: check direct entry to protected paths, sign-out, and auth changes. Authentication policy is app-specific; do not copy another app's subscription/role/acceptance rules.

Keep one intended router/navigation stack and root navigator key per app surface. Make authentication refresh reactive through the chosen router/provider mechanism without recreating the router unintentionally on unrelated state changes. Dispose resources according to the provider lifecycle and the installed GoRouter API.

Use `ShellRoute`/the existing shell mechanism for a shared frame. The shell gets a complete routed child, and separate navigation widgets render tabs/drawer/rail. Prefer a shell with slots or specialized wrappers over a giant shell driven by booleans for every screen. Stateful tabs need their intended stack/state retention; do not reset a tab's state on every navigation casually.

When a route overrides a provider family, scope the dependent providers that must observe it consistently. Preserve family arguments, keys and container ownership; unrelated family instances are not shared global state. Do not compose a legacy feature under a new shell while dropping its required inherited/provider scope.

Transitions belong to routing/shared presentation helpers, not duplicated in every callback. Distinct named helpers can share a single transition implementation receiving a builder, following Bayin's transition composition pattern. Preserve keys and returned route result types.

## App startup and deep links

`main.dart` initializes Flutter and only the SDK/storage dependencies the app uses, in the order their consumers require. Pass initialized dependencies into the correct provider container/overrides. `app.dart` binds the router, locale, delegates, supported locales, complete theme choices and app-level listeners/gates.

For a same-project alternate entry point, reuse the existing bootstrap/container when intended; route selection is separate from initializing integrations. In a standalone copy, move/configure the required startup owners so it no longer imports the original package.

Deep-link services parse incoming data in their owner and hand off to the router when initialization and the relevant navigator/provider scope are ready. Test cold/warm navigation according to the changed behavior. Do not fix readiness by copying unexplained delays, creating a second global router, or importing an old navigator key beside a new one without an explicit shared design.

App-level request/response listeners belong in app composition or a focused listener owner under that same scope. They should not be registered separately by each screen or recreated by nested app shells. Keep business reactions and error feedback sequencing intact.

## Verification

For the affected routes, check direct entry, required/missing arguments, logged-in/out behavior, unknown routes, back/pop results, shell selection, and the intended state lifetime. Test route changes with the target's existing test setup; no need for a live backend when provider overrides can exercise the route contract. Disclose separately when platform deep-link delivery is untested.

Source anchors: Jawwab `core/routes/{app_routes,go_router_provider,screens_export,route_not_found_screen}.dart`, `core/extensions/go_router_extensions.dart`, `main.dart`, `app.dart`; Bayin `core/routes/app_routes.dart`, `core/controllers/providers/go_router_provider.dart`, preferences and app composition. Follow current user preferences over incidental nested branches or unsafe casts in those examples.
