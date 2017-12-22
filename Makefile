APP=blackrock

#JS_FILES=media/js/admin.js media/js/local_session.js media/js/mammals media/js/optimization media/js/paleoecology media/js/respiration media/js/sampler media/js/portal
# most of the JS in blackrock is still not nearly jshint or jscs clean. until then, we still
# want to run against something.
JS_FILES=media/js/paleoecology/explore.js media/js/src media/js/respiration/ media/js/optimization media/js/portal/blackrock_webca.js media/js/portal/maps.js media/js/portal/object_detail.js media/js/portal/photogallery.js media/js/portal/portal.js

MAX_COMPLEXITY=7

all: jenkins

include *.mk

makemessages: check jenkins
	$(MANAGE) makemessages -l es --ignore="ve" --ignore="login.html" --ignore="password*.html"
	$(MANAGE) compilemessages

.PHONY: makemessages
