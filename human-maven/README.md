How to use:

Pipe maven's output to this script. Personally, on Windows, I have a custom `mvn.bat` in `PATH`, with this:

    @call java8env.bat
    @call C:\Users\yura\apps\apache-maven-3.3.9\bin\mvn.cmd %* | python C:\Users\yura\p\scripts\human-maven\human-maven.py
