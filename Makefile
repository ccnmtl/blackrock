MANAGE=./manage.py
APP=blackrock
FLAKE8=./ve/bin/flake8

jenkins: ./ve/bin/python check test flake8

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

test: ./ve/bin/python
	$(MANAGE) jenkins --pep8-exclude=migrations --enable-coverage --coverage-rcfile=.coveragerc

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) --max-complexity=12

runserver: ./ve/bin/python check
	$(MANAGE) runserver

migrate: ./ve/bin/python check jenkins
	$(MANAGE) migrate

check: ./ve/bin/python
	$(MANAGE) check

jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint --config=.jshintrc media/js/admin.js media/js/local_session.js media/js/mammals media/js/optimization media/js/paleoecology media/js/respiration media/js/sampler

jscs: node_modules/jscs/bin/jscs
	./node_modules/jscs/bin/jscs media/js/admin.js media/js/local_session.js media/js/mammals media/js/optimization media/js/paleoecology media/js/respiration media/js/sampler

node_modules/jshint/bin/jshint:
	npm install jshint --prefix .

node_modules/jscs/bin/jscs:
	npm install jscs --prefix .


shell: ./ve/bin/python
	$(MANAGE) shell_plus

makemessages: ./ve/bin/python check jenkins
	$(MANAGE) makemessages -l es --ignore="ve" --ignore="login.html" --ignore="password*.html"
	$(MANAGE) compilemessages

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm -f celerybeat-schedule
	rm -rf .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make check
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make check
	make test
	make migrate
	make flake8

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python check jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate
