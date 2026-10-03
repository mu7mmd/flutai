#!/usr/bin/env python3
"""Read-only FLUTAI placement checks; no Flutter or third-party dependency."""

import argparse
import json
from pathlib import Path
import re


FOUNDATION = {
    "entry point": ("main.dart",),
    "app composition": ("app.dart",),
    "configuration": ("core/config/app_config.dart", "config/app_config.dart"),
    "colors": ("core/constants/app_colors.dart",),
    "sizes": ("core/constants/app_sizes.dart",),
    "font identifiers": ("core/constants/app_fonts.dart",),
    "typography": ("core/styles/text_styles.dart", "core/constants/text_styles.dart"),
    "theme": (
        "core/themes/app_theme.dart", "core/theme/app_theme.dart",
        "core/styles/app_theme.dart",
    ),
    "route definitions": ("core/routes/app_routes.dart",),
    "router provider": (
        "core/routes/go_router_provider.dart",
        "core/controllers/providers/go_router_provider.dart",
    ),
    "context access": ("core/extensions/context_extension.dart",),
}
WIDGET = re.compile(
    r"\bclass\s+([A-Za-z]\w*)(?:\s*<[^{};]+>)?\s+extends\s+"
    r"([A-Za-z_]\w*)"
)
WIDGET_BASES = {
    "StatelessWidget", "StatefulWidget", "ConsumerWidget", "ConsumerStatefulWidget",
    "HookWidget", "HookConsumerWidget", "Text", "AppBar", "Scaffold",
    "ElevatedButton", "OutlinedButton", "TextButton", "IconButton",
}


def dart_files(folder):
    return sorted(
        p for p in folder.rglob("*.dart")
        if p.is_file() and not p.name.endswith((".g.dart", ".freezed.dart"))
        and "generated" not in p.relative_to(folder).parts
    ) if folder.is_dir() else []


def without_comments(text):
    # Declaration checks are intentionally warnings, not a substitute for a Dart AST.
    return re.sub(r"/\*[\s\S]*?\*/|//[^\n]*", "", text)


def has_implementation(path):
    code = without_comments(path.read_text(encoding="utf-8"))
    code = re.sub(r"(?m)^\s*(?:library|import|export|part)\b[\s\S]*?;", "", code)
    return bool(code.strip())


def implemented_files(folder):
    return [path for path in dart_files(folder) if has_implementation(path)]


