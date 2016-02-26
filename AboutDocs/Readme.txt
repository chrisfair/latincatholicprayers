Latin Catholic Prayers is a simple application with the aim in mind to quiz
prayers until you know them by heart.  It is provided free because I really
want to encourage the memorization of Catholic Prayers and specifically
memorization of Catholic Prayers in Latin.

Unfortunately the Linux package requires the latest ubuntu Linux 10.10 because
its dependencies on the OS change fairly drastically between versions.  The
windows version requires that the visual C++ runtime is installed or it will
not run.  The visual C++ runtime can be found at
http://www.microsoft.com/downloads/en/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en

There is a good chance that most folks already have it installed, but there is
always the off chance that someone does not.  In any case install the runtime
and everything should work.  One issue with the Windows version is that whenever
the grammar option is used it generates multiple DOS windows while it is calculating
the grammar.  I cannot seem to get that to go away.  It does not hurt the overall
function of the program but it is aesthetically annoying.

If you find the program useful I really hope that you will consider doing a
donation.  As I say in the program I am a single  widowed Catholic dad with two
boys one has autism and every dollar I can save is another chance that the
two kids will have money for college someday.  Otherwise I just do not have the
resources to get them to college.

The program does require Python 2.6, wxpython, and pyglet to work.  All of those
are taken care of in the packages but if you want to download the source code
and modify it you will need these libraries.  Of these pyglet is not a standard
debian package and you will need to download it.  The locations of these follow:

http://www.python.org/download/releases/2.6.6/
http://www.wxpython.org/download.php#stable  (note that you must get the python
2.6 version...if you have Linux you can get it through the repositories)
http://www.pyglet.org/download.html  (if you use Linux you will have to get
AVBIN which is separate)

I do not have a MAC and I cannot build the MAC executable but you can use the
mercurial source in conjunction with these dependencies to make it work on your
box.  You will also need the MAC version of Whitaker's words and modify the
source to get it to work with the program.