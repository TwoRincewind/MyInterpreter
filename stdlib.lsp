; stdlib

(def \n "
")

(def nil '())
(def fn lambda)

(def list (lambda (. args) args))

(def defmacro-codegen (lambda (name args body) (list def name (list macro args (cons do body)))))
(def defmacro (macro (name args . body) (eval (defmacro-codegen 'name 'args 'body))))

(def defun-codegen (lambda (name args body) (list def name (list lambda args (cons do body)))))
(defmacro defun (name args . body) (eval (defun-codegen 'name 'args 'body)))
(def defn defun)

(defun nil? (l) (_=_ l nil))

(defmacro comment (. a) nil)

(defun reduce (f a l) (if (nil? l) a (reduce f (f a (car l)) (cdr l))))
(defun foldr  (f a l) (if (nil? l) a (f (foldr f a (cdr l)) (car l))))

(defun + (. args) (if (nil? args) 0 (reduce _+_ (car args) (cdr args))))
; (+ 1 2 3 4) = (_+_ 1 (_+_ 2 (_+_ 3 4)))
(defun * (. args) (reduce _*_ 1 args))
(defun ++ (. args) (reduce _++_ "" args))
(defun - (. args) (if (nil? args) (raise "zero args for -")
		   (if (nil? (cdr args))
		   (_-_ 0 (car args))
		   (reduce _-_ (car args) (cdr args))
		   )))
(defun / (. args) (if (nil? args) (raise "zero args for /")
		   (if (nil? (cdr args))
		   (_/_ 1 (car args))
		   (reduce _/_ (car args) (cdr args))
		   )))
(defun % (. args) (if (nil? args) (raise "zero args for %")
		   (if (nil? (cdr args)) (raise "one arg for %")
		   (reduce _%_ (car args) (cdr args))
		   )))
(def < _<_)  ; temporary crutch
