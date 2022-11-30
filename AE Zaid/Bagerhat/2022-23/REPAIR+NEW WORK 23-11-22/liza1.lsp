(defun c:liza1 (/ mx mn)

(setq oldsnap (getvar "osmode"));save snap settings
(setq oldblipmode (getvar "blipmode"));save blipmode setting
(setvar "osmode" 0);Switch OFF snap
(setvar "blipmode" 0);Switch OFF Blipmode
(command "style" "liza" "times.ttf" 2 1 0 "N" "N")
(setvar "osmode" 32);switch ON snap
(setq a (getpoint "\nPick a point : "))
(setvar "osmode" 0);Switch OFF snap
(setq b (getint "\nInsert Datum : "))


(setq y 0)

(while
(setq pt (getpoint "\nInsert Point : "))
(setq p1 (list (+ (car a) 5 (car pt))(- (cadr a) 4.5)))
(setq p2 (list (+ (car a) 5 (car pt))(cadr a)))
(command "Line" p1 p2 "")

(setq p1 (list (+ (car a) 5.1 (car pt))(- (cadr a) 2.25)))
(setq p2 (list (+ (car a) 5.6 (car pt))(- (cadr a) 4.4)))
(setq tx (rtos (car pt) 2 2))
(command "mtext" p1 "s" "liza" "r" "90" "h" "0.5" p2 tx "")`

(setq p1 (list (+ (car a) 5.1 (car pt))(cadr a)))
(setq p2 (list (+ (car a) 5.6 (car pt))(- (cadr a) 2.15)))
(setq tx (rtos (cadr pt) 2 2))
(command "mtext" p1 "s" "liza" "r" "90" "h" "0.5" p2 tx "")

(setq ptp (list (+ (car a) 5 (car pt))(+ (cadr a) (- (cadr pt) b))))

(if (= y 0)
(setq h1 a)
(command "Line" old ptp "")
)


(if (> (cadr pt) (cadr mn))
(setq mx (cadr pt))
(setq mx mx)
)


(if (> (cadr pt) (cadr mn))
(setq mn pt)
(setq mn mn)
)

(setq old ptp)
(setq y (+ y 1))
(setq h2 (list (+ (car a) 5 (car pt))(cadr a)))

)


(command "Line" h1 h2 "")

(setq i1 (list (car h1)(- (cadr h1) 2.25)))
(setq i2 (list (car h2)(- (cadr h2) 2.25)))
(command "Line" i1 i2 "")

(setq i1 (list (car i1)(- (cadr i1) 2.25)))
(setq i2 (list (car i2)(- (cadr i2) 2.25)))
(command "Line" i1 i2 "")


(setq t mx)

(setq y (fix (/ t 5)))
(setq y (* 5 (+ y 1)))
(setq y (+ 1 (- y b)))
(setq y (abs y))

(setq x b)
(setq z 0)

(repeat y
(setq p1 (list (car a)(+ (cadr a) z)))
(if (= (rem x 5) 0)
(setq p2 (list (- (car p1) 1)(cadr p1)))
(setq p2 (list (- (car p1) 0.5)(cadr p1)))
)
(if (= x b)
(setq p2 (list (- (car p1) 1)(cadr p1)))
(setq p2 p2)
)
(command "Line" p1 p2 "")


(setq b1 (list (- (car p1) 3)(+ (cadr p1) 0.25)))
(setq c1 (list (- (car p1) 1)(- (cadr p1) 0.25)))
(setq d1 (list (- (car p1) 8.5)(+ (cadr p1) 0.25)))

(setq sx (rtos x 2 2))
(setq tx (strcat "DATUM AT " sx " (m)"))

(if (= x b)
(command "mtext" d1 "s" "liza" "r" "0" "h" "0.5" c1 tx "")
(if (= (rem x 5) 0)
(command "mtext" b1 "s" "liza" "r" "0" "h" "0.5" c1 sx "")
(setq x x)
)
)
(setq x (+ x 1))
(setq z (+ z 1))
)


(setq p1 (list (- (car a) 8.5)(- (cadr a) 2)))
(setq q1 (list (- (car a) 1)(- (cadr a) 2.5)))
(setq p2 (list (- (car a) 8.5)(- (cadr a) 4.25)))
(setq q2 (list (- (car a) 1)(- (cadr a) 4.75)))
(command "mtext" p1 "s" "liza" "r" "0" "h" "0.5" q1 "EXISTING R.L. (m)" "")
(command "mtext" p2 "s" "liza" "r" "0" "h" "0.5" q2 "DISTANCE IN (m)" "")
(setq p3 (list (- (car a) 5)(+ (cadr a) 5)))
(setq q3 (list (- (car a) 1)(+ (cadr a) 15)))
(command "mtext" p3 "s" "liza" "r" "90" "h" "0.5" q3 "ELEVATION (m PWD)" "")
(setq p4 (list (car a)(- (cadr a) 4.5)))
(setq q4 (list (car a)(+ (cadr a) (- z 1))))
(command "Line" p4 q4 "")





(setvar "osmode" oldsnap);Reset snap
(setvar "blipmode" oldblipmode);Reset blipmode

(princ)
)
(princ)