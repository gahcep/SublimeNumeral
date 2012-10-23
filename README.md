
# SublimeNumeral for Sublime Text 2

This plugin allows you to convert between main Numerical Systems: 

  * binary (`BIN`)
  * hexadecimal (`HEX`)
  * decimal (`DEC`)

To work with plugin (being able to convert a numbers) you can use the following:

 - Keyboard Shortcut: use `ctrl+shift+c` (for Windows)
 - Main Menu: go to `Tools -> Numeral -> Convert`
 - Context Menu: click on `Numeral -> Convert`
 - Command Pallete: type `Numeral: Convert`


Each pressing the convertion rotation is performed: `BIN -> DEC -> HEX -> BIN`.

Also there are a several options which influence on convertion behaviour. For details please see section **'Settings'**.

Plugin autorecognizes a selected number according to the following rules:

 - numbers `0x1500` or `1500h` or `15FCC` are recognized as hexadecimal (`HEX`);
 - numbers `0b101001` or `101001b` are recognized as binary (`BIN`)
 - numbers `59300` or `1030` or `200100` are recognized either as decimal (`DEC`) or hexadecimal (`HEX`) according to the option **opt\_prefer_numeral** (see below);
 - numbers `1000` or `101000` or `11111` are recognized either as decimal (`DEC`) or hexadecimal (`HEX`) according to the option **opt\_prefer_numeral** (see below);

> **Imporant**: If the option **opt\_prefer_numeral** is set to 'binary', the number 1 remains unmodified.

# Installation

The plugin isn't yet accessable via [Sublime Control Package](http://wbond.net/sublime_packages/package_control), thus can be installed via `git`:

### On Windows:

    - git clone https://github.com/gahcep/SublimeNumeral.git %APPDATA%/Sublime\ Text\ 2/Packages/SublimeNumeral

### On Linux:

    - git clone https://github.com/gahcep/SublimeNumeral.git  ~/.config/sublime-text-2/Packages/SublimeNumeral

### On MacOS:

    -  git clone https://github.com/gahcep/SublimeNumeral.git ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/SublimeNumeral

# Commands

`numeral_convert`: Cyclically convert between `BIN`, `DEC` and `HEX` numerical systems. Bound to `ctrl+shift+c`.


# Settings

All options are located in file `%APPDATA%/Sublime\ Text\ 2/Packages/SublimeNumeral/SublimeNumeral.sublime-settings`.

##### opt\_prefer_numeral

> *Default value*: **"binary"**

> Option is useful when trying to convert under ambiguous situation, e.g. 1000 - could be either `BIN` or `DEC` or `HEX`.  

> Available options are: **"decimal"**, **"hexadecimal"** and **"binary"**

##### opt_capitalize

> *Default value*: **false**

> Set if all letters included in a number will be capitalized.  

> E.g. `0x100fcc -> 0x100FCC`  

##### opt\_binary\_use_prefix

> *Default value*: **true**

> Set if prefix **'0b'** will be used for outputting a binary numbers.

##### opt\_hexadecimal\_use_prefix

> *Default value*: **true**

> Set if prefix **'0x'** will be used for outputting a hexadecimal numbers.

##### opt\_binary\_leading_enable

> *Default value*: **false**

> Fill a binary number with a zeros up to the nearest byte  

> E.g. if the option is **false** `0x25 -> 0b100101`  
> E.g. if the option is **true**  `0x25 -> 0b00100101`

##### opt\_binary\_leading_align

> *Default value*: **false**

> Fill a binary number with a zeros up to the nearest even-counted byte  

> E.g. if the option is 'false': `0x25    -> 0b100101`  
> E.g. if the option is 'true':  `0x25    -> 0b0000000000100101` (2^1)  
> E.g. if the option is 'true':  `0x2525  -> 0b0010010100100101` (2^1)  
> E.g. if the option is 'true':  `0x22525 -> 0b00000000000000100010010100100101` (2^2)

##### opt\_binary\_leading_count

> *Default value*: **0**

> The same as previous option but count of bytes, the number will be aligned to, 
can be fixed set. Cancels the option **opt\_binary\_leading_align** if not zero.  
> Settings number is a count of bits! And if the number exceeds that count, nothing happens.  

> Available range is **0** - disable, **1-256** bits
