init:
	pip install -e .

run:
ifndef ADDRESS
	echo "ADDRESS variable not passed"
	exit 1
endif
	PYTHONPATH=`pwd` python mobilium_server/server.py -a $(ADDRESS)
