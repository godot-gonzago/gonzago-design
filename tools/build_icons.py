import os
from scour import scour

os.makedirs('../icons/', exist_ok = True)

options = scour.parse_args([
    '--set-precision=5',
    '--create-groups',
    '--strip-xml-prolog',
    '--remove-descriptive-elements',
    '--enable-comment-stripping',
    '--enable-viewboxing',
    '--no-line-breaks',
    '--strip-xml-space',
    '--enable-id-stripping',
    '--shorten-ids'
])

# TODO: Do this for each icon
options.infilename = '../source/icons/gonzago.svg'
options.outfilename = '../icons/gonzago.svg'
(input, output) = scour.getInOut(options)
scour.start(options, input, output)
