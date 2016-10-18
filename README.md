gaepyfpdf
=========
On Google App Engine you are not allowed to write to the file system. This makes it impossible to use custom fonts,
and by extension unicode characters.

With this fork I'm modifying pyfpdf to use an in memory cache instead or writing to the file system.


For further information on pyfpdf, see the project site:
https://github.com/reingart/pyfpdf
