#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit
set -o pipefail
set -o nounset



# INIT WORKING DIR
# ======================================================================================================
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../
CWD="$(pwd)"


# ENV
# ======================================================================================================

export PYTHONUNBUFFERED=1
export PYTHONPATH="${CWD}"





# INIT COLOR HIGHLIGHTING
# ===================================================

RED='\033[0;31m'
RED_BG='\e[41m'
BLACK='\e[1;30m'
CYAN='\e[36m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

process_counter=0
function start_section() {
    process_counter=$((process_counter+1))
    echo -e "${BLUE}[STEP ${process_counter} : ${1}]${NC}"
}
function end_section() {
    COUNT_OF_ERRORS=$1

    if (( ${COUNT_OF_ERRORS} > 0))
    then
        echo -e "\n${RED_BG}${BLACK}  FAILED  ${NC}   ${1} errors found\n"
        exit 1
    fi
    echo -e "${GREEN}>> DONE without errors${NC}\n"
}



# SEARCH ALL PY FILES
# ===================================================

PY_FILES=`find ${CWD}/db_utils -type f -name "*.py" ! -path './.*' -not -path "**/migrations/*" -not -path "**/test_requests/*" -not -path "**/vendor/*"`
echo "$PY_FILES"



# RUN LINTING
# ===================================================

export PYTHONPATH=${CWD}

start_section "TYPE CHECKING : MYPY"
mypy --version --verbose
python3 -V
test -f ${CWD}/setup.cfg && echo "setup.cfg is file" || { echo "setup.cfg is not file"; exit 3; }
cd ${CWD}

#python3.6 -m mypy ${PY_FILES} --show-traceback | grep --color --ignore-case --extended-regexp ^[^:]+

set +e
MYPY_RESULT=$(mypy ${PY_FILES} --show-traceback --config-file="${CWD}/setup.cfg")
set -e

SAVEIFS=$IFS
IFS=$'\n'
MYPY_RESULT_LINES=(${MYPY_RESULT})
IFS=$SAVEIFS

MAX_LINES_COUNTER=0
ERROR_LINES_COUNTER=0
for (( i=0; i<${#MYPY_RESULT_LINES[@]}; i++ ))
do
    _LINE=${MYPY_RESULT_LINES[${i}]}

    HAS_FILE_IN_LINE=false
    {
        _UNUSED_VAR=$(echo ${_LINE} | egrep --color --ignore-case --extended-regexp ^[^:]+:.+)
    } && {
        if (( ${#_UNUSED_VAR} > 1 ))
        then
            echo ${_LINE} | grep --color --ignore-case --extended-regexp ^[^:]+
        else
            echo -e "${CYAN}>> ${_LINE}${NC}"
            ERROR_LINES_COUNTER=$((ERROR_LINES_COUNTER+1))

        fi
    } || {
        echo -e "${CYAN}>> ${_LINE}${NC}"
        ERROR_LINES_COUNTER=$((ERROR_LINES_COUNTER+1))
    }

    if (( ${#_LINE} > 1 ))
    then
        MAX_LINES_COUNTER=${i}
    fi
done

end_section ${ERROR_LINES_COUNTER}



start_section "LINTING PEP 8"
cd ${CWD}
pycodestyle $PY_FILES --max-line-length=158
end_section 0



start_section "LINTING FLAKE"
cd ${CWD}
flake8 $PY_FILES
end_section 0



start_section "LINTING PYLINT"
cd ${CWD}
python3.8 -m pylint --load-plugins pylint_flask_sqlalchemy --errors-only -j 4 **/*.py
end_section 0



#TEST_PY_FILES=`find . -type f -name "*__test.py" ! -path './.*' -not -path "**/pysmp/*"`
#echo "$TEST_PY_FILES"
#
#
#
#start_section "RUN UNIT TESTS"
#pytest --maxfail=1 -rf -l --cov=. --cov-report=term --cov-report=html:.var/test_coverage_html --cov-report=xml:.var/coverage.xml --junit-xml=.var/junit.xml ${TEST_PY_FILES}
#end_section 0



printf "${GREEN}DONE${NC}\n"
