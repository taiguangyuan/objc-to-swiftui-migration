# Objective-C source analysis

## Analysis checklist

For each `.h` / `.m` pair, record:
- class name, superclass, protocols, categories;
- public API vs private implementation;
- properties, ownership, nullability, generics, enums and constants;
- initializers and dependency injection;
- all callers and construction sites;
- delegate/data-source contracts;
- notifications, KVO, target-action, selectors and blocks;
- gestures: recognizer types and configurations, control events, delegate rules, dependencies and cancellation paths;
- hard-coded `frame` / `bounds` / `center` assignments, `layoutSubviews` math, and manual coordinate calculations;
- RAC signals, commands, schedulers, disposal and completion semantics;
- network requests, request parameters, response parsing and error mapping;
- persistence, caching, analytics and feature flags;
- thread assumptions and main-thread UI updates.

## Conversion principles

- Preserve semantics, not syntax. Translate Objective-C nullable behavior explicitly using Swift optionals.
- Do not silently coerce malformed strings to numeric zero. Preserve validation and error states.
- Convert completion handlers to `async throws` only when cancellation, ordering and error semantics remain equivalent.
- Convert delegates to closures or observable state when that simplifies ownership; retain protocols for multi-method or long-lived contracts.
- Convert notifications/KVO to explicit state or event streams where practical.
- Replace mutable shared state with value types and controlled mutation where safe.
- Avoid force unwraps unless the invariant is proven and documented.
- Preserve serialization keys and backend contracts explicitly with `CodingKeys` or custom decoding.
- Audit retain cycles, timer invalidation, observer removal and request cancellation.
- Translate hard-coded frames into native SwiftUI layout intent; never copy coordinates (see `SKILL.md`).
- Preserve gesture operation logic exactly, including event phases, thresholds, failure/cancellation and recognizer competition; verify each path before completion.

## Lifecycle mapping

| UIKit / Objective-C | SwiftUI candidate | Caution |
|---|---|---|
| `viewDidLoad` | initializer / `.task` / state setup | `.task` can run again when identity changes |
| `viewWillAppear` | `.onAppear` | can fire repeatedly |
| `viewDidDisappear` | `.onDisappear` | not equivalent to deallocation |
| layout callbacks | layout containers / `GeometryReader` | avoid geometry when constraints express intent |
| hard-coded frame / `layoutSubviews` | layout containers + modifiers | translate intent; never copy coordinates |
| target-action | `Button` / control action | preserve enabled and accessibility states |
| gesture recognizer | native SwiftUI gesture modifiers | preserve phases, thresholds, cancellation and competition |
| custom `hitTest` / raw touches | `contentShape` / `allowsHitTesting` | preserve hit area and fallthrough behavior |
| delegate callbacks | closures, bindings, observable model, protocol | choose based on lifecycle and multiplicity |
| KVO | observable model / publisher | avoid duplicate observation |
| NotificationCenter | app-level event or observable state | scope and delivery semantics matter |
| timer | `Task` loop / TimelineView | cancellation and background behavior |
| RACCommand | async action + explicit state | preserve executing, error and completion behavior |

Never apply this table mechanically. Trace the actual runtime semantics first.
