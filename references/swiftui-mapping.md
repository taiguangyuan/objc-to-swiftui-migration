# Native SwiftUI mapping rules

## Layout selection

- Vertical flow: `VStack`.
- Horizontal flow: `HStack`.
- Overlay / z-order: `ZStack`.
- Repeated two-dimensional content: `Grid` or `LazyVGrid` / `LazyHGrid`.
- Scrollable content: `ScrollView` with appropriate lazy stacks for large collections.
- System-style selectable lists: `List` when its behavior matches the original.
- Relative sizing: `aspectRatio`, `frame`, alignment guides; `GeometryReader` only when genuinely geometry-dependent.
- Insets around scroll content: `contentMargins` where available, otherwise explicit content padding.
- Safe area overlays/insets: `safeAreaInset`, `overlay`, and safe-area modifiers with care.
- **Never copy hard-coded Objective-C `frame` coordinates** into `.frame` / `.offset` / `.position`. Translate the encoded intent (alignment, proportions, spacing, scroll size, z-order) into native layout. See "Layout and gesture parity constraints" in `SKILL.md`.

## State ownership

- `@State`: view-owned transient state.
- `@Binding`: parent-owned state passed to child.
- `@Environment`: app-wide dependencies or environment values, not a dumping ground.
- Avoid duplicating the same source of truth across view and model.
- **iOS 17+:** prefer `@Observable` for shared feature state, `@Bindable` for bindings to observable models, and `@State` / `@Environment` instead of `StateObject` / `EnvironmentObject`.
- **iOS 16 and below:** use `ObservableObject` / `@Published` / `@StateObject` as required by the project's compatibility target.

## Reactive technology policy (native-first)

- Never add RxSwift / RxCocoa, ReactiveObjC / RAC, or any other third-party reactive framework by default. See the "Reactive technology constraint" section in `SKILL.md`.
- Use Swift Concurrency (`async`/`await`, `Task`, `.task`, structured cancellation) for asynchronous work.
- Do not use `PassthroughSubject` / `CurrentValueSubject` (or Rx `Subject` / `Relay`) to model simple state changes; use native state and explicit methods.
- Do not build a custom reactive command layer to imitate `RACCommand`; use a method plus explicit `isRunning` / `error` / result state.
- A third-party reactive library is allowed only when native tools cannot meet the requirement gracefully, with documented justification, user approval, and isolation behind a narrow interface.

Official references: [Managing model data in your app](https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app), [Observation framework](https://developer.apple.com/documentation/observation), [ObservableObject to Observable migration](https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro).

## Navigation

Prefer `NavigationStack` with typed route state for push navigation. Use `sheet(item:)`, `fullScreenCover(item:)`, `alert`, `confirmationDialog` for presentations. Model tab selection explicitly with `TabView(selection:)`.

Preserve deep links, back behavior, navigation bar appearance, status bar expectations, and state restoration where applicable.

## Gesture mapping and parity

Preserve the original operation logic exactly, including event phases, thresholds, cancellation, and interaction with other gestures.

- Build a gesture matrix in `migration/03-behavior-map.md` for every recognizer/control event: type, configuration, action per phase, thresholds, recognizer dependencies, hit-test behavior, and feedback.
- Map to native gestures: `.onTapGesture(count:)`, `.onLongPressGesture(minimumDuration:maximumDistance:perform:onPressingChanged:)`, `DragGesture(minimumDistance:)`, `MagnifyGesture`, `RotateGesture`, `SpatialTapGesture`, and `.gesture` / `.highPriorityGesture` / `.simultaneousGesture` with explicit `.onChanged` / `.onEnded` handling.
- Reproduce custom hit areas with `.contentShape(...)` and `allowsHitTesting`.
- For custom `UIGestureRecognizer` subclasses or raw touch handling that native gestures cannot express exactly, document the gap and use a narrowly scoped bridge only with user approval.
- Verify every path on device/simulator (multi-touch, rapid repeats, long-press cancellation, drag vs scroll, combined pinch/rotate, background/foreground) and record results in `migration/06-validation-report.md`.

## Rendering and visual fidelity

- Reuse original assets and fonts where licensing and project ownership permit.
- Match text metrics, line limits, truncation, baseline alignment, image scaling, clipping and corner radii.
- Do not use arbitrary offsets to imitate broken Auto Layout.
- Avoid hard-coded screen dimensions. Prefer parent-relative layout.
- Verify on the same device size, OS version, content and state.
- Account for Dynamic Type, localization, RTL and accessibility even if the legacy screen was weak in these areas; document intentional differences.

## UIKit bridge policy

A bridge is exceptional and must be:
1. narrowly scoped to one unsupported system capability;
2. isolated behind a SwiftUI-facing API;
3. documented with the missing native SwiftUI equivalent;
4. covered by tests;
5. tracked for future removal.

Forbidden: wrapping a whole UIViewController, XIB root view, storyboard scene, or legacy component tree as the migrated screen.
