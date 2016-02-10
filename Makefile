APP=blackrock

#JS_FILES=media/js/admin.js media/js/local_session.js media/js/mammals media/js/optimization media/js/paleoecology media/js/respiration media/js/sampler media/js/portal
# most of the JS in blackrock is still not nearly jshint or jscs clean. until then, we still
# want to run against something.
JS_FILES=media/js/paleoecology/explore.js

MAX_COMPLEXITY=8

all: jenkins

include *.mk

makemessages: check jenkins
	$(MANAGE) makemessages -l es --ignore="ve" --ignore="login.html" --ignore="password*.html"
	$(MANAGE) compilemessages
