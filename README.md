# FLUTAI

Flutter/Dart coding workflows for creating, extending, debugging and reviewing apps with layered features, reusable components and named design tokens.

Version: 0.4.0. This repository contains the exported plugin, bundled skills, reference guides and structure checker. A coding environment with project and tool access is required.

## Install using Codex CLI

Replace OWNER/REPO with this repository address:

```bash
codex plugin marketplace add https://github.com/OWNER/REPO.git
codex plugin add flutai@flutai-marketplace
```

Start a new Codex session after installation.

## Install in a managed ChatGPT workspace

A workspace admin can open Admin > Plugins > Add > Import marketplace and enter this repository URL. Leave Path empty. Use the default branch to receive future updates. Review the imported plugin and configure access.

GitHub publication does not publish this plugin to the public ChatGPT Plugins Directory. Browser-only personal accounts do not use the workspace admin import flow.

## Refresh the Git marketplace

```bash
codex plugin marketplace upgrade flutai-marketplace
```

This refreshes the marketplace source. Check the installed version and restart the client/session as appropriate. Managed workspace marketplaces support daily sync and Sync now.

## Publish this repository

Create an empty public GitHub repository, extract this archive, and upload all its contents, including `.agents` and `.codex-plugin`. Commit the extracted files rather than only the ZIP. The marketplace manifest must remain at `.agents/plugins/marketplace.json`.

## Source and branding

The original plugin files and skills are preserved. No new license has been selected for this export. Choose an appropriate license before granting reuse/modification rights. FLUTAI is an independent project; the included Flutter logo does not imply endorsement.

## Official documentation

- https://learn.chatgpt.com/docs/developer-commands
- https://learn.chatgpt.com/docs/enterprise/plugin-management
- https://developers.openai.com/plugins/build/plugins
