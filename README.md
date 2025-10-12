# Animal Language

[![Documentation Status](https://readthedocs.org/projects/animal/badge/?version=latest)](https://animal.readthedocs.io/en/latest/?badge=latest)
[![Go Report Card](https://goreportcard.com/badge/github.com/animal-lang/animal)](https://goreportcard.com/report/github.com/animal-lang/animal)
[![Release](https://img.shields.io/github/v/release/animal-lang/animal)](https://github.com/animal-lang/animal/releases)

Animal is a programming language where operators, control flow and data structures are expressed with animal calls and behaviors with fully‑feathered (im sorry i had to) language with functions, nests (classes), lists, file I/O and symbolic error handling.

## Quick Start

```bash
go install github.com/animal-lang/animal/cmd/animal@latest
# Start the REPL
animal --repl
# Run a program
animal path/to/script.anml
```

A tiny sample:

```animal
roar "Welcome to the animal kingdom!"

age -> 5
weight -> 10
total -> age meow weight

roar "Total:", total
```

## Highlights

- **Intuitive syntax** – `meow`, `woof`, `moo`, `leap`, `pounce`, `howl` and more!

- **Modern tooling** – Interactive REPL, execution timers (`animal --time`) and debugging output (`animal --debug`).

- **Deep standard library** – File helpers (`drop`, `fetch`, `sniff_file`), symbolic error handling (`try`/`catch` blocks), list methods (`sniff`, `snarl`, `prowl`, `wag`, …) and math utilities.

- **Nests and functions** – Build reusable abstractions with `nest` definitions and first‑class `howl` functions.

- **Runs everywhere** – Native Go binary plus a WebAssembly build so Animal code can run in the browser.

### Editor Support

- **VS Code** – Install the [Animal Language extension](https://marketplace.visualstudio.com/items?itemName=klus3kk.animal) for syntax highlighting, icon theming and language configuration.

- **Online playground** – Try the language directly in your browser at the [Animal Playground](https://animal-lang.github.io/animal-playground).

## Documentation

Full guides, language reference and standard library docs live at [animal.readthedocs.io](https://animal.readthedocs.io/).

## Install from Source

```bash
git clone https://github.com/animal-lang/animal.git
cd animal
go build -o animal ./cmd/animal
go test ./...
```

## Example for lists, file I/O and symbolic errors

```animal
log_path -> "log.txt"

pack -> ["lynx", "otter", "stoat"]
pack.sniff("mink")

drop(log_path, "Pack members: " purr pack)

*[
  howl find_index(name) {
      idx -> pack.howl(name)
      idx growl -1 sniffback
  }

  roar "Mink index:", find_index("mink")
]* *(
  roar "Something went wrong:", _error
)* *{
  "Missing pack member"
}*
```

## License

Animal is released under the [MIT License](LICENSE).
