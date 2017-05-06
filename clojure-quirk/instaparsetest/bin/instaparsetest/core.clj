(ns instaparsetest.core
  (:use clojure.pprint)
  (:require [instaparse.core :as insta]))
;function that retursn exponent of x^n
(defn exp [x n]
  (reduce * (repeat n x)))
(defn negV [n] (- n))
;helper print function with return of printed value
(defn ret-print [thingToPrint]
  (println thingToPrint)
  thingToPrint)

(defn third [aList] (nth aList 2))
(defn fourth [aList] (nth aList 3))
(defn fifth [aList] (nth aList 4))
(defn seventh [aList] (nth aList 6))

(defn stFirst [subtree] (first (first subtree)))
(defn stSecond [subtree] (second (first subtree)))

(defn CallByLabel [labelName & args]
  ;(println args)
  ;(apply (resolve (symbol (name labelName))) args))
  (apply (ns-resolve 'instaparsetest.core (symbol (name labelName))) args))

(defn interpret-quirk [subtree scope]
  ;(pprint subtree)
  (CallByLabel (first subtree) subtree {}))

;the following functions reduce
;(CallByLabel (first (second subtree)) (second subtree) scope)
;to this:
;(CallByLabel (stSecond subtree) (second subtree) scope)

;(CallByLabel (stSecond subtree) (second subtree) scope)

(defn Program [subtree scope]
  (println "PROGRAM")
  (pprint subtree)

 ;[:Program [:Statement ...] [:Program ... ]]
 ;[:Program [:Statement ...]]
  (if
   ;Program0
   (< 2 (count subtree))
     ;(println "Here stupid"));;if count of subtree is greater than 2
    ((def newScope (CallByLabel (first (second subtree)) (second subtree) scope))
     (ret-print newScope)
      ;(System/exit 0))
     (CallByLabel (first (third subtree)) (third subtree) newScope)))
   ;Program1
  (if (>= 2 (count subtree))
    (CallByLabel (first (second subtree)) (second subtree) scope))
  (System/exit 0))

(defn Statement [subtree scope]
  (println "STATEMENT")
  (pprint subtree)
  (CallByLabel (first (second subtree)) (second subtree) scope))

(defn FunctionDeclaration [subtree scope]
  (println "FUNCTIONDECLARATION")
  ;(pprint subtree)
  ;(println (first (fifth subtree)))
  (def func_name (ret-print (CallByLabel (first (third subtree)) (third subtree) scope)))
  (def func_params (ret-print (CallByLabel (first (fifth subtree)) (fifth subtree) scope)))
  ;(println func_params)(System/exit 0))
  (def body_func (ret-print (CallByLabel (first (seventh subtree)) (seventh subtree) func_params)))
  (cond
    (ret-print (= [] func_params))
    (assoc scope func_name body_func))
  ;(assoc scope func_name body_func)
  ;(assoc scope func_name [func_params body_func])
)
  ;(System/exit 0)
  ;(ret-print(assoc scope
                   ;(ret-print(CallByLabel (first (third subtree)) (third subtree) scope))

                   ;(def func_dec (CallByLabel (first (fifth subtree)) (fifth subtree) scope) (CallByLabel (first (seventh subtree)) (seventh subtree) func_dec))))
  ;(System/exit 0) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  ;(cond
    ;(= :Name (first (third subtree)))
       ;(CallByLabel (first (second subtree)))


(defn FunctionParams [subtree scope]
  (println "FUNCTIONPARAMS")
  (pprint subtree)
  ;(println (first(second subtree)))
  ;(System/exit 0)
  (cond
    (= :RPAREN (first (second subtree)))
    []
    (= :NameList (first (second subtree)))
    (CallByLabel (first (second subtree)) (second subtree) scope)
    ))

(defn FunctionBody [subtree scope]
  (println "FUNCTIONBODY")
  (pprint subtree)
  (println scope)
  (cond
    (= 2 (count subtree))
    (CallByLabel (first (second subtree)) (second subtree) scope)
    (= :Program (first (second subtree)))
    ((def newScope (CallByLabel (first (second subtree)) (second subtree) scope))
     (ret-print newScope)
      ;(System/exit 0))
     (CallByLabel (first (third subtree)) (third subtree) newScope))
    )
  )
;(= :Return (first (second subtree)))
    ;(CallByLabel (first (second subtree)) (second subtree) scope)))
(defn Return [subtree scope]
  (println "RETURN")
  (pprint subtree)
  ;(println scope)
  (ret-print (CallByLabel (first (third subtree)) (third subtree) scope)))

(defn Assignment [subtree scope]
  ;(println "ASSIGNMENT")
  ;(pprint subtree)
  (CallByLabel (first (second subtree)) (second subtree) scope))

(defn SingleAssignment [subtree scope]
  (println "SINGLEASSIGNMENT")
  (pprint subtree)
  ;(println (fifth subtree))
  ;(System/exit 0)
  (cond
    (= :VAR (first (second subtree)))
    (ret-print (assoc scope (CallByLabel (first (third subtree)) (third subtree) scope) (CallByLabel (first (fifth subtree)) (fifth subtree) scope)))))

(defn MultipleAssignment [subtree scope]
  (println "MULTIPLEASSIGNMENT")
  (pprint subtree)
  (System/exit 0))

(defn Print [subtree scope]
  (println "PRINT")
  (pprint subtree)
  (ret-print (CallByLabel (first (third subtree)) (third subtree) scope)))

