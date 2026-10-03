<img src="docs/images/new-conscirpt-hero-image.png" alt="VERA20k hero image" width="100%">

# VERA20k

This fork uses VERA20k as the starting point for a faithful Rust reimplementation
of the Red Alert 2: Yuri's Revenge engine (`gamemd.exe`). Its first compatibility
baseline is vanilla Yuri's Revenge 1.001: original rules, legacy feel and smooth
independent presentation that preserves gameplay. Fidelity takes priority over
expanded limits; Ares/Phobos and other mod compatibility are later explicit scopes.
The [agentic masterplan](docs/plans/yr1001-masterplan.md) records progress and gaps.

You'll need your own copy of the game. EA sells it in *Command & Conquer The Ultimate
Collection*, on [Steam](https://store.steampowered.com/bundle/39394/) and on
[EA's site](https://www.ea.com/games/command-and-conquer/command-and-conquer-the-ultimate-collection/buy/pc).

<img src="docs/images/vera20k-screenshots.png" alt="VERA20k skirmish setup screen and in-game view" width="100%">

## Status

Pre-alpha. Local skirmish is playable on Windows against a placeholder AI.

- **Working:** retail and random maps, menus and sidebar, base building,
  [harvesting and refinery deposits](tools/spatial_oracle/refinery_dock.md), core combat,
  and save/load.
- **Partial:** aircraft attack runs, mind control, crates, death effects, and
  [bridges](tools/spatial_oracle/bridge_shadow_render.md).
- **Missing:** multiplayer, the original AI, campaign, most map triggers, movies,
  and several special weapons and superweapons.
- **Compatibility:** vanilla 1.001 is the first baseline; whole-game parity is open.
  The upstream 30-player/20,000-unit target is outside this baseline.

Ordinary Allied Power Plant destruction has bounded native comparisons through
[tank impact, effects and crew](tools/spatial_oracle/building_death_anims_joined.md),
[stock smudges](tools/spatial_oracle/building_death_anims_joined_stock_smudges.md)
and [cancelled held products](tools/spatial_oracle/building_death_anims_limbo_cancel.md).
Whole-object parity remains open.

Ordinary gameplay and audio/exit services now run from the event-loop service
owner independently of redraw requests. [Stage 2 progress](docs/plans/yr1001-stage2-runtime.md)
records the remaining interpolation, legacy effect cadence and worker handoff
work; synchronous GPU stalls still delay the single-thread runtime.

## Running it

You need Rust 1.88 or newer, a GPU with Vulkan, DirectX 12 or Metal, and the game installed.
It's been played on Windows, Linux and macOS, and CI builds and tests all three.

```sh
git clone https://github.com/ckbk456/vera20k.git
cd vera20k
cp config.toml.example config.toml   # then set ra2_dir to your game folder
cargo run --release --bin vera20k    # always --release: debug builds are too slow to play
```

The tests don't need the game: `cargo test -p vera20k --lib`. See
[CONTRIBUTING.md](CONTRIBUTING.md#set-up) for more setup details, including where VERA20k looks
for `config.toml`.

## How it's built

The original `gamemd.exe` is the reference. Newer gameplay code names the original function it
was ported from, and [native harnesses](tools/native_oracle.md) run the original code to check
the Rust results. Most of the code is written by AI coding agents that I direct, following the
rules in [AGENTS.md](AGENTS.md).

## Contributing

Help is welcome, and you don't need reverse-engineering experience. Playing VERA20k next to the
original and reporting differences helps a lot, and so does trying it on Linux or macOS. Start
with [CONTRIBUTING.md](CONTRIBUTING.md) or the
[good first issues](https://github.com/YuriPlanet/vera20k/labels/good%20first%20issue), or say
hi on [Discord](https://discord.gg/kmjRUn5m5F). For more depth there's the
[architecture overview](https://yuriplanet.github.io/vera20k/), the
[native oracle](tools/native_oracle.md) and the [research notes](docs/research/README.md).

## Credits and legal

Thanks to OpenRA, XCC Mixer, the ModEnc wiki, Project Perfect Mod, EA's GPL source release of
Command & Conquer and Red Alert, World-Altering Editor, Final Alert, YRpp, Ares, Phobos and
many others.

Licensed under the [GPLv3](LICENSE-GPL). This repository contains no game files. Command &
Conquer and Red Alert are trademarks of Electronic Arts Inc., and the screenshots show game art
owned by Electronic Arts. VERA20k is not affiliated with or endorsed by Electronic Arts.
