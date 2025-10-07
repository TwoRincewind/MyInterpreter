This project should grow up to LISP command line interpreter.
Current functional:
1. Recognizes:
    - ; single-line comments
    - (lists)
    - "strings"
    - anything else as token (string for now), separates by whitespaces and commas
2. Supports:
    - unclosed strings and lists detection
    - :l :load for loading file (just prints them for now)
    - :q :quit :exit self-explanatory
3. Nuances:
    - treats file input as console input (always prints every top-level object for now)

