---
title: "Tips for LaTeXing in Sublime"
toc: true
categories:
  - Tips
tags:
  - LaTeX
  - Sublime
toc_sticky: True
---

(This post is migrated from my old [Blogspot](https://jwt625.blogspot.com/2017/05/tips-for-latexing-in-sublime.html). Bear with my broken English at the time.)

# Environment
I’m using Sublime (both 2 and 3) on Windows, with [LaTeXTools](https://github.com/SublimeText/LaTeXTools) plugin for using LaTeX.

# Shortcuts for LaTeXTools
Comma means its a ‘combo’ shortcut, you push the first set of buttons and then the second button.

delete temp files: `ctrl+l`, `Backspace`
forward search in pdf: `ctrl+l, j`
More to be added.

# Inverse search from Sumatra PDF
The default option for Sumatra PDF to perform inverse search might be WinEdit. I’d like it to be Sublime.

So for me in Sumatra PDF, go to `Settings -> Options`, set the inverse search command to `"C:\Program Files\Sublime Text 3\sublime_text.exe" "%f:%l"`

If you are using other editors, you can refer to [The SumatraPDF Inverse-Search for any arbitrary Editor](https://tex.stackexchange.com/questions/125546/the-sumatrapdf-inverse-search-for-any-arbitrary-editor).

# Auto-completion for labels and refs across multiple files
Looks like it’s supported. Simply add %!TEX root = relativePathToYour/main.tex on the first line of your separated .tex file.

See [Sublime Text: Reference completion across multiple files using LaTeXTools and import](https://tex.stackexchange.com/questions/345519/sublime-text-reference-completion-across-multiple-files-using-latextools-and-im) for reference.

