#!/bin/bash
# see uv_fix_
# https://discuss.python.org/t/information-for-python-users-regarding-emudhra-emsign-ca-certificate-security-incident/109576
# fdfind -H -I -t d -g .venv ~/dev ~/projects ~/uv_venvs | tee venv-list.txt
# usage: ./uv_fix_venvs.sh venv-list.txt
# one .venv path per line
set -u
list=${1:?venv list file}
pip_spec='pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70'
while IFS= read -r venv || [[ -n ${venv:-} ]]; do
  [[ -z $venv || $venv == \#* ]] && continue
  py=$venv/bin/python
  echo "== $py"
  "$py" -m pip install "$pip_spec"
  "$py" -m pip install --upgrade certifi
done < "$list"
