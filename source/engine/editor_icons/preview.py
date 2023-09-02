from pathlib import Path


if __name__ == "__main__":
    dir = Path(__file__).parent
    with dir.joinpath("preview.htm").open("w") as html:
        html.writelines([
            '<!DOCTYPE html>\n',
            '<html lang="en">\n',
            '<head>\n',
            '<meta charset="UTF-8">\n',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n',
            '<meta http-equiv="X-UA-Compatible" content="ie=edge">\n',
            '<title>Icons Preview</title>\n',
            '<style>\n',
            '* { box-sizing: border-box; }\n',
            '#myInput { width: 100%; }\n',
            '#myUL { list-style-type: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; }\n',
            '</style>\n',
            '</head>\n',
            '<body bgcolor="#1d2229">\n',
            '<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Filter..">\n',
            '<ul id="myUL">\n'
        ])

        for image in dir.rglob("*.svg"):
            # https://realpython.com/python-xml-parser/#document-object-model-dom
            html.writelines([
                '<li>',
                '<img src="%s">\n' % image.relative_to(dir),
                '</li>'
            ])

        html.writelines([
            '</ul>\n',
            '<script>\n',
            'function myFunction() {\n',
            '    var input, filter, ul, li, a, i, txtValue;\n',
            '    input = document.getElementById("myInput");\n',
            '    filter = input.value.toUpperCase();\n',
            '    ul = document.getElementById("myUL");\n',
            '    li = ul.getElementsByTagName("li");\n',
            '    for (i = 0; i < li.length; i++) {\n',
            '        a = li[i].getElementsByTagName("a")[0];\n',
            '        txtValue = a.textContent || a.innerText;\n',
            '        if (txtValue.toUpperCase().indexOf(filter) > -1) {\n',
            '            li[i].style.display = "";\n',
            '        } else {\n',
            '            li[i].style.display = "none";\n',
            '        }\n',
            '    }\n',
            '}\n',
            '</script>\n',
            '</body>\n',
            '</html>\n'
        ])
