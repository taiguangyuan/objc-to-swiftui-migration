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

## State ownership

- `@State`: view-owned transient state.
- `@Binding`: parent-owned state passed to child.
- `@Observable` / `ObservableObject`: shared feature state with clear ownership.
- `@Environment`: app-wide dependencies or environment values, not a dumping ground.
- Avoid duplicating the same source of truth across view and model.

## Navigation

Prefer `NavigationStack` with typed route state for push navigation. Use `sheet(item:)`, `fullScreenCover(item:)`, `alert`, `confirmationDialog` for presentations. Model tab selection explicitly with `TabView(selection:)`.

Preserve deep links, back behavior, navigation bar appearance, status bar expectations, and state restoration where applicable.

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
