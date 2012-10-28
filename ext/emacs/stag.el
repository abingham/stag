;;; stag.el --- emacs interface for the stag source tagging tool.
;;
;; This file is not part of GNU Emacs.
;;
;;; Commentary:
;;
;; Description:
;;
;; Just read the code.

; TODO: A better intro comment.

;;; Code:

(defcustom stag-program "stag"
  "The name of the stag program."
  :type '(string)
  :group 'stag)

(defcustom stag-tag-file "STAG.sqlite"
  "The name of the file containing tag information."
  :type '(string)
  :group 'stag)

(defun stag-find-defs (name)
  "Find definitions in a stag tag file."
  (interactive
   (list
    (read-string "Name: ")))
  (let ((buff-name "*stag defs*"))
    (shell-command 
     (format "%s find_defs --tagfile=%s %s" 
	     stag-program 
	     stag-tag-file
	     name) 
     buff-name)
    (switch-to-buffer buff-name)))

; TODO: Rescan
; TODO: Find refs

;;;###autoload(require 'stag)
(provide 'stag)
