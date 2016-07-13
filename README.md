# [HexBinDec][home]
[![The MIT License](https://img.shields.io/badge/license-MIT-orange.svg?style=flat-square)](http://opensource.org/licenses/MIT)

This package provides ability to inplace change the base of numbers in [SublimeText 3 Editor][1].

## Usage
1. Move the cursor over a number or select one or more numbers.
2. Press one of the following key combinations to convert the numbers.

	- <kbd>Ctrl+shift+b, ctrl+shift+d</kbd> binary to decimal
	- <kbd>Ctrl+shift+b, ctrl+shift+h</kbd> binary to hexadecimal
	- <kbd>Ctrl+shift+d, ctrl+shift+b</kbd> binary to decimal
	- <kbd>Ctrl+shift+d, ctrl+shift+h</kbd> binary to hexadecimal
	- <kbd>Ctrl+shift+h, ctrl+shift+b</kbd> hexadecimal to binary
	- <kbd>Ctrl+shift+h, ctrl+shift+d</kbd> hexadecimal to decimal

The commands are available in
- command pallet under `Convert Number: ...`
- main menu -> edit -> Convert Numbers
- context menu -> Convert Numbers

## Setup
You can setup patterns to identify binary, decimal and hexadecimal numbers for each syntax just by adding the following settings to the syntax specific settings file `<scope>.sublime-settings`.

```javascript
	// ...

	// Define the format of binary numbers for the Hex-Bin-System plugin
	// Binaries look like 'B101110'
	"convert_src_bin": "'B([01]+)'",
	"convert_dst_bin": "'B{0:b}'",

	// Define the format of hexadecimal numbers for the Hex-Bin-System plugin
	// Hexadecimals look like 'H1AF23'
	"convert_src_hex": "'H(\\H+)'",
	"convert_dst_hex": "'H{0:X}'",

	// Define the format of exponential numbers for the Hex-Bin-System plugin
	// The pattern must match the base as group 1 and exponent as group 2.
	// Exponential numbers look like 3.14EX-4
	"convert_src_exp": "\\b([1-9]\\.\\d+)EX([-+]?\\d+)\\b",
	"convert_dst_exp": "EX",

	// ...
```

## Inspired by

[Hex-Bin-System][2] by ALLZ

[home]:		<https://github.com/deathaxe/sublime-hexbindec>
[1]:			<http://www.sublimetext.com>
[2]:			<https://github.com/ALLZ/hex-bin_system>