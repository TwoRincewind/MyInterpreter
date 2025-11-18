(defmacro odd? (n) (if (= n 0) false (even? (- n 1))))
(defmacro even? (n) (if (= n 0) true (odd? (- n 1))))