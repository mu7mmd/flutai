# Precision before finishing

Use only the checks relevant to the changed code. Keep this review focused; it is not a reason to build new infrastructure or expand the feature.

## Trace the behavior

Translate the request into its actual cases before implementation: inputs, conditions, visible/actionable states, outputs, and side effects. Follow each affected case from caller through state/repository/model to the UI. Preserve exact parameter types, request keys, result cardinality, units, null behavior, ordering, and role checks. Verify names against real definitions; do not invent an API or localization key.

For a changed condition, walk through true, false, and relevant boundary cases. For collection updates, ensure the selected item changes and unrelated items remain. Look specifically for shadowed parameters, comparing a value with itself, mismatched IDs, reversed conditions, or a branch that can never execute.

For example, a removal operation on `[2, 4, 6]` targeting `4` must leave `[2, 6]`; removing a missing value must leave the collection unchanged. Testing only an empty input would miss a broken comparison that clears every item.

After extracting reusable logic, inspect every changed caller: same outputs, same side effects, same required timing, and one source for the shared behavior. Check that a generic helper has not erased a distinct domain action or weakened a type.

## Check state and UI only where affected

Confirm the loading, success, error, and empty states that the feature can actually reach. Do not swallow errors or replace a failed operation with fake success. Preserve local and server validation. Check the exact provider instance and owner before changing reads, watches, invalidation, shared state, or disposal.

For asynchronous code, inspect whether completion, cancellation, disposal, or repeated taps affect this operation. Keep existing safeguards that protect a real lifecycle; do not add locks, queues, retries, or cancellation layers without a concrete need.

For layout changes, preserve interaction bounds, text direction, localization, and responsive constraints. Use actual rendering/device checks where available and needed. Source inspection alone cannot establish visual correctness.

## Keep performance proportional

Avoid repeated expensive work, unnecessary requests, state updates, and obvious redundant rebuilds in affected paths. Prefer existing lazy list/pagination and localized state builders when they fit the requirement. Do not introduce caching, background isolates, debouncing, or architectural layers without a demonstrated cost or explicit requirement. State the evidence before claiming a performance improvement.

## Validate the right thing

Choose analysis and tests that cover the changed contract. A regression test should demonstrate the error or expected behavior rather than mirror implementation text. Test a helper through the relevant calling contract when that is where the bug lives. Keep format and diff checks scoped; do not rewrite unrelated files.

Distinguish what passed from what was unavailable. Never substitute a successful static check for a device, backend, native lifecycle, or release check. Do not claim “perfect” or “fully verified” without evidence covering the stated behavior.
