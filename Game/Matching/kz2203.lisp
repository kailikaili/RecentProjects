(defun match ( p d &optional (a nil))
   (cond
       (;if both a null, return t or a
          (and (null p) (null d))
          (if(null a) t a)
       )
       (;if patern is null but data is not nil, return nil, match fails
          (and (null p) (not (null d)))
          nil
       )
       (;if pattern is not null, data is null, we should concern '*' in pattern
          (and (not (null p)) (null d))
          (if(equal (car p) '*) (match (cdr p) d a) nil)
       )
       (;if botu are atom 
          (and (atom p) (atom d))
          (equal p d)
       )
       (;both are list
          (and (listp p) (listp d))
          (cond
              (;if both (car p) and (car d) are list 
                 (and (listp (car p)) (listp (car d)))
                 ;match the result list, and iterate the results in following match
                 (let ((result (match (car p) (car d) a)))
                     (
                        iterate_ans (cdr p) (cdr d) result
                     )
                 )
              )
              (;most simple (car p) and (car d) are eqaul ,match (cdr p) and (cdr d)
                 (equal (car p) (car d))
                 (match (cdr p) (cdr d) a)
              )
              (;(car p) equals to ?, then match result part of p and d
                 (equal (car p) '?)
                 (match (cdr p) (cdr d) a)
              )
              (;if (car p) is a list and is started with ampersand  however (car d) is an atom, we need to call andmatch to check whether (car d) is satisfy the requirement list, if match succeeded, we should match rest of p and d
                 (and (listp (car p)) (atom (car d)))
                 (cond
                     (
                         (equal (car (car p)) '&)
                         (if (andmatch (cdr(car p)) (car d) a) (match (cdr p) (cdr d) a) nil)
                     )
                     (
                         t
                         nil
                     )
                 )
              )
              (;if (car p) equal to a '*'
                 (equal (car p) '*)
                 ;record the result of  (match (cdr p) d a) and (match p (cdr d) a) as a1 and a2
                 (let ((a1 (match (cdr p) d a))(a2 (match p (cdr d) a)))
                     (cond
                         (
                            (and (null a1) (null a2))
                            nil
                         )
                         (
                            (null a1)
                            a2
                         )
                         (
                            (null a2)
                            a1
                         )
                         (;when both a1 and a2 are not null, we should check whether a1 and a2 are equal, if not equal, we should merge a1 and a2
                            (and (atom (car (car a1))) (atom (car (car a2))))
                            (if(answer_equal a1 a2) a1 (merge_answer (list a1) (list  a2)))
                         )
                         (;if a1 is a single solution set, we need to merge (list a1) and a2
                            (atom (car (car a1)))
                            (merge_answer (list a1) a2)
                         )
                         (;otherwise wo need to merge a1 (list a2)
                            t
                            (merge_answer a1 (list a2))
                         )
                     )
                 )
                 ;(merge_answer (match (cdr p) d a) (match p (cdr d) a))
              )
              (;if (car p) is started with ? and a variable
                 (and (symbolp (car p)) (equal (elt (symbol-name (car p))  0) #\?))
                 (cond
                     (;if it is bounded , we need to match rest of p and d
                         (is_subset (merge_answer (car p) (car d)) a)
                         (match (cdr p) (cdr d) a)
                     )
                     (;if we can find associated value in solution set, return nil
                         (assoc (car p) a)
                          nil
                     )
                     (;if it is not bounded yet, we need to bind the value , update the solution set and complete rest match
                          t
                          (match (cdr p) (cdr d) (merge_answer a (merge_answer (car p) (car d))))
                     )
                 )
              )
              (; if (car p) is started with ! and a variable
                 (and (symbolp (car p))(equal (elt (symbol-name (car p))  0) #\!))
                 (
                    ;convert !symbol  to ?symbol
                    let ((result (assoc (intern (concatenate 'string "?" (subseq (symbol-name (car p)) 1 (length (symbol-name (car p))))))  a)))
                    (if (or (null result) (equal (cdr result)(list (car d)))) 
                        nil
                        (match (cdr p) (cdr d) a)
                    )
                 )
              )
              (; if (car p) is started with < and a variable
                 (and (symbolp (car p))(equal (elt (symbol-name (car p))  0) #\<))
                 (
                    ;convert !symbol  to ?symbol
                    let ((result (assoc (intern (concatenate 'string "?" (subseq (symbol-name (car p)) 1 (length (symbol-name (car p))))))  a)))
                    (if (or (null result) (equal (cdr result)(list (car d)))) 
                        nil
                        (match (cdr p) (cdr d) a)
                    )
                 )
              )
              (; if (car p) is started with > and a variable
                 (and (symbolp (car p))(equal (elt (symbol-name (car p))  0) #\<))
                 (
                    ;convert !symbol  to ?symbol
                    let ((result (assoc (intern (concatenate 'string "?" (subseq (symbol-name (car p)) 1 (length (symbol-name (car p))))))  a)))
                    (if (or (null result) (not (> (car  (cdr result)) (car d))))
                        nil
                        (match (cdr p) (cdr d) a)
                    )
                 )
              )
              (
                 (and (symbolp (car p))(equal (elt (symbol-name (car p))  0) #\>))
                 (
                    ;convert !symbol  to ?symbol
                    let ((result (assoc (intern (concatenate 'string "?" (subseq (symbol-name (car p)) 1 (length (symbol-name (car p))))))  a)))
                    (if (or (null result) (not (< (car  (cdr result)) (car d))))
                        nil
                        (match (cdr p) (cdr d) a)
                    )
                 )
              )
              (
                 t
                 nil
              )
          )
       )
       (
          t
          nil
       )
   )
)
;match function for ampersand 
(defun andmatch(p d a)
  (cond
      (
         (null p)
         t
      )
      (
         (equal (elt (symbol-name (car p))  0) #\?)
         (if(equal (cdr (assoc (intern (concatenate 'string "?" (subseq (symbol-name (car p)) 1 (length (symbol-name (car p)))))) a)) (list d))
             (andmatch (cdr p) d a)
             nil
         )
      )
      (
         (equal (elt (symbol-name (car p))  0) #\!)
         (if(not (equal (cdr (assoc (intern (concatenate 'string "?" (subseq (symbol-name (car p)) 1 (length (symbol-name (car p)))))) a)) (list d)))
             (andmatch (cdr p) d a)
             nil
         )
      )
      (
         (equal (elt (symbol-name (car p))  0) #\<)
         (if(>  (car (cdr (assoc (intern (concatenate 'string "?" (subseq (symbol-name (car p)) 1 (length (symbol-name (car p)))))) a))) d)
             (andmatch (cdr p) d a)
             nil
         )
      )
      (
         (equal (elt (symbol-name (car p))  0) #\>)
         (if(<  (car (cdr (assoc (intern (concatenate 'string "?" (subseq (symbol-name (car p)) 1 (length (symbol-name (car p)))))) a))) d)
             (andmatch (cdr p) d a)
             nil
         )
      )
      (
         t
         nil
      )
  )
)
;iterate answers in a to find and merge the result
(defun iterate_ans(p d a)
   (cond
       (
          (null a)
          nil
       )
       (
          (atom (car (car a)))
          (match p d a)
       )
       (
          t
          (let ((a1 (match p d (car a))) (a2 (iterate_ans p d (cdr a))))
            (cond
                (
                     (and (null a1) (null a2))
                            nil
                )
                ( 
                     (null a1)
                     a2
                )
                (
                     (null a2)
                     a1
                )
                (
                    (and (atom (car (car a1))) (atom (car (car a2))))
                    (if(answer_equal a1 a2) a1 (merge_answer (list a1) (list a2)))
                )
                (
                    (atom (car (car a1)))
                    (merge_answer (list a1) a2)
                )
                (
                    t
                    (merge_answer a1 (list a2))
                )
            )
         )
       )
   )
)
 
; merge answers to a list
(defun merge_answer(a1 a2)
   (cond
       (
          (and (null a1) (null a2))
          nil
       )
       (
          (and (null a1) (not (null a2)))
          a2
       )
       (
          (and (not (null a1)) (null a2))
          a1
       )
       (
          (atom a1)
          (list (list a1 a2))
       )
       (
          (and (atom (car (car a1))) (atom (car (car a2))))
          (if (answer_equal a1 a2) a1 (append a1 a2))
       )
       (
          (and (atom (car (car a1))) (not (atom (car (car a2)))))
          (if (in_answer_set a1 a2) a2 (append a2 (list a1)))
       )
       (
          (and (not (atom (car (car a1)))) (atom (car (car a2))))
          (if (in_answer_set a2 a1) a1 (append a1 (list a2)))
       )
       (
          (and (not (atom (car (car a1))))  (not (atom (car (car a2)))))
          (merge_answer (merge_answer a1 (car a2)) (cdr a2))
       )
       (
          t
          nil
       )
   )
)
;find whether a in answer set
(defun in_answer_set(a as)
  (cond
      (
         (null as)
         nil
      )
      (
         (answer_equal a (car as))
         t
      )
      (
         t
         (in_answer_set a (cdr as))
      )
  )
)
;determine whether they are equal
(defun answer_equal(l1 l2)
  (and (equal (length l1) (length l2))  (is_subset l1 l2))
)
; determine whether l1 is a subset of l2
(defun is_subset(l1 l2)
  (cond
      (
         (null l1)
         t
      )
      (
         (in_list (car l1) l2)
         (is_subset (cdr l1) l2)
      )
      (
         t
         nil
      )
  )
)
; check whether a target in the list ls
(defun in_list (tg ls)
  (cond
      (
         (null ls)
         nil
      )
      (
         (equal tg (car ls))
         t
      )
      (
         t
         (in_list tg (cdr ls))
      )
  )
)