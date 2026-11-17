# XIB and Storyboard analysis

## XML model

Interface Builder documents are XML. Parse:
- root `<document>` metadata and deployment/plugin information;
- `<objects>` and nested `<subviews>`;
- `<view>`, `<viewController>`, `<tableView>`, `<collectionView>`, stack views, controls and custom classes;
- `<constraints>` and `<constraint>` attributes;
- `<connections>`: outlet, action, segue, relationship;
- `<resources>`: images, colors, fonts, named resources;
- `<rect>`, `<fontDescription>`, `<color>`, `<userDefinedRuntimeAttributes>`;
- safe-area and scroll-view layout guides;
- table/collection prototype cells and reuse identifiers.

## Hierarchy reconstruction

Use containment relationships, not XML line order. A view's parent is the object whose `subviews` collection contains it. View-controller relationships and segues are separate from view containment.

For each node record:
- object id and type;
- custom class and module;
- parent id and child ids;
- frame as design-time metadata only;
- hidden, alpha, interaction, clipping, background, tint, content mode;
- text, font, alignment, line count, capitalization and control state;
- constraints attached to the relevant item;
- connections in and out.

## Constraint interpretation

For each constraint preserve:
- first item / first attribute;
- relation;
- second item / second attribute;
- multiplier;
- constant;
- priority;
- identifier.

Translate intent, not raw numbers:
- edge-to-edge parent constraints → padding / frame alignment;
- centered constraints → alignment or frame alignment;
- equal dimensions → shared frame / aspect ratio / Grid;
- stack-like equal spacing → HStack / VStack / Grid;
- proportional constraints → aspectRatio or carefully justified GeometryReader;
- safe-area anchors → SwiftUI safe-area behavior / safeAreaInset / ignoresSafeArea;
- scroll content guides → ScrollView content, not fixed screen coordinates.

Auto Layout priorities do not map one-to-one to SwiftUI. Determine which constraints are required, which are fallback preferences, and how hugging/compression affects the result. Use layoutPriority only when it represents the same intended tradeoff.

## Storyboard-specific analysis

Record:
- initial view controller;
- scene identifiers and storyboard identifiers;
- navigation, tab, split and presentation relationships;
- segue identifiers, kinds, destinations and unwind actions;
- custom transitions and presentation styles;
- embedded controllers and container relationships;
- custom classes/modules;
- restoration identifiers and state restoration behavior.

Map to typed routes and SwiftUI presentation state. A segue is not automatically a `NavigationLink`: modal, unwind, custom and conditional transitions need separate treatment.

## Limitations

XML cannot reveal:
- views added or removed in code;
- constraints activated conditionally at runtime;
- custom drawing or layer manipulation;
- runtime intrinsic content size;
- data-dependent cell content;
- code-driven navigation;
- appearance proxy changes;
- dynamic type / localization behavior unless explicitly configured.

Cross-check with source, runtime screenshots and Xcode.
