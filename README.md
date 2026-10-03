# FlutAI

Flutter/Dart coding workflows for creating, extending, debugging and reviewing apps with layered features, reusable components and named design tokens.

Version: 0.4.3. A coding environment with project and tool access is required.

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

Maintainer workflow: prepare and verify changes, present the version and change summary for owner approval, then publish only after approval. Create a tag and Release for approved release publication.

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
