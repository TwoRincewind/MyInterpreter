(def t (macro (x) (do (def z 42) (print x) x)))
(def m (dambda (a) (do (print z) (_+_ a a) (print z))))
(print (m (t 3)))