def audit(project, source, shared=(), feature=None, requires_data=False,
          repository_owner=None):
    roots = [source, *shared]
    errors, warnings, owners = [], [], {}

    def finding(target, rule, path, message):
        target.append({"rule": rule, "path": str(path.relative_to(project)),
                       "message": message})

    def choose(relative_paths):
        return next((root / rel for root in roots for rel in relative_paths
                     if (root / rel).is_file() and has_implementation(root / rel)), None)

    if feature is None:
        for capability, paths in FOUNDATION.items():
            owner = choose(paths)
            if owner:
                owners[capability] = str(owner.relative_to(project))
            else:
                finding(errors, "missing-foundation", source,
                        f"Missing {capability}; expected an implemented owner at: {', '.join(paths)}")
        for area in ("widgets", "helpers", "services", "utils", "providers"):
            candidates = [root / "core" / area for root in roots]
            if area == "providers":
                candidates += [root / "core/controllers" for root in roots]
            if not any(implemented_files(p) for p in candidates):
                finding(warnings, "capability-review", source / "core",
                        f"No {area} implementation found; verify actual needs or document a reused owner.")
        if not (project / "l10n.yaml").is_file():
            finding(warnings, "localization-review", project,
                    "Verify localization generation and catalogs; l10n.yaml was not found.")

    selected = source / "features" / feature if feature else source
    files = dart_files(selected)
    if feature and not files:
        finding(errors, "empty-feature", selected, "No handwritten Dart feature implementation found.")
    if not feature and not dart_files(source / "features"):
        finding(errors, "missing-features", source, "No feature implementation found under features/.")

    for path in files:
        parts = path.relative_to(source).parts
        text = path.read_text(encoding="utf-8")
        code = without_comments(text)
        if len(parts) >= 3 and parts[0] == "features":
            tail = parts[2:]
            if path.name.endswith("_screen.dart") and tail[:2] != ("presentation", "screens"):
                finding(errors, "screen-placement", path,
                        "Move the screen to features/<feature>/presentation/screens/.")
            if path.name.endswith(("_repo.dart", "_repository.dart")) and tail[:2] != ("data", "repositories"):
                finding(errors, "repository-placement", path,
                        "Move the repository to features/<feature>/data/repositories/.")
            if path.name.endswith(("_model.dart", "_request.dart")) and tail[:2] != ("data", "models"):
                finding(warnings, "model-placement-review", path,
                        "Feature data/request types normally belong in data/models; verify this type's responsibility.")
            if "widgets" in tail and tail[:2] != ("presentation", "widgets"):
                finding(errors, "widget-placement", path,
                        "Feature widgets belong in presentation/widgets, sibling to presentation/screens.")
        if parts[:1] == ("core",) and len(parts) == 2 and path.name in {
            "theme.dart", "router.dart", "styles.dart", "services.dart", "helpers.dart",
            "widgets.dart", "components.dart", "constants.dart", "config.dart",
        } and has_implementation(path):
            finding(errors, "flat-core-implementation", path,
                    "Place implementations in the owning core directory; a root barrel may only export.")
        if path.name in {"widgets.dart", "screens.dart"} and has_implementation(path):
            finding(errors, "implementation-in-barrel", path,
                    "Use separate implementation files. This conventional barrel name is reserved for exports.")
        widgets = [name for name, base in WIDGET.findall(code)
                   if base in WIDGET_BASES or name.endswith(("Screen", "Widget"))]
        if len(widgets) > 1:
            finding(warnings, "public-components-review", path,
                    "Review separate files for public components: " + ", ".join(widgets))
        if parts[:2] == ("core", "widgets") and len(parts) == 3 and widgets:
            finding(warnings, "widget-family-review", path,
                    "New shared UI belongs in its widgets/<family>/ folder; preserve existing owners for focused edits.")

    if requires_data:
        feature_roots = [root / "features" / feature for root in roots]
        groups = {
            "models": [p / "data/models" for p in feature_roots],
            "repositories": [p / "data/repositories" for p in feature_roots],
            "state": [p / area for p in feature_roots
                      for area in ("providers", "controllers")],
        }
        for capability, candidates in groups.items():
            found = next((p for p in candidates if implemented_files(p)), None)
            if capability == "repositories" and repository_owner:
                found = repository_owner
            if found:
                owners[f"feature {capability}"] = str(found.relative_to(project))
            else:
                finding(errors, "missing-feature-layer", selected,
                        f"Data-backed feature has no implemented {capability} owner in the selected/shared roots.")
    return {"source_root": str(source.relative_to(project)), "feature": feature,
            "handwritten_files_checked": len(files), "owners": owners,
            "errors": errors, "warnings": warnings,
            "limits": "Placement and file-presence checks only. Review wiring, variants, imports, runtime behavior and capability coverage separately."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--source-root", default="lib")
    parser.add_argument("--shared-root", action="append", default=[])
    parser.add_argument("--feature")
    parser.add_argument("--requires-data", action="store_true")
    parser.add_argument("--repository-owner", help="Verified shared repository path relative to the project, e.g. lib/core/pagination/data/repositories/pagination_repo.dart")
    args = parser.parse_args()
    project = args.project.resolve()
    if not project.is_dir():
        parser.error("project must be an existing directory")

    def directory(value):
        path = (project / value).resolve()
        if not path.is_relative_to(project) or not path.is_dir():
            parser.error(f"source roots must be existing directories inside the project: {value}")
        return path

    source = directory(args.source_root)
    shared = [directory(p) for p in args.shared_root]
    if args.feature and not re.fullmatch(r"[a-z][a-z0-9_]*", args.feature):
        parser.error("feature must be one snake_case directory name")
    if args.requires_data and not args.feature:
        parser.error("--requires-data needs --feature")
    repository_owner = None
    if args.repository_owner:
        repository_owner = (project / args.repository_owner).resolve()
        if not args.requires_data or not repository_owner.is_relative_to(project):
            parser.error("--repository-owner requires --requires-data and a path inside the project")
        if not repository_owner.is_file() or repository_owner.suffix != ".dart" or not has_implementation(repository_owner):
            parser.error("--repository-owner must identify a nonempty Dart implementation file")
    try:
        result = audit(project, source, shared, args.feature,
                       args.requires_data, repository_owner)
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
