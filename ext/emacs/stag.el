;;; stag.el --- emacs interface for the stag source tagging tool.
;;
;; This file is not part of GNU Emacs.
;;
;;; Commentary:
;;
;; Description:
;;
;; Just read the code.

;;; Code:

(defcustom stag-program "stag"
  "The name of the stag program."
  :type '(string)
  :group 'stag)

(defun stag-find-defs (name)
  (interactive
   (list
    (read-string "Name: ")))
  ; TODO: Allow user to set tag file
  (let ((buff-name "*stag defs*"))
    (shell-command (format "%s find_defs %s" stag-program name) buff-name)
    (switch-to-buffer buff-name)))

;;;###autoload(require 'stag)
(provide 'stag)
