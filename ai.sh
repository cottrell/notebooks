#!/bin/bash

type npm | cd npm && make install && cd -
type bun | cd bun && make install && cd -

# good idea? or bad?
cd npm && make update && cd -
cd bun && make update && cd -

cd gemini && make install && cd -
cd claude && make install && cd -
cd codex && make install && cd -
cd mistral && make install && cd -
