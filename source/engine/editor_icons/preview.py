from pathlib import Path


if __name__ == "__main__":
    dir = Path(__file__).parent
    with dir.joinpath("preview.htm").open("w") as html: 
        html.write('<!DOCTYPE html>\n')
        html.write('<html lang="en">\n')
        html.write('<head>\n')
        html.write('<meta charset="UTF-8">\n')
        html.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        html.write('<meta http-equiv="X-UA-Compatible" content="ie=edge">\n')
        html.write('<title>Icons Preview</title>\n')
        html.write('</head>\n')
        html.write('<body bgcolor="#1d2229">\n')
        
        for image in dir.rglob("*.svg"):
            html.write('<img src="%s" width="16px" height="16px">\n' % image.relative_to(dir))

        html.write('</body>\n')
        html.write('</html>')
