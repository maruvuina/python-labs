# -*- coding: utf-8 -*-
import xml.sax.saxutils
import sys

def main():
    maxwidth, format = process_options()
    if maxwidth is not None:
        print_start()
        count = 0
        while True:
            try:
                line = input()
                if count == 0:
                    color = "lightgreen"
                elif count % 2:
                    color = "white"
                else:
                    color = "lightyellow"
                print_line(line, color, maxwidth, format)
                count += 1
            except EOFError:
                break
        print_end()

def process_options():
    maxwidth = 100
    format = ".0f"
    maxwidth_arg = "maxwidth="
    format_arg = "format="
    for arg in sys.argv[1:]:
        if arg in ["-h", "--help"]:
            print("""\
usage:
csv2html.py [maxwidth=int] [format=str] < infile.csv > outfile.html
maxwidth - необязательное целое число. Если задано, определяет
максимальное число символов для строковых полей. В противном случае
используется значение по умолчанию {0}.

format - формат вывода чисел. Если не задан, по умолчанию используется
формат "{1}".""".format(maxwidth, format))
            return None, None
        elif arg.startswith(maxwidth_arg):
            try:
                maxwidth = int(arg[len(maxwidth_arg):])
            except ValueError:
                pass
        elif arg.startswith(format_arg):
            format = arg[len(format_arg):]
    return maxwidth, format

def print_start():
    print("<table border='1'>")

def print_end():
    print("</table>")

def print_line(line, color, maxwidth, format):
    print("<tr bgcolor='{0}'>".format(color))
    numberFormat = "<td align='right'>{{0:{0}}}</td>".format(format)
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print(numberFormat.format(x))
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                field = xml.sax.saxutils.escape(field)
                if len(field) <= maxwidth:
                    field = xml.sax.saxutils.escape(field)
                else:
                    field = "{0} ...".format(xml.sax.saxutils.escape(field[:maxwidth]))
                print("<td>{0}</td>".format(field))
    print("</tr>")

def extract_fields(line):
    fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None:  # начало строки в кавычках
                quote = c
            elif quote == c:  # конец строки в кавычках
                quote = None
            else:
                field += c
                # другая кавычка внутри строки в кавычках
                continue
        if quote is None and c == ",":  # end of a field
            fields.append(field)
            field = ""
        else:
            field += c
            # добавить символ в поле
    if field:
        fields.append(field)  # добавить последнее поле в список
    return fields


main()
