If you modify the SOLR configuration, the following steps should update everything:


settings:
    staging:
        REMOTE_USER=tlcreg
        REMOTE_HOST=cardamom.cc.columbia.edu
        PATH_TO_CCNMTL_TOMCAT=/www/apps/tomcat5/wwwappdev/ccnmtl
        PATH_TO_SCHEMA_FILE=solr/solrhome/blackrock_portal/conf/schema.xml
        SETTINGS=settings_stage
        
    prod:
        REMOTE_USER=tlcreg
        REMOTE_HOST=huckleberry.cc.columbia.edu
        PATH_TO_CCNMTL_TOMCAT=/www/apps/tomcat5/wwwapp/ccnmtl
        PATH_TO_SCHEMA_FILE=solr/solrhome/blackrock_portal/conf/schema.xml
        SETTINGS=settings_production


regerate the index file
    ./manage.py build_solr_schema   --settings=$SETTINGS > new_schema.xml

replace the schema file on the solr server with the new schema file:
     scp new_schema.xml $REMOTE_USER@$REMOTE_HOST:$PATH_TO_CCNMTL_TOMCAT/$PATH_TO_SCHEMA_FILE

double-check permissions:
    $ ls -lart schema.xml
    -rwxrwxr--  1 tlcreg tlcxml 8945 Apr 10 13:11 schema.xml

restart the server
    ssh $REMOTE_USER@$REMOTE_USER@$REMOTE_HOST 'sudo /etc/init.d/tomcat-ccnmtl5 restart'

wait a good long while
    rebuilding the index will break if the server isn't back up yet.

rebuild the index:
    ./manage.py rebuild_index  --settings=$SETTINGS
    Accept changes, etc.
    
nota bene:
    Restart the server and rebuild the index may have to be done twice. Not sure exactly.
