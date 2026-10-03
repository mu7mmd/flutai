# Changelog

## 0.4.3

- Require direct Flutter and external-package imports, and relative imports for project files within the same source tree.
- Separate Dart SDK, Flutter SDK, dependencies, and project imports with one blank line between nonempty groups.
- Order relative imports from farthest to nearest, with current-directory files last.
- Use purposeful `show`/`hide` selections while preserving required APIs, extensions, prefixes, generated directives, and package boundaries.
- Apply the import rules to new/touched code and import reviews without unrelated cleanup or silent tooling changes.

## 0.4.2

- Set Mohammad Alamoudi as the developer and add the owner's LinkedIn profile to author metadata.
- Add the GitHub project URL as the plugin website and portable homepage/repository metadata.
- Rename the plugin display name to FlutAI in both manifests and the marketplace label.
- Update current documentation and starter prompt branding.
- Keep the technical identifiers flutai and flutai-marketplace unchanged.

## 0.4.1

- Add the GitHub marketplace catalog for FLUTAI.
- Add a Codex compatibility manifest with the same identity, version, skills and presentation as the portable manifest.
- Replace placeholder repository URLs with mu7mmd/flutai.
- Document workspace import, daily sync, manual Codex refresh and release notifications.
- Preserve the existing Flutter workflow and assets.

## 0.4.0

- Initial exported FLUTAI plugin source.
