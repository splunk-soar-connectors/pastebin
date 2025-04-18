# File: pastebin_consts.py
#
# Copyright (c) 2019-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#

# Test Connectivity endpoints
PASTEBIN_CONNECTION_MESSAGE = "Querying endpoint to verify the credentials provided"
PASTEBIN_CONNECTIVITY_FAIL_MESSAGE = "Test connectivity failed"
PASTEBIN_CONNECTIVITY_PASS_MESSAGE = "Test connectivity passed"
DEFAULT_TIMEOUT_SECONDS = 30
# Creating paste
PASTEBIN_CREATING_PASTE_URL = "https://pastebin.com/api/api_post.php"
PASTEBIN_CREATING_PASTE_PAYLOAD = (
    "api_dev_key={}&api_paste_code={}&api_option={}"
    "&api_user_key={}&api_paste_name={}&api_paste_format={}&api_paste_private={}&api_paste_expire_date={}"
)
# Get user key
GET_USER_KEY_URL = "https://pastebin.com/api/api_login.php"
PASTEBIN_GET_USER_KEY_PAYLOAD = "api_dev_key={}&api_user_name={}&api_user_password={}"
# Get paste data
GET_PASTE_DATA_URL = "https://pastebin.com/raw/{}"
# Error messages
PASTEBIN_ERROR_MESSAGE = "Unknown error occurred. Please check the asset configuration and|or action parameters"
PASTEBIN_ERROR_CODE_MESSAGE = "Error code unavailable"
PASTEBIN_ERROR_MESSAGE_FORMAT = "Error code: {}. Error message: {}"
# Dictionaries
PASTEBIN_FORMAT_DICT = {
    "4CS": "4cs",
    "6502 ACME Cross Assembler": "6502acme",
    "6502 Kick Assembler": "6502kickass",
    "6502 TASM/64TASS": "6502tasm",
    "ABAP": "abap",
    "ActionScript": "actionscript",
    "ActionScript 3": "actionscript3",
    "Ada": "ada",
    "AIMMS": "aimms",
    "ALGOL 68": "algol68",
    "Apache Log": "apache",
    "AppleScript": "applescript",
    "APT Sources": "apt_sources",
    "Arduino": "arduino",
    "ARM": "arm",
    "ASM (NASM)": "asm",
    "ASP": "asp",
    "Asymptote": "asymptote",
    "autoconf": "autoconf",
    "Autohotkey": "autohotkey",
    "AutoIt": "autoit",
    "Avisynth": "avisynth",
    "Awk": "awk",
    "BASCOM AVR": "bascomavr",
    "Bash": "bash",
    "Basic4GL": "basic4gl",
    "Batch": "dos",
    "BibTeX": "bibtex",
    "Blitz3D": "b3d",
    "Blitz Basic": "blitzbasic",
    "BlitzMax": "bmx",
    "BNF": "bnf",
    "BOO": "boo",
    "BrainFuck": "bf",
    "C": "c",
    "C#": "csharp",
    "C (WinAPI)": "c_winapi",
    "C++": "cpp",
    "C++ (WinAPI)": "cpp-winapi",
    "C++ (with Qt extensions)": "cpp-qt",
    "C: Loadrunner": "c_loadrunner",
    "CAD DCL": "caddcl",
    "CAD Lisp": "cadlisp",
    "Ceylon": "ceylon",
    "CFDG": "cfdg",
    "C for Macs": "c_mac",
    "ChaiScript": "chaiscript",
    "Chapel": "chapel",
    "C Intermediate Language": "cil",
    "Clojure": "clojure",
    "Clone C": "klonec",
    "Clone C++": "klonecpp",
    "CMake": "cmake",
    "COBOL": "cobol",
    "CoffeeScript": "coffeescript",
    "ColdFusion": "cfm",
    "CSS": "css",
    "Cuesheet": "cuesheet",
    "D": "d",
    "Dart": "dart",
    "DCL": "dcl",
    "DCPU-16": "dcpu16",
    "DCS": "dcs",
    "Delphi": "delphi",
    "Delphi Prism (Oxygene)": "oxygene",
    "Diff": "diff",
    "DIV": "div",
    "DOT": "dot",
    "E": "e",
    "Easytrieve": "ezt",
    "ECMAScript": "ecmascript",
    "Eiffel": "eiffel",
    "Email": "email",
    "EPC": "epc",
    "Erlang": "erlang",
    "Euphoria": "euphoria",
    "F#": "fsharp",
    "Falcon": "falcon",
    "Filemaker": "filemaker",
    "FO Language": "fo",
    "Formula One": "f1",
    "Fortran": "fortran",
    "FreeBasic": "freebasic",
    "FreeSWITCH": "freeswitch",
    "GAMBAS": "gambas",
    "Game Maker": "gml",
    "GDB": "gdb",
    "GDScript": "gdscript",
    "Genero": "genero",
    "Genie": "genie",
    "GetText": "gettext",
    "Go": "go",
    "Godot GLSL": "godot-glsl",
    "Groovy": "groovy",
    "GwBasic": "gwbasic",
    "Haskell": "haskell",
    "Haxe": "haxe",
    "HicEst": "hicest",
    "HQ9 Plus": "hq9plus",
    "HTML": "html4strict",
    "HTML 5": "html5",
    "Icon": "icon",
    "IDL": "idl",
    "INI file": "ini",
    "Inno Script": "inno",
    "INTERCAL": "intercal",
    "IO": "io",
    "ISPF Panel Definition": "ispfpanel",
    "J": "j",
    "Java": "java",
    "Java 5": "java5",
    "JavaScript": "javascript",
    "JCL": "jcl",
    "jQuery": "jquery",
    "JSON": "json",
    "Julia": "julia",
    "KiXtart": "kixtart",
    "Kotlin": "kotlin",
    "KSP (Kontakt Script)": "ksp",
    "Latex": "latex",
    "LDIF": "ldif",
    "Liberty BASIC": "lb",
    "Linden Scripting": "lsl2",
    "Lisp": "lisp",
    "LLVM": "llvm",
    "Loco Basic": "locobasic",
    "Logtalk": "logtalk",
    "LOL Code": "lolcode",
    "Lotus Formulas": "lotusformulas",
    "Lotus Script": "lotusscript",
    "LScript": "lscript",
    "Lua": "lua",
    "M68000 Assembler": "m68k",
    "MagikSF": "magiksf",
    "Make": "make",
    "MapBasic": "mapbasic",
    "Markdown": "markdown",
    "MatLab": "matlab",
    "Mercury": "mercury",
    "MetaPost": "metapost",
    "mIRC": "mirc",
    "MIX Assembler": "mmix",
    "MK-61/52": "mk-61",
    "Modula 2": "modula2",
    "Modula 3": "modula3",
    "Motorola 68000 HiSoft Dev": "68000devpac",
    "MPASM": "mpasm",
    "MXML": "mxml",
    "MySQL": "mysql",
    "Nagios": "nagios",
    "NetRexx": "netrexx",
    "newLISP": "newlisp",
    "Nginx": "nginx",
    "Nim": "nim",
    "NullSoft Installer": "nsis",
    "Oberon 2": "oberon2",
    "Objeck Programming Langua": "objeck",
    "Objective C": "objc",
    "OCaml": "ocaml",
    "OCaml Brief": "ocaml-brief",
    "Octave": "octave",
    "OpenBSD PACKET FILTER": "pf",
    "OpenGL Shading": "glsl",
    "Open Object Rexx": "oorexx",
    "Openoffice BASIC": "oobas",
    "Oracle 8": "oracle8",
    "Oracle 11": "oracle11",
    "Oz": "oz",
    "ParaSail": "parasail",
    "PARI/GP": "parigp",
    "Pascal": "pascal",
    "Pawn": "pawn",
    "PCRE": "pcre",
    "Per": "per",
    "Perl": "perl",
    "Perl 6": "perl6",
    "Phix": "phix",
    "PHP": "php",
    "PHP Brief": "php-brief",
    "Pic 16": "pic16",
    "Pike": "pike",
    "Pixel Bender": "pixelbender",
    "PL/I": "pli",
    "PL/SQL": "plsql",
    "PostgreSQL": "postgresql",
    "PostScript": "postscript",
    "POV-Ray": "povray",
    "PowerBuilder": "powerbuilder",
    "PowerShell": "powershell",
    "ProFTPd": "proftpd",
    "Progress": "progress",
    "Prolog": "prolog",
    "Properties": "properties",
    "ProvideX": "providex",
    "Puppet": "puppet",
    "PureBasic": "purebasic",
    "PyCon": "pycon",
    "Python": "python",
    "Python for S60": "pys60",
    "q/kdb+": "q",
    "QBasic": "qbasic",
    "QML": "qml",
    "R": "rsplus",
    "Racket": "racket",
    "Rails": "rails",
    "RBScript": "rbs",
    "REBOL": "rebol",
    "REG": "reg",
    "Rexx": "rexx",
    "Robots": "robots",
    "Roff Manpage": "roff",
    "RPM Spec": "rpmspec",
    "Ruby": "ruby",
    "Ruby Gnuplot": "gnuplot",
    "Rust": "rust",
    "SAS": "sas",
    "Scala": "scala",
    "Scheme": "scheme",
    "Scilab": "scilab",
    "SCL": "scl",
    "SdlBasic": "sdlbasic",
    "Smalltalk": "smalltalk",
    "Smarty": "smarty",
    "SPARK": "spark",
    "SPARQL": "sparql",
    "SQF": "sqf",
    "SQL": "sql",
    "SSH Config": "sshconfig",
    "StandardML": "standardml",
    "StoneScript": "stonescript",
    "SuperCollider": "sclang",
    "Swift": "swift",
    "SystemVerilog": "systemverilog",
    "T-SQL": "tsql",
    "TCL": "tcl",
    "Tera Term": "teraterm",
    "TeXgraph": "texgraph",
    "thinBasic": "thinbasic",
    "TypeScript": "typescript",
    "TypoScript": "typoscript",
    "Unicon": "unicon",
    "UnrealScript": "uscript",
    "UPC": "upc",
    "Urbi": "urbi",
    "Vala": "vala",
    "VB.NET": "vbnet",
    "VBScript": "vbscript",
    "Vedit": "vedit",
    "VeriLog": "verilog",
    "VHDL": "vhdl",
    "VIM": "vim",
    "VisualBasic": "vb",
    "VisualFoxPro": "visualfoxpro",
    "Visual Pro Log": "visualprolog",
    "WhiteSpace": "whitespace",
    "WHOIS": "whois",
    "Winbatch": "winbatch",
    "XBasic": "xbasic",
    "XML": "xml",
    "Xojo": "xojo",
    "Xorg Config": "xorg_conf",
    "XPP": "xpp",
    "YAML": "yaml",
    "YARA": "yara",
    "Z80 Assembler": "z80",
    "ZXBasic": "zxbasic",
}
PASTEBIN_PRIVATE_DICT = {"Public": 0, "Unlisted": 1, "Private": 2}
PASTEBIN_EXPIRE_DATE_DICT = {
    "Never": "N",
    "10 Minutes": "10M",
    "1 Hour": "1H",
    "1 Day": "1D",
    "1 Week": "1W",
    "2 Weeks": "2W",
    "1 Month": "1M",
    "6 Months": "6M",
    "1 Year": "1Y",
}
