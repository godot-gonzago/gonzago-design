# Gonzago Framework Editor Icons

Editor icons for use in Gonzago Framework

## Icons

<table>
@begin:icons
  <thead><tr><th align="left" colspan="4" width="2048">Gonzago</th></tr></thead>
  <tbody>
@begin:icon_row
    <tr>
@begin:icon
      <td><img src="{image_src}" width="24" height="24"></td>
      <td>
        <p>
          {meta.get('title', rel_path.stem)} <a href="{relation}" target="_blank">:pushpin:</a>
          <br><var>{', '.join(subject)}</var>
        </p>
      </td>
@end:icon
@if:icons.count%2 == 1
      <td colspan="2"></td>
@end:icons.count%2
    </tr>
@end:icon_row
  </tbody>
@end:icons
</table>
