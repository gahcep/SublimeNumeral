import re
import sublime, sublime_plugin

OPTIONSFILE = sublime.load_settings("SublimeNumeral.sublime-settings")

class NumeralConvertCommand(sublime_plugin.TextCommand):

	BITS_CEILING = 256

	hex_base = "([0-9a-f]{1,})"
	# match 10FF30
	match_hex_pure = "^" + hex_base + "$"
	# match 0x10FF30 or 10FF30h
	match_hex = ("^0x" + hex_base + "$", 
		         "^"   + hex_base + "h$")

	# match only those numbers which have a alpha [a-f] in it
	match_hex_alpha = "^[0-9]*[a-fA-F]+[0-9]*$"
 
	# match 34100
	match_dec_pure = "^([0-9]{1,})$"

	bin_base = "([0,1]{1,})"
	# match 0100100
	match_bin_pure = "^" + bin_base + "$"
	# match 0b0100100 or 0100100b
	match_bin = ("^0b" + bin_base + "$",
	 			 "^"   + bin_base + "b$")

	# match if there is a anything except [0-9] and [a-f,h,x]
	match_nan = "[^0-9a-fhx]{1,}"

	def bin2dec(self, bin):
		return int(bin, 2)

	def bin2hex(self, bin):
		pass

	def dec2bin(self, dec):
		pass

	def dec2hex(self, dec):

		# Get hexadecimal specific options
		opt_capitalize             = OPTIONSFILE.get('opt_capitalize',             False)
		opt_hexadecimal_use_prefix = OPTIONSFILE.get('opt_hexadecimal_use_prefix', True);

		# Convert the number
		number = hex(int(dec))[2:]
		
		if opt_capitalize:
			rep_text = number.upper()

		if opt_hexadecimal_use_prefix:
			rep_text = "0x" + rep_text

		return rep_text

	def hex2bin(self, hex):
		
		# Get binary specific options
		opt_binary_use_prefix     = OPTIONSFILE.get('opt_binary_use_prefix',     True)
		opt_binary_leading_enable = OPTIONSFILE.get('opt_binary_leading_enable', False);
		opt_binary_leading_align  = OPTIONSFILE.get('opt_binary_leading_align',  False);
		opt_binary_leading_count  = OPTIONSFILE.get('opt_binary_leading_count',  0);

		# Convert the number
		number = bin(int(hex, 16))[2:]

		if opt_binary_leading_count > 0 and opt_binary_leading_count <= BITS_CEILING:
			rep_text = number.zfill(opt_binary_leading_count)

		elif opt_binary_leading_align:
			rep_text = number.zfill(self.zfillsize(number, True))

		elif opt_binary_leading_enable:
			rep_text = number.zfill(self.zfillsize(number, False))

		if opt_binary_use_prefix: rep_text = "0b" + rep_text
		
		return rep_text

	def hex2dec(self, hex):
		pass


	def zfillsize(self, rep_text, even_align = False):
		''' Return number of placeholder (PH) which
		    is rewuired to be filled with zeroes.
		    'even_align' equals 'false' means to retrieve
		    not aligned count of PH.
		    'even_align' equals 'true' means to retrieve
		    aligned count of PH
		'''

		# Get the length
		rep_len = len(rep_text)
		
		# Get the count of leading zeroes needed to be add
		loopi = 8
		difference = 0
		
		# Loop until we find a min number of bits equals 
		# to two's pow, but more than a given number bits 
		# count (difference should be more or equal to zero) 
		# OR we exceed the ceiling (256)
		while(loopi <= BITS_CEILING):
			difference = loopi - rep_len
			if difference >= 0: break

			loopi = loopi * 2 if even_align else loopi + 8

		return rep_len + difference
		

	def recognize(self, selection):
		''' Trying to auto-recognize a numerical system.
			Priority in case of ambiguity: BIN > DEC > HEX
		'''
		if not selection:
			return "NAN", None

		# In case of ambiguity we need this option
		opt_prefer_numeral = OPTIONSFILE.get('opt_prefer_numeral', 'decimal')

		# Check if we have a NAN (Not A Number)
		if re.search(self.match_nan, selection, re.IGNORECASE):
			return "NAN", None
		
		# Is it BIN w/ pre/postfix? e.g. 0b100100 | 100100b
		for pattern in self.match_bin:
			match = re.findall(pattern, selection, re.IGNORECASE)
			if match:
				return "BIN", match[0]
		
		# Is it HEX w/ pre/postfix? e.g. 0x100 | 100h
		for pattern in self.match_hex:
			match = re.findall(pattern, selection, re.IGNORECASE)
			if match:
				return "HEX", match[0]
		
		# Is it HEX w/ alphabetical in it [A,B,C,D,E,F]? e.g. 10FF
		match = re.findall(self.match_hex_alpha, selection, re.IGNORECASE)
		if match: 
			return "HEX", match[0]
		
		# We now have an ambiguity: the given number has only
		# digits from 0 to 9 and thus could be 
		# -- a HEX w/o alphabetical in it (A,B,C,D,E,F)
		# -- a BIN w/o a digits greater than 2 (2,3,4,5,6,7,8,9)
		# -- a true DEC number
		
		if (opt_prefer_numeral == "binary"):
			# Is it BIN w/o pre/postfix? 
			match = re.findall(self.match_bin_pure, selection)
			if match:
				return "BIN", match[0]
			else: # No, so give another try
				opt_prefer_numeral = "decimal"

		if (opt_prefer_numeral == "decimal"):
			match = re.findall(self.match_dec_pure, selection)
			if match:
				return "DEC", match[0]
		else:
			match = re.findall(self.match_hex_pure, selection)
			if match:
				return "HEX", match[0]

		# If the number was smth like: 0b231x00
		return "NA", None

	def run(self, edit):

		# Get only first selection range
		sel = self.view.sel()
		
		sel_text = self.view.substr(sel[0])
		rep_text = ""

		# Recognize a numeral system
		numsys = self.recognize(sel_text)

		if numsys[0] == "NA" or numsys[0] == "NAN":
			sublime.status_message("Selection can't be converted")
			rep_text = None

		elif numsys[0] == "BIN":
			rep_text = self.bin2dec(numsys[1])
		elif numsys[0] == "DEC":
			rep_text = self.dec2hex(numsys[1])
		elif numsys[0] == "HEX":
			rep_text = self.hex2bin(numsys[1])

		else:
			rep_text = None

		if rep_text: self.view.replace(edit, sel[0], str(rep_text))
