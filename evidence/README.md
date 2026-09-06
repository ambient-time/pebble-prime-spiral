# Prime Spiral evidence

The production PBW passed installation and native checks on all six targets.
`validation.json` records its hash, rendering samples, free heap, and cadence.
Each target report includes the native logs and capture paths.

I inspected the hero, quarter-hour, evening, noon-rollover, and midnight-rollover
captures on every target. The field stays circular and the center time remains
clear. White and gray discs separate the bright bearings from steady primes on
color screens. Monochrome screens use dot size for emphasis. The 260-pixel
version uses larger center digits. Noon and midnight align all three bearings
at the top of the field and show the correct 24-hour readout.

The host suite checks every integer from 2 through 1800 against an independent
sieve, all 1799 golden-angle coordinates, and all three radial limits. Brightness
fixtures differ from the source Gaussian by at most 0.00339 on a 0–1 scale.
Readout tests cover every second in a day and fractional noon and midnight.
Address and undefined-behavior sanitizers pass.

Native checks confirm changing seconds, natural noon and midnight rollovers,
a tap burst, and the return to one redraw per second. Emulator timing and heap
samples describe these runs; physical-watch battery life, daylight readability,
and wrist-tap sensitivity remain untested.

`independent-build.json` records a clean rebuild from the released source ZIP.
It compares every application byte apart from the SDK header CRC, resource
timestamp, and validated GNU build ID, and checks resource packs for exact
agreement. This proof stays outside the ZIP whose hash it records.

Private mirror, CloudPebble build, dashboard upload, and public listing status
belong in the release record. These native checks establish none of those
publication steps.
