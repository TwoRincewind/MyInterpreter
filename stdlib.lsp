;;;; stdlib

;;; useful stuff
(def \n "
")
(def nil '())
(def fn lambda)
(def nil? (macro (l) (_=_ l nil)))
(def list (lambda (. args) args))

;;; easier functions
(def defmacro-defun-codegen
	(lambda (head name args body)
	  (list def name
      (list head args
        (if (nil? body) nil
          (if (nil? (cdr body)) (car body)
      			(cons do body)))))))
(def defmacro (macro (name args . body) (eval (defmacro-defun-codegen macro 'name 'args 'body))))
(defmacro defun (name args . body) (eval (defmacro-defun-codegen lambda 'name 'args 'body)))
(def defn defun)

;;; useful functions
(defmacro comment (. a) nil)

(defun reduce (f a l) (if (nil? l) a (reduce f (f a (car l)) (cdr l))))
(defun foldr  (f a l) (if (nil? l) a (f (foldr f a (cdr l)) (car l))))

;;; boolean functions
(defun not (boo) (if boo false true))
(defun  or-codegen (args) (if (nil? args) true (list if (car args) true (or-codegen (cdr args)))))
(defun and-codegen (args) (if (nil? args) true (list if (car args) (and-codegen (cdr args)) false)))
(defmacro  or (. args) (eval ( or-codegen 'args)))
(defmacro and (. args) (eval (and-codegen 'args))) ; (and 1 2 3) = (if 1 (if 2 3 false) false)

(defun cond-codegen (args)
	(if (nil? args) nil ; (raise "wrong arity of cond")
    (if (nil? (cdr args)) (car args)
  		(list if (car args) (car (cdr args)) (cond-codegen (cdr (cdr args)))))))
(defmacro cond (. args) (eval (cond-codegen 'args))) ; (cond 1 2 3 4 5) = (if 1 2 (if 3 4 5))

;;; basic math operations
; (defun + (. args) (if (nil? args) 0 (reduce _+_ (car args) (cdr args)))) ; ability to interop +
(defun +  (. args) (reduce _+_  0  args)) ; (+ 1 2 3 4) = (_+_ 0 (_+_ 1 (_+_ 2 (_+_ 3 4))))
(defun *  (. args) (reduce _*_  1  args))
(defun ++ (. args) (reduce _++_ "" args))

(defun - (. args)
	(cond (nil? args) (raise "zero args for -")
	      (nil? (cdr args)) (_-_ 0 (car args))
	      (reduce _-_ (car args) (cdr args))))
(defun / (. args)
	(cond (nil? args) (raise "zero args for /")
	      (nil? (cdr args)) (_/_ 1 (car args))
	      (reduce _/_ (car args) (cdr args))))
(defun % (. args)
	(cond (nil? args) (raise "zero args for %")
	      (nil? (cdr args)) (raise "one arg for %")
	      (reduce _%_ (car args) (cdr args))))

;;; basic binary predicates
(defun bp-core (bp a l) (if (nil? l) true (if (bp a (car l)) (bp-core bp (car l) (cdr l)) false )))
(defun bp-pre-core (bp args) (if (nil? args) true (bp-core bp (car args) (cdr args))))

(defun <  (. args) (bp-pre-core _<_  args))
(defun >  (. args) (bp-pre-core _>_  args))

(defun _<=_ (a b) (if (not (_>_ a b))))
(defun _>=_ (a b) (if (not (_<_ a b))))
(defun <= (. args) (bp-pre-core _<=_ args))
(defun >= (. args) (bp-pre-core _>=_ args))

(defun three-op-eq (a b c) (if (_=_ a b) (_=_ b c) false))
(defun bineq (a b)
	(def type-a (typeof a))
	(def type-b (typeof b))
	(cond (three-op-eq type-a type-b "Symbol") (_=_ (++ a) (++ b))
	      (three-op-eq type-a type-b "List") (_=_ (++ a) (++ b))
	      (_=_ a b)))
(defun = (. args) (bp-pre-core bineq args))
