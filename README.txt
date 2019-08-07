usage: fontswitch.py [-h] [--chunk <int>] [--out <path>]
                     [--fonts <font name> [<font name> ...]]
                     path

Convert a .txt file to .rtf and randomly apply a font on each character

positional arguments:
  path                  .txt file to convert

optional arguments:
  -h, --help            show this help message and exit
  --chunk <int>         Consecutive characters with the same font
  --out <path>          output file path
  --fonts <font name> [<font name> ...]
                        List of fonts to use. Default are: Arial, Arial Black,
                        Calibri, Cambria, Candara, Comic Sans MS, Constantia,
                        Corbel, Estrangelo Edessa, Franklin Gothic Medium,
                        Gabriola, Gautami, Georgia, Impact, Latha, Lucida Sans
                        Unicode, Modern, MS Sans Serif, MS Serif, MV Boli,
                        Myanmar Text, Nyala, Palatino Linotype, Plantagenet
                        Cherokee, Roman, Script, Segoe Print, Segoe Script,
                        Segoe UI, Small Fonts, Sylfaen, Tahoma, Times New
                        Roman, Trebuchet MS, Tunga, Verdana

Requirements:
- Python 3
- The fonts used by the script

Example:
basic:	
python fontswitch.py algo.txt

with output file: 
python fontswitch.py algo.txt --out algo_fonts.rtf

with custom fonts: 
python fontswitch.py algo.txt --fonts courier new, comic sans ms

with sequences of 10 characters using the same font:
python fontswitch.py algo.txt --chunk=10
