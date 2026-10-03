# API, models, state, and routing

Read this reference when changing data access, state ownership, pagination, forms, or navigation. Preserve the target's actual model types and public contracts; similar class names across the baseline apps do not imply interchangeable APIs.

## API and repositories

Keep common transport in `ApiService`: request construction, auth/language headers, timeout behavior, response parsing, and the existing token-refresh/error publication path. Feature repositories hold an `ApiService` dependency, call named `ApiEndpoints` with `ApiKeys`, map successful data into a typed result, and propagate the project's error object. Keep bodies/query serialization in request/model methods when they have an existing owner.

Repository methods stay short and explicit. Bayin commonly throws `response.exception`; Jawwab uses `response.requiredError`. Inspect the actual response model before choosing. Do not create per-screen HTTP clients, duplicate shared headers, use a success fallback for failure, or replace typed results with unstructured maps simply to reduce lines.

Use the current endpoint/key definitions and extend their owner for new shared entries. Keep distinct public business actions while extracting their repeated internal request/mapping work from the second use. Preserve backend-required differences in status handling, omitted fields, null fields, body encoding, file transfer, and result shape.

## Models and state

Models own `fromMap`, `toMap`, typed nested parsing, equality when meaningful, and reusable derived values. Use shared map/list helpers and constructor tear-offs where supported. Shared models belong in core only when their role spans features; feature-specific models remain under their feature.

Preserve nullable-copy semantics. Both apps have a `NullableValue` helper for cases where “keep the old value” and “set to null” must differ. Follow the current model's contract rather than replacing it with `newValue ?? oldValue`. Do not copy display/API business mappings into several screens.

Use the target's Riverpod annotations, provider families, and established `FutureState`/`AsyncValue` forms. Providers/notifiers coordinate actions, result state, refresh/invalidation, and affected callers. Repositories perform data access; widgets render and dispatch actions. Resolve stable dependencies once in the provider's appropriate build/initialization scope, and keep dynamic dependencies reactive.

`ref.watch` observes values needed for rendering/derived state; `ref.read` is appropriate for an action or a deliberate snapshot; `ref.listen` handles the existing side-effect flow. Preserve family arguments, scope ownership, keep-alive behavior, and disposal. A cached notifier or family instance is not automatically shared with every caller.

When the app uses `ApiRequestNotifier.guard` and app-level listeners for request loading/error/success UI, reuse that flow. Keep completion sequencing and callbacks intact. Jawwab's bank-account provider demonstrates separate add/update/delete methods delegating repeated coordination to `_bankAccountRequest`, with operation-specific success actions.

## Pagination, loading, and validation

Extend the existing pagination request/provider/list or grid instead of rebuilding fetch/page/filter/search/refresh handling per screen. Jawwab's feature providers configure a `PaginationRequest` with endpoint, list key, model parser, and optional hooks. Bayin uses its own pagination type/family and `getList` adapter. Use the target's actual version; do not blend their constructor parameters.

Render established loading, error/retry, empty, and populated states through shared builders. Preserve whether refresh keeps existing data visible, how retry invalidates the provider, page numbering, and selection return types. A single selection and a list of selections are different contracts; trace the overlay and caller before changing either.

Keep form validation in `FormValidator` and existing field/`ValidationForm` integration. Local validation must preserve API errors for the correct field and reset/update with locale changes as required. Read the current error shape; Bayin's map-based field errors and Jawwab's typed validation list are not interchangeable. Keep phone/numeric formatting separate from semantic validation.

## Routing and generated code

Read [routing.md](routing.md) for route files, provider ownership, paths, parameters, guards, shell composition, and deep-link handling. New routers belong under `core/routes/`; retain Bayin's existing router-provider location when extending that existing source tree. Do not collapse a new app's navigation into `core/router.dart` or screen-local route strings.

Edit source declarations, not `.g.dart` or generated localization implementations. Run the target's existing generator only when its source changes require it, with its installed dependency versions. Keep the generated diff scoped to the work; do not migrate Riverpod or routing APIs to match another project's snapshot.

## Source anchors

Inspected on 2026-10-03: both response models, request providers, pagination providers/models, and provider builders; Bayin `features/notifications/data/repositories/notifications_repo.dart`; Jawwab `features/wallet/data/repositories/wallet_repo.dart`, `providers/manage_bank_account_provider.dart`, `data/models/bank_account_model.dart`, `features/community/providers/posts_provider.dart`, and the generic pagination/selection APIs. API, routing, socket, and Firebase module entry points/signatures were inspected for ownership; this reference does not certify those implementations as defect-free.
