#!/bin/bash

type bun | cd bun && make install && cd -
cd gemini && make install && cd -
cd claude && make install && cd -
cd codex && make install && cd -
cd mistral && make install && cd -