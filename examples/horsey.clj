; path: list of points ((1 3) (3 5) (5 7))
;                         ^
; stack - список ещё не проверенных направлений
; 

; (((1 2) (1 -2) (-1 2) (-1 -2)) ((1 -2) (-1 2) (-1 -2)) ((-1 2) (-1 -2)))
; (( ... ) ((1 -2) (-1 2) (-1 -2)) ((1 -2) (-1 2) (-1 -2)) ((-1 2) (-1 -2)))
; (() ((1 -2) (-1 2) (-1 -2)) ((-1 2) (-1 -2)))
; ((2 5) (1 3) (3 5) (5 7))

;; Сделать так, чтобы код работал для доски 8x8
;; Необходимо сделать Tail Call Optimization 

(def m 6)
(def n 6)
(def nm (* n m))
(def start-position '(1 1))

;;   

;; (defn check-step? (step path)  ; '(to from)
;;     (cond (or (nil? path) (nil? (cdr path))) false
;;         (= (take 2 path) step) true
;;         (check-step? step (cdr path))))

;; (a b c d e a b f g)

(defn in-borders? (p) (and (<= 1 (car p) n) (<= 1 (car (cdr p)) m)))

;; (defn duplicated-step? (path) (check-step? (take 2 path) (cdr path)))

;; (def all-dirs '((2 1) (2 -1) (-2 1) (-2 -1) (1 2) (1 -2) (-1 2) (-1 -2)))
;; (def all-dirs '((1 2) (2 1) (2 -1) (1 -2) (-1 -2) (-2 -1) (-2 1) (-1 2)))
(def all-dirs '((2 1) (1 2) (-1 2) (-2 1) (-2 -1) (-1 -2) (1 -2) (2 -1)))
;; @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

(def all-cells
    (concat (map (lambda (r) 
         (map (lambda (c)
              (list r c))
              (range 1 (+ 1 m)))) 
         (range 1 (+ 1 n)))))


(def all-moves (concat (map (lambda (cell)
                      (filter (lambda (step) (in-borders? (car step)))
                              (map (lambda (delta-move) (list (zip-with + cell delta-move) cell))
                                   all-dirs)))
    all-cells)))


(defn steps-set-gen ()
  (eval (cons do (map (lambda (step) (list def (symbol (++ step)) false)) all-moves)))
  (defn add (x) (eval (list set! (symbol (++ x)) true)))
  (defn has? (x) (eval (symbol (++ x))))
  (defn remove (x) (eval (list set! (symbol (++ x)) false)))
  (lambda (cmd) (eval cmd))
)

(def steps-set (steps-set-gen))

(defn step-was? (step) ((steps-set 'has?) step))

;; @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

(defmacro -= (x v) (set! x (- x v)))
(defmacro += (x v) (set! x (+ x v)))

(defn cells-multiset-gen ()
  (eval (cons do (map (lambda (cell) (list def (symbol (++ cell)) 0)) all-cells)))
  (def distinct 0)
  (defn add (x) (do
                (def name (symbol (++ x)))
                (when (= (eval name) 0) (+= distinct 1))
                (eval (list += name 1))))
  (defn remove (x) (do
                (def name (symbol (++ x)))
                (when (= (eval name) 1) (-= distinct 1))
                (eval (list -= name 1))))
;;   (defn distinct () xxx)
  (lambda (cmd) (eval cmd))
)

(def cells-multiset (cells-multiset-gen))

(defn path-isgood? (path) (and (= (car path) start-position) (= (cells-multiset 'distinct) nm)))

;; @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

(defn dfs-tail (path stack)
    ;; (print path)
    (if
        ; success
        (path-isgood? path) path (if
        ; если мы выше начала - нет решения
        (nil? path) false (if
        ; если некуда ходить из текущей позиции
        (nil? (car stack)) (do
                                (if (not (nil? (cdr path))) ((steps-set 'remove) (take 2 path)) nil)
                                ((cells-multiset 'remove) (car path))
                                (dfs-tail (cdr path) (cdr stack)))
        ; иначе нам есть что делать
        (do (def next-pos (zip-with + (car path) (car (car stack))))
            (def step (list next-pos (car path)))
            (def new-stack (cons (cdr (car stack)) (cdr stack)))
            (if
                ; если мы резко оказались вне доски
                (not (in-borders? next-pos)) (dfs-tail path new-stack) (if
                ; если этот ход мы уже делали
                (step-was? step) (dfs-tail path new-stack)
                (do
                    ((steps-set 'add) step)
                    ((cells-multiset 'add) next-pos)
                    (dfs-tail (cons next-pos path) (cons all-dirs new-stack))))))))))

(print (dfs-tail (list start-position) (list all-dirs)))
