# Gonzago Framework Palettes

Different palettes for use in Gonzago Framework and its design elements.

## Formats

<table>
  <thead>
    <tr>
      <th align=\"left\">ID</th>
      <th align=\"left\">Suffix</th>
      <th align=\"left\">Description</th>
    </tr>
  </thead>
  <tbody>
@begin:format
    <tr><td>{format.id}</td><td>{format.suffix}</td><td>{format.description}</td></tr>
@end:format
  </tbody>
</table>

## Palettes\n\n"

@begin:palette
### {palette.name}
@cond:palette.description

{palette.description}
@end:palette.description

<table>
@cond:palette.version
  <tr><th>Version</th><td>{palette.version}</td></tr>
@end:palette.version
@cond:palette.author
  <tr><th>Author</th><td>{palette.author}</td></tr>
@end:palette.author
@cond:palette.source
  <tr><th>Source</th><td>{palette.source}</td></tr>
@end:palette.source
  <tr>
    <th>Colors</th>
@begin:palette.colors
    <td>
      <p>{palette.color.name}
      <br>{palette.color.description}
      <br><img src=\"https://placehold.co/24x24/{palette.color.hex}/{palette.color.hex}/png\" /> #{palette.color.hex}
    </td>
@end:palette.colors
  </tr>
</table>
@end:palette
