# FlutAI

Flutter/Dart coding workflows for creating, extending, debugging and reviewing apps with layered features, reusable components and named design tokens.

Version: 0.5.0. A coding environment with project and tool access is required.

## Install with Codex CLI

```bash
codex plugin marketplace add https://github.com/mu7mmd/flutai.git --ref main
codex plugin add flutai@flutai-marketplace
```

Start a new Codex session after installation.

## Import into a managed ChatGPT workspace

A workspace admin can import the marketplace:

1. Open **Admin > Plugins > Add > Import marketplace**.
2. Set **Source** to `https://github.com/mu7mmd/flutai`.
3. Leave **Path** empty.
4. Set **Branch, tag, or commit** to `main`, or leave it empty to follow the default branch.
5. Import, review the result, then configure the plugin's availability and installation policy.

New marketplaces enable daily automatic sync. Use **Admin > Plugins > Marketplaces > Sync now** to request an earlier refresh. Sync uses the importing admin's GitHub connection.

This import flow applies to managed workspaces with admin access. It does not establish automatic GitHub sync for personal ChatGPT accounts. Publishing on GitHub does not publish FlutAI in the public ChatGPT Plugins Directory.

## Update a Codex installation

```bash
codex plugin marketplace upgrade flutai-marketplace
codex plugin list --json
```

The upgrade command refreshes the Git marketplace. Verify the installed plugin version and use the client's reinstall/update flow if it still shows the previous version, then start a new session. Each independent client must refresh its source; this repository cannot force every device to update.

Follow `main` for ongoing updates. A fixed commit stays pinned to that revision.

## Versions and release notifications

Keep `plugin.json` and `.codex-plugin/plugin.json` at the same semantic version. Record changes in [CHANGELOG.md](CHANGELOG.md).

Publishing a GitHub Release is separate from committing a version change and separate from marketplace sync. Users can choose **Watch > Custom > Releases** on GitHub for release notifications. These are GitHub notifications, not guaranteed in-app update prompts.

Maintainer workflow: prepare and verify changes, then present the version and change summary for owner approval. The owner's initial approval to upload or publish a prepared FlutAI update covers the source commit/push, its matching version tag, and publication of the GitHub Release; do not request a second release confirmation for the same approved update. Honor an explicit request to save source only, keep a draft, or defer publication. Verify the published commit, tag, and Release separately from marketplace/client refresh.

## Owner rules in 0.5.0

The bundled workflow now requires exact reference matching, shared component/state boundaries, scroll-owned insets, unified sheet presentation, keyboard/audio/session lifecycle checks, and safe source-tree promotion. Read the [decision and coverage casebook](skills/flutter-coding/references/owner-feedback-cases.md) for the reviewed corrections and their final precedence. App-specific examples are explicitly scoped rather than imposed on unrelated projects. [Validation notes](documentation/owner-rule-validation.md) distinguish package checks from runtime behavior.

## Repository layout

- `plugin.json`: portable Agent Plugins manifest.
- `.codex-plugin/plugin.json`: Codex compatibility manifest.
- `.agents/plugins/marketplace.json`: marketplace catalog; its local source path refers to the repository root.
- `skills/flutter-coding/`: existing workflow, reference guides and structure checker.
- `assets/`: branding.

## Source and branding

No license has been selected. FlutAI is an independent project; the included Flutter logo does not imply endorsement.

## Official documentation

- [Codex plugin commands](https://learn.chatgpt.com/docs/developer-commands)
- [ChatGPT workspace import and sync](https://learn.chatgpt.com/docs/enterprise/plugin-management)
- [Plugin packaging](https://developers.openai.com/plugins/build/plugins)
