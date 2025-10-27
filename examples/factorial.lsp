(def comment (macro (some) '()))

(comment
  (print "input a number")
  (def n (read))
  (def res 1)
  ; (print (_+_ n 1))
  (def f '(do
	    (set! res (_*_ res n))
	    (set! n (_-_ n 1))
	    (if (_<_ 0 n) (eval f) 0)
	    ))
  (eval f)
  (print res)

  (def t (macro (x) (do (def z 42) (print x) x)))
  (def m (dambda (a) (do (print z) (_+_ a a) (print z))))
  (print (m (t 3)))
  )


(def dact (dambda (n self) (
		if (_<_ n 2) 1
		(_*_ n (self (_-_ n 1) self))
	)))

(def lact (lambda (n self) (
		if (_<_ n 2) 1
		(_*_ n (lact (_-_ n 1) self))
	)))

(def foo (lambda (f, n) (do (def lact 43) (def dact 42) (f n f))))
