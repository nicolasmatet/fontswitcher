from random import randrange
import argparse
import os
from typing import Tuple, List

_list_fonts = ['Arial, Arial Black, Calibri, Cambria, Candara, Comic Sans MS, Constantia, Corbel,'
               ' Estrangelo Edessa, Franklin Gothic Medium, Gabriola, Gautami, Georgia, Impact, Latha, '
               'Lucida Sans Unicode, Modern, MS Sans Serif, MS Serif, MV Boli, Myanmar Text, Nyala, '
               'Palatino Linotype, Plantagenet Cherokee, Roman, Script, Segoe Print, Segoe Script, '
               'Segoe UI, Small Fonts, Sylfaen, Tahoma, Times New Roman, Trebuchet MS, Tunga, Verdana']

line_break = "\pard\plain \s0\ql\widctlpar\hyphpar0\ltrpar\cf0\kerning1\dbch\\af13\langfe1081\dbch\\af16\\afs24\\alang1033\loch\\f3\\fs24\lang1033\n"
new_paragraph = "\n\par" + line_break


def get_fonts_lines(list_string_fonts):
    return """{\\fonttbl{\\f0\\froman\\fprq2\\fcharset0 Times New Roman;}\n""" + \
           "\n".join(["{{\\f{:d}\\fnil\\fprq2\\fcharset0 {:};}}"
                     .format(idx + 1, font) for idx, font in enumerate(list_string_fonts)]) + "}\n\n"


def transform_text(input_path, output_path, list_fonts, chunk):
    number_of_fonts = len(list_fonts) + 1
    with open(input_path, "r") as input_file:
        with open(output_path, "w+") as output:
            output.truncate(0)
            output.write("{\\rtf1\\ansi\deff3\\adeflang1025\n")
            output.write(get_fonts_lines(list_fonts))
            output.write('\n' + line_break)
            content = iter(input_file.read())
            eof = False
            while not eof:
                font_idx = randrange(1, number_of_fonts)
                buffer, paragraphs, eof = get_buffer(content, chunk)
                if not paragraphs:
                    output.write("{" + "\\f{:d}\n{:}".format(font_idx, buffer) + "}")
                else:
                    start = 0
                    for paragraph in paragraphs:
                        if start < paragraph:
                            output.write("{" + "\\f{:d}\n{:}".format(font_idx, buffer[start:paragraph]) + "}")
                        output.write(new_paragraph)
                        start = paragraph
                    if start < len(buffer):
                        output.write("{" + "\\f{:d}\n{:}".format(font_idx, buffer[start:]) + "}")
            output.write("\par }")


def get_buffer(content_iterator, chunk) -> Tuple[str, List[int], bool]:
    buffer = ''
    paragraphs = []
    eof = False
    try:
        car = next(content_iterator)
    except StopIteration:
        return buffer, paragraphs, True
    if car == "\n":
        paragraphs.append(0)
        chunk += 1
    else:
        buffer += car
    if car == " ":
        buffer, paragraphs, eof = __get_next_bufer(content_iterator, chunk, buffer, paragraphs)
    elif chunk > 1 and not eof:
        buffer, paragraphs, eof = __get_next_bufer(content_iterator, chunk - 1, buffer, paragraphs)
    return buffer, paragraphs, eof


def __get_next_bufer(content_iterator, chunk, current_buffer, current_paragraphs):
    next_buffer, next_paragraphs, eof = get_buffer(content_iterator, chunk)
    if next_paragraphs:
        for i in next_paragraphs:
            current_paragraphs.append(len(current_buffer) + i)
    return current_buffer + next_buffer, current_paragraphs, eof


parser = argparse.ArgumentParser(description='Convert a .txt file to .rtf and randomly apply a font on each character')
parser.add_argument('path', type=str, help='.txt file to convert')
parser.add_argument('--chunk', metavar='<int>', type=int, help='Consecutive characters with the same font ', default=1)

parser.add_argument('--out', metavar='<path>', type=str, help='output file path', default=None)
parser.add_argument('--fonts', metavar='<font name>', type=str, nargs='+',
                    help='List of fonts to use. Default are:\n' + _list_fonts[0], default=_list_fonts)

args = parser.parse_args()
font_names = " ".join(args.fonts).split(",")
output_file = os.path.splitext(args.out)[0] + '.rtf' if args.out else os.path.splitext(args.path)[0] + '_out.rtf'
chunk_size = int(args.chunk) if args.chunk > 1 else 1
input_file = args.path
if not os.path.isfile(input_file):
    raise FileNotFoundError
transform_text(args.path, output_file, font_names, chunk_size)
print("output file:", output_file, ">> done !")
