# Migration validation

## Build

Discover the actual workspace/project and scheme before running commands.

Typical commands (adapt to the repository):
```bash
xcodebuild -list -project App.xcodeproj
xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 16' build
xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 16' test
```

Do not assume a scheme, simulator name, or destination. Capture exit code and relevant log tail.

## Visual comparison

Compare screenshots with identical:
- simulator/device model and display scale;
- OS version and appearance;
- locale, Dynamic Type size and orientation;
- data fixture, selected tab, scroll position and modal state.

Review:
- outer safe area and navigation/tab bars;
- parent-child alignment and z-order;
- text baseline and font metrics;
- spacing, intrinsic size and compression;
- scrolling and content insets;
- keyboard avoidance;
- empty/loading/error states.

Pixel-diff tools are useful but not sufficient: animation, antialiasing, rendering differences and dynamic system chrome can create noise.

## Functional matrix

For every control/action record:
- initial state;
- action;
- expected state transition;
- side effects;
- navigation/presentation;
- error and cancellation path;
- automated or manual verification evidence.

## Completion states

Use only:
- `not-started`
- `analyzed`
- `implementing`
- `implemented-unverified`
- `verified`
- `blocked`

A successful compile alone does not mean verified.
