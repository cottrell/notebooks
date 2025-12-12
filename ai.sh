#!/bin/bash

if ! type node >/dev/null 2>&1; then (cd nodejs && make install); else (cd nodejs && make update); fi
if ! type bun >/dev/null 2>&1; then (cd bun && make install); else (cd bun && make update); fi

# good idea? or bad?
if ! type gemini >/dev/null 2>&1; then (cd gemini && make install); else (cd gemini && make update); fi
if ! type claude >/dev/null 2>&1; then (cd claude && make install); else (cd claude && make update); fi
if ! type codex >/dev/null 2>&1; then (cd codex && make install); else (cd codex && make update); fi
if ! type mistral >/dev/null 2>&1; then (cd mistral && make install); else (cd mistral && make update); fi
