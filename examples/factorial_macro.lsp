(defmacro fact (n)
  (prints 'n \n)
  (if (< n 3) n
    (* n (fact (- n 1)))))

(defmacro facc (n acc)
  (prints 'acc \n)
  (if (< n 2) acc
    (facc (- n 1) (* n acc))))
