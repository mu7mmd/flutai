# Flutter code review

Read the actual diff and the relevant callers, state owners, and models. Prioritize concrete regressions in behavior, data handling, authorization, lifecycle, layout, and public contracts. Use the focused checks in [precision.md](precision.md). Check repeated logic and access against the owner's DRY and simplicity rules. Account for project rules before suggesting another pattern.

Check changed imports against [coding-style.md](coding-style.md#dart-imports): resolved relative project paths, separated SDK/dependency/project groups, farthest-to-nearest local ordering, and complete `show`/`hide` selections without namespace conflicts.

For each actionable finding, identify the file and location, the triggering condition, its impact, and the supporting code path. Separate demonstrated issues from unresolved questions. Do not fill a review with speculative warnings or style preferences already covered by the repository's conventions.

Report findings in severity order and summarize relevant validation gaps. Keep optional design suggestions separate from defects and wait for agreement before adopting a different coding philosophy. If no actionable issue is found, say so and state the review's limits. A request to review does not automatically request implementation of the findings.
