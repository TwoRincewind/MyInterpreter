(defn maybeprint (n) (when (= (% n 50) 0) (do (prints n " ") (flush))))
(defn odd? (n) (if (= n 0) false (do (maybeprint n) (even? (- n 1)))))
(defn even? (n) (if (= n 0) true (do (maybeprint n) (odd? (- n 1)))))
; (print (odd? (read)))