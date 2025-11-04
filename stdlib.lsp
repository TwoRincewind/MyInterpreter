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
(defun  or-codegen (args) (if (nil? args) false (list if (car args) true (or-codegen (cdr args)))))
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
(defun != (. args) (not (bp-pre-core bineq args)))

;;; list tools
(defun map (func lst)
	(if (nil? lst) nil
    (cons (func (car lst)) (map func (cdr lst)))))

(defun reverse-core (lst acc) (if (nil? lst) acc (reverse-core (cdr lst) (cons (car lst) acc))))
(defun reverse (lst) (reverse-core lst nil))

(defun map-reverse-core (func lst acc)
	(if (nil? lst) acc
    (map-reverse-core func (cdr lst) (cons (func (car lst)) acc))))
(defun map-reverse (func lst) (map-reverse-core func lst nil))
(defun map-tail (func lst) (reverse (map-reverse func lst)))

(defun filter (pred lst)
	(cond (nil? lst) nil
			  (pred (car lst)) (cons (car lst) (filter pred (cdr lst)))
			  (filter pred (cdr lst))))

(defun take (n lst)
	(cond (< n 1) nil
	  		(nil? lst) nil
	  		(cons (car lst) (take (- n 1) (cdr lst)))))

(defun drop (n lst)
	(cond (< n 1) lst
	  		(nil? lst) nil
	  		(drop (- n 1) (cdr lst))))

(defun append-reverse (a b)
	(if (nil? a) b (append-reverse (cdr a) (cons (car a) b))))
(defun append (a b) (append-reverse (reverse a) b))

(defun concat (lsts) (reduce append nil lsts))

(defun length (lst) (reduce (lambda (a b) (+ a 1)) 0 lst))

(defun all? (pred lst)
	(cond (nil? lst) true
	      (pred (car lst)) (all? pred (cdr lst))
	      false))

(defun any? (pred lst)
	(cond (nil? lst) false
	      (pred (car lst)) true
	      (any? pred (cdr lst))))

(defun indexof-from (elem lst idx)
	(cond (nil? lst) -1
	      (= elem (car lst)) idx
	      (indexof-from elem (cdr lst) (+ 1 idx))))
(defun indexof (elem lst) (indexof-from elem lst 0))

(defun range (a b)
	(if (< a b) (cons a (range (+ 1 a) b)) nil))

(defun range-tail-core (a b acc)
	(if (< a b) (range-tail-core a (- b 1) (cons (- b 1) acc)) acc))
(defun range-tail (a b) (range-tail-core a b nil))

(defun list-ref (n lst)
	(def tmp (drop n lst))
	(if (nil? tmp) (raise (++ "index out of bounds: " n " of " lst))
	    (car tmp)))

(defun zip-with (f a b)
	(if (or (nil? a) (nil? b)) nil
	    (cons (f (car a) (car b)) (zip-with f (cdr a) (cdr b)))))

(defun flatten (lsts)
	(cond (!= (typeof lsts) "List") (list lsts)
	      (nil? lsts) nil
	      (append (flatten (car lsts)) (flatten (cdr lsts)))))

(defun dedupe (lst)
	(if (nil? lst) nil
	    (cons (car lst) (dedupe (filter (lambda (v) (!= v (car lst))) (cdr lst))))))



(defun prints (. args) (reduce (lambda (nothing arg) (print arg)) nil args))



(prints "stdlib loaded" \n)
