# Project documentation and source comments

Read when implementing or changing code, requirements, configuration, settings, or version constraints. Apply the owner's selective-comment policy and keep developer documentation with the implementation.

## Documentation ownership

Use `documentation/` at the Flutter project/repository root, alongside its source and package configuration. This holds developer explanations of the actual project, not copies of FLUTAI rules or plugin memory. Create it when needed and update relevant files in the same task as the implementation. Keep source comments focused on local reasoning as described in [coding-style.md](coding-style.md#selective-source-comments).

Document all newly implemented or changed code at the appropriate component, module, feature, or flow level: what it does, its requirements, how its parts connect, and any setup or assumptions a developer needs. Cover every affected responsibility without repeating every line or generating a separate page for each symbol. Keep a focused change's documentation scoped to its implementation and affected contracts; do not rewrite unrelated documentation.

Inspect existing documentation before adding files. Update its existing owner instead of duplicating explanations. For new explanations, use readable Markdown files with meaningful topic names unless the user or project requires another format. Split independent topics and substantial features into separate files; combine closely related small explanations. Keep a small index when several files need navigation. Create only files with actual content, not an empty standard set.

| Example file | Explain when relevant |
| --- | --- |
| `documentation/code_doc.md` | Architecture, component ownership, important data/state/UI flows, interfaces, and implementation rationale. Split large feature explanations into named feature files or a feature subfolder. |
| `documentation/requirements_doc.md` | Implemented requirements, prerequisites, supported scenarios, expected behavior, and actual limitations. |
| `documentation/config_doc.md` | Configuration owners/paths, environments, required keys, value meanings/defaults, generation, and setup commands. |
| `documentation/settings_doc.md` | Runtime/developer settings, accepted values, defaults, persistence, and effects of changing them. |
| `documentation/versions_doc.md` | Actual app, SDK, language, and relevant dependency versions/constraints; compatibility requirements and reasons for important constraints or workarounds. |
| `documentation/design_doc.md` | Established design tokens, shared component/overlay owners, defaults, supported EOC variants, and usage examples that preserve Design Linking. |

These names illustrate topics, not required files for every project. Reuse equivalent names already present within `documentation/`.

## Useful content and accuracy

Explain the actual implementation with real owning source paths and concise examples when helpful. Describe important inputs/outputs, validation, side effects, sequencing, and configuration steps at the level the feature requires. For shared widgets and EOC specializations, explain the base parameters, specialized callers, and where flow-specific callbacks/listeners/controllers belong. State a decision's reason when code alone would not reveal it.

Read requirements, configuration, settings, and versions from the actual source and package files. Distinguish SDK constraints from installed/resolved versions. Do not invent compatibility guarantees, undocumented setup steps, or successful integration/testing claims. Mark genuinely unknown or pending requirements clearly. Use placeholder values for credentials in examples.

When behavior, parameters, setup, settings, or versions change, update their existing explanations and any affected cross-links. Keep essential brief code rationale near the code and its longer explanation here; neither replaces the other.

## Completion checks

- Confirm relevant new/changed implementation, requirements, configuration, settings, and version constraints have current explanations in `documentation/`.
- Verify source paths, links, parameter/default descriptions, commands, and version statements against the implementation.
- Confirm comments explain non-obvious behavior or reasons, without annotating obvious code or repeating documentation blocks.
- Report which documentation was created/updated and any information that could not be verified; do not treat writing documentation as runtime validation.
