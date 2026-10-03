# Flutter debugging

Start with the reported symptom, reproduction steps or log, expected behavior, and the smallest relevant source path. Request only missing information necessary to distinguish plausible causes. Trace a concrete execution path before editing.

For state problems, inspect provider identity and family arguments, scope placement, listeners, disposal, and active consumers. Distinct family instances do not automatically serialize work across arguments. For auth and permissions, distinguish stored session state from the validated user's actual role and backend access.

For rendering problems, examine layout constraints, safe regions, scroll ownership, text direction, and the existing asset's geometry. Preserve the intended shape and interaction area. Report whether the result was inspected on a device, emulator, browser, or only in source.

For Android/iOS or CI failures, identify the failing task and source revision. Compare relevant configuration and dependencies with a known successful run when available. Separate dependency-resolution errors, compiler diagnostics, resource shrinking, memory exhaustion, and signing problems. Investigate Flutter alternatives first. Follow the main skill's native approval boundary before editing native/build settings, including CI controls for native builds; explain exact changes, reasons, and alternatives first. Preserve unrelated working settings.

Use documentation matching the installed package/SDK version when behavior is uncertain. Do not infer runtime behavior solely from native configuration or a successful build. Choose a regression check that would fail before the fix when practical, then rerun the relevant check after the fix.

Keep secrets out of logs, source, and plugin instructions. Use the project's established secret injection mechanism. Creating or fixing code does not by itself authorize store releases or changes to production services.
