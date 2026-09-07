# Prime Spiral

Prime numbers form a sunflower of light. Three invisible bearings sweep through
its points to mark the hour, minute, and second. Nearby primes brighten and
grow as each bearing passes.

The arrangement contains every integer from 2 through 1800, including all 278 primes. The golden angle determines each point’s position. The hour reaches 58% of the field radius,
the minute 80%, and the second the outer edge.

The face updates once a second. Tap your wrist for about six seconds of smoother
motion. Leaving the face stops that timer. It works without a phone connection,
account, settings, or network access.

## Watches

| Target | Display |
| --- | --- |
| basalt | 144 × 168, color |
| chalk | 180 × 180, color |
| diorite | 144 × 168, monochrome |
| emery | 200 × 228, color |
| flint | 144 × 168, monochrome |
| gabbro | 260 × 260, color |

## Build and verify

Use Pebble SDK 4.33.1 and a host C compiler. Normal builds use the checked-in
resources. Python 3 regenerates the source tables; Pillow redraws
the menu icon. The face has no external font or library dependencies.

```sh
make test
pebble build --sdk 4.33.1
```

Pebble names the output after the project directory. With this directory named
`prime-spiral`, the result is `build/prime-spiral.pbw`. The source ZIP contains the
project at its root and can build outside the Ambient Time checkout.

The native verification scripts use the Python environment containing
`pebble-tool`. Run each target before packaging:

```sh
python test/emulator.py basalt --fresh
python test/emulator.py chalk --fresh
python test/emulator.py diorite --fresh
python test/emulator.py emery --fresh
python test/emulator.py flint --fresh
python test/emulator.py gabbro --fresh
python test/package.py
python test/independent.py --pebble pebble
```

Each capture uses a fresh local emulator profile. The script verifies process
ownership before closing it. Checks cover installation, logs, changing seconds,
natural noon and midnight rollovers, a wrist tap, and the return to one update
per second. Packaging verifies every target's application and resource CRC,
metadata, and evidence hash. [Evidence notes](evidence/README.md) describe the
results and remaining physical-watch checks.

The release directory holds the versioned PBW, independent source ZIP, and
SHA-256 checksums.

## Source and adaptation

Luke Steuber created [Prime Spiral](https://datapoems.io/clocks/prime-spiral/)
and this Pebble port. The supplied HTML and screenshot are in `reference/`;
[provenance](reference/provenance.json) records their exact file hashes.

The port preserves the source's sieve, golden-angle coordinates, local time,
three radial limits, and Gaussian brightness response. Integer tables avoid
runtime trigonometry. Host tests compare the generated points with the source
formula and bound brightness error below 0.008 on a 0–1 scale.

Both screen shapes keep the circular field. Its radius is 43.5% of the shorter
screen dimension. Version 1.0.1 removes the digital center disc at Luke’s
request. The pinned source retains that readout; the watch now shows only
the prime field and its three time bearings.

Pebble's color displays use white and gray discs in place of blur and opacity.
Monochrome displays keep white prime dots and use their size to show emphasis.
Only a sparse subset of faint composite points appears on monochrome screens.
The browser's continuous motion becomes one update per second with the bounded
tap animation above. The port uses the supplied monochrome palette.

The package UUID is `3b314f24-6f15-4790-b841-d1767a0c8663`.
Keep it unchanged when updating this face.

Copyright 2026 Luke Steuber. [MIT License](LICENSE).
