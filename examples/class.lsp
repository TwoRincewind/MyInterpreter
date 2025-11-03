(def endl "
")

(def acc-class
  (lambda ()
    (do
      (def get '(lambda () val))
      (def add
        '(lambda (delta)
          (do
            (set! val (+ val delta))
            val)))
      (def sub
        '(lambda (delta)
          (do
            (def new (- val delta))
            (if (< new 0) (print (++ "аяяй" endl)) (set val new))
            val)))
      (def acc-constructor (lambda (val) (lambda (method) (eval (eval method)))))
      acc-constructor)))
