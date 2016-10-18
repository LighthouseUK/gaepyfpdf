gaepyfpdf
=========
On Google App Engine you are not allowed to write to the file system. This makes it impossible to use custom fonts,
and by extension unicode characters.

With this fork I'm modifying pyfpdf to use an in memory cache instead or writing to the file system.


For further information on pyfpdf, see the project site:
https://github.com/reingart/pyfpdf


TODO:
====
- Need to completely refactor all of the code that loads font data. With a ram disk we can avoid a lot of file checking.
This will help simplify the code. If we need to dump the ram disk to a file then we can do it from a single location
instead of littering the code with file open ops.