"(def \n "
")
(def acc-class (lambda () 
  (do
  (def get (dambda () val))
  (def add (dambda (delta)
    (do
      (set! val (_+_ val delta))
      val
    )))
  (def sub (dambda (delta)
    (do
      (def new (_-_ val delta))
      (if (_<_ new 0) (print (_++_ "аяяй" \n)) (set! val new))
      val
    )))
  (def acc-constructor (lambda (val) (lambda (method-name) (eval (eval method-name) ))))
  acc-constructor
)))"

(def nil '())

(def acc-class (lambda (initial-val)
  (do
    (def val initial-val)
    (lambda (all-args)
      (do
        (def method (car all-args))
        (def args (cdr all-args))

        (def get (dambda () val))
        (def add (dambda (delta)
          (do
            (set! val (_+_ val delta))
            val
          )))
        (def sub (dambda (delta)
          (do
            (def new (_-_ val delta))
            (if (_<_ new 0) (print (_++_ "аяяй" "\n")) (set! val new))
            val
          )))

        (if (_==_ method (symbol "get"))
          (get)
          (if (_==_ method (symbol "add"))
            (add (car args))
            (if (_==_ method (symbol "sub"))
              (sub (car args))
              nil))))))))
