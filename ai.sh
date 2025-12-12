#!/bin/bash

if type npm >/dev/null 2>&1; then (cd npm && make install); fi
if type bun >/dev/null 2>&1; then (cd bun && make install); fi

# good idea? or bad?
(cd npm && make update)
(cd bun && make update)

(cd gemini && make install)
(cd claude && make install)
(cd codex && make install)
(cd mistral && make install)
