This project should grow up to LISP command line interpreter.
Current functional:
1. Recognizes:
    - ; single-line comments
    - (lists)
    - "strings"
    - 123 as int
    - 3.14 as float
    - Special Forms {n} SF: (SF ... {n arguments})
        - {1} `quote` to store it without evaluation
        - {1} `eval` to evaluate
        - {1} `typeof` to get the type of object
        - {2} `cons` to add first elem to second (should be list)
        - {1} `car` to get head of the list
        - {1} `cdr` to get all but the first items of the list
        - {3} `if` <=> first ? second : third
        - {...} `do` to eval every object and return the last one
        - {1} `print` to print object (to console for now)
        - {0} `read` to read object (from console for now)
        - {1} `symbol` to treat string as symbol's name
        - {2} `def` to define first (should be symbol) with second
        - {2} `set` to rewrite first (symbol) with second
        - {2} `lambda` to make callable function:
            first as list of arguments (should be list of symbols to use in code);
            second as body with code.
            Lambdas can be called same as builtin expression.
    - Binary Operations BO (BO first second):
        - \_+\_ as addition
        - \_-\_ as substraction
        - \_*\_ as multiplication
        - \_/\_ as division
        - \_%\_ as getting remainder of division
        - \_++\_ as concatenation into strings
    - Binary Predicats BP (BP first second):
        - \_<\_ as "first less than second"
        - \_>\_ as "first greater than second"
        - \_==\_ as "first equals second"
    - anything else as token, separates by whitespaces and commas
2. Supports:
    - '<...> as simple form of quote
    - detection of unclosed strings and lists
    - :l :load for loading file for evaluation
    - :q :quit :exit self-explanatory
    - : for repeating last command
3. Config moments:
    - car and cdr treat non-list x as (x) and return x and () respectively
    - procedures return ()
    - symbols can be redefined (for now)
    - only last object is shown in case of input redirected from file (and there isn't load/exit for now)
    - passing not enough values to lambda will result in another lambda with remainded arguments
    - extra arguments will be packed to list and passed with the last one