(defn NameList [subtree scope]
  (println "NAMELIST")
  (pprint subtree)
  (println (count subtree))
  ;(pprint (first(second subtree)))
  ;(pprint (first (fourth subtree)))
  ;(pprint (first (third subtree)))
  ;(CallByLabel (first(fourth subtree))(fourth subtree) scope)
  ;(System/exit 0)
  (cond
    (= 2 (count subtree))
     (CallByLabel (first (second subtree)) (second subtree) scope)
    (= :COMMA (first (third subtree)))
    (conj (assoc scope (CallByLabel (first(second subtree)) (second subtree) scope) nil)
          (assoc scope (CallByLabel (first(fourth subtree))(fourth subtree) scope) nil))
   ))

(defn ParameterList [subtree scope]
  (println "PARAMETERLIST")
  (pprint subtree)
  ;(println (count subtree))
  (cond
    (= 2 (count subtree))
    (CallByLabel (first (second subtree)) (second subtree) scope)))

(defn Parameter [subtree scope]
  (println "PARAMETER")
  (pprint subtree)
  (println scope)
  (CallByLabel (first (second subtree)) (second subtree) scope))

(defn Expression [subtree scope]
  (println "EXPRESSION")
  ;(println (count subtree))
  (pprint subtree)
	;(println (first (fourth subtree)))
  ;(System/exit 0)
  (cond
    (= 2 (count subtree))
    (CallByLabel (first (second subtree)) (second subtree) scope)
    (= :ADD (first (third subtree)))
     (+ (CallByLabel (first (second subtree)) (second subtree) scope)
        (CallByLabel (first (fourth subtree)) (fourth subtree) scope))
    (= :SUB (first (third subtree)))
    (- (CallByLabel (first (second subtree)) (second subtree) scope)
       (CallByLabel (first (fourth subtree)) (fourth subtree) scope))))

(defn Term [subtree scope]
  (println "TERM")
  (pprint subtree)
  ;(println (first (third subtree)))
  ;(println (count subtree))
  ;(println (count subtree))
  ;(System/exit 0)
  (cond
    (= 2 (count subtree))
    (CallByLabel (first (second subtree)) (second subtree) scope)
    (= :MULT (first (third subtree)))
    (* (CallByLabel (first (second subtree)) (second subtree) scope)
       (CallByLabel (first (fourth subtree)) (fourth subtree) scope))
    (= :DIV (first (third subtree)))
    (/ (CallByLabel (first (second subtree)) (second subtree) scope);quot???
       (CallByLabel (first (fourth subtree)) (fourth subtree) scope)))); end Term


(defn Factor [subtree scope]
  (println "FACTOR")
  (pprint subtree)
  (cond
    (= 4 (count subtree))
    (Math/pow (CallByLabel (first (second subtree)) (second subtree) scope)
              (CallByLabel (first (fourth subtree)) (fourth subtree) scope))
    (= 2 (count subtree))
    (CallByLabel (first (second subtree)) (second subtree) scope)))

(defn FunctionCall [subtree scope]
  (println "FUNCTIONCALL")
  (pprint subtree)
  ;(System/exit 0)
  (def check_Empty (CallByLabel (first (fourth subtree)) (fourth subtree) scope))
  (cond (= [] check_Empty)
        (CallByLabel (first (second subtree)) (second subtree) scope)
    ;(CallByLabel (first (fourth subtree)) (fourth subtree) scope))
  ;(System/exit 0)
))

(defn FunctionCallParams [subtree scope]
  (println "FUNCTIONCALLPARAMS")
  (pprint subtree)
  (if (>= 2 (count subtree))
    []))

(defn SubExpression [subtree scope]
  (println "SUBEXPRESSION")
  (pprint subtree)
  (cond
    (= :LPAREN (first (second subtree)))
    (CallByLabel (first (third subtree)) (third subtree) scope)))

(defn Value [subtree scope]
  (println "VALUE")
  (pprint subtree)
  ;(println "heyhey")
  ;(pprint (second subtree))
  (CallByLabel (first (second subtree)) (second subtree) scope)
  ;(System/exit 0)
)

(defn Name [subtree scope]
  (println "NAME")
  (println subtree)
  (ret-print scope)
  ;(System/exit 0)
  (cond
    (= nil (get scope (last (second subtree))))
    (ret-print(last (second subtree)))
    :else
    (get scope (second (second subtree)))))

(defn Num [subtree scope]
  (println "NUM")

  (println subtree)
  ;(System/exit 0)
  (def sign (ret-print(first (second  subtree))))
  ;(println (* -1 (Double/parseDouble(second (third subtree)))))
  ;(System/exit 0)
  ;(if (ret-print(> 2 (count subtree)))
  ;(def getDigit (Double/parseDouble (second (third subtree))))
 ; )
  (cond
    (= :SUB sign)
    (ret-print (negV (Double/parseDouble (second (third subtree)))))
    (= :ADD sign)
    (ret-print (Double/parseDouble (second (third subtree))))
    (= 2 (count subtree))
    (ret-print (Double/parseDouble (second (second subtree)))))
  ;(System/exit 0)
)
;(defn Num [subtree scope]

  ;(pprint subtree)
  ;(println (second (second subtree)))
  ;(ret-print (Double/parseDouble (second (second subtree)))))

(defn -main [& args]
  (def quirk-parser (insta/parser (slurp "resources/quirk-grammar-ebnf.txt") :auto-whitespace :standard))
  (def parse-tree (quirk-parser (slurp *in*))) ;; "print 1" "print + 1"

  (if (.equals "-pt" (first *command-line-args*))
    (def SHOW_PARSE_TREE true))
  (if (= true SHOW_PARSE_TREE)
    (pprint parse-tree)
    (interpret-quirk parse-tree {})))