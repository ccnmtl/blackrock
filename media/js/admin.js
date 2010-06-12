var original_request = null;

function verifyDate(str) {
    var datePattern = /\d{2,4}-\d{1,2}-\d{1,2}/
    return datePattern.test(str);    
}

function verifyTime(str) {
    var timePattern = /\d{1,2}:\d{1,2}:\d{1,2}/
    return timePattern.test(str)	
}

function submitSolrQuery(form) {
    $('solr_status').innerHTML = "";
    $('solr_error').innerHTML = "";
    $('solr_progress').style.display = 'none';
    
    var msg;
    if ($('id_solr_loader').last_import_date) {
        if ($('id_solr_loader').last_import_date.value && !verifyDate($('id_solr_loader').last_import_date.value)) {
            msg = "<p>Please enter a valid last import date.</p>";
        } else if ($('id_solr_loader').last_import_time.value && !verifyTime($('id_solr_loader').last_import_time.value)) {
            msg = "<p>Please enter a valid last import time.</p>";
        }
    }
    
    if (msg) {
        $('solr_error').innerHTML = msg;
    } else {
        params = {}
        if ($('id_solr_loader').last_import_date) {
            params[$('id_solr_loader').last_import_date.name] = escape($('id_solr_loader').last_import_date.value);
            params[$('id_solr_loader').last_import_time.name] = escape($('id_solr_loader').last_import_time.value);
        }
        params[$('id_solr_loader').application.name] = escape($('id_solr_loader').application.value)
        params[$('id_solr_loader').collection_id.name] = escape($('id_solr_loader').collection_id.value)
        params[$('id_solr_loader').import_set_type.name] = escape($('id_solr_loader').import_set_type.value)
        params[$('id_solr_loader').facet_field.name] = escape($('id_solr_loader').facet_field.value)
        params[$('id_solr_loader').import_set.name] = escape($('id_solr_loader').import_set.value)
        
        original_request = doXHR(form.action, 
          { 
             method: 'POST', 
             sendContent: queryString(params),
             headers: {"Content-Type": "application/x-www-form-urlencoded"} 
          });
       
       waitForResults();
       $('solr_progress').style.height = $('id_solr_loader').offsetHeight + "px";
       $('solr_progress').style.display = 'block';   
    }
    return false; 
}

function onWaitSuccess(doc) {
    var json = JSON.parse(doc.responseText, null);
    if (json['solr_complete']) {
        var status = "";
        if (json.solr_error)
            status = status + json.solr_error + "<br />"
        if (json.solr_created)
            status += json.solr_created + " rows created.<br />";
        if (json.solr_updated)
            status += json.solr_updated + " rows updated.<br />";
        if (json.solr_import_date)
            if ($('id_solr_loader').last_import_date)
                $('id_last_import_date').value = json.solr_import_date;
        if (json.solr_import_time)
            $('id_last_import_time').value = json.solr_import_time;    
        
        $('solr_status').innerHTML = status;
        $('solr_progress').style.display = 'none';
        
        try {
           original_request.cancel();
        } catch (e) {}
    } else {
        setTimeout(waitForResults, 30000 /* ..after 30 seconds */);
    }
}

function onWaitError(err) {
     $('solr_error').innerHTML = "An error occurred importing data (" + err + "). Please try again."
     $('solr_progress').style.display = 'none';
     
     try {
         original_request.cancel(); 
      } catch (e) {}
}

function waitForResults() {
    url = 'http://' + location.hostname + ':' + location.port + "/blackrock_main/loadsolrpoll";   
    deferred = doXHR(url, { method: 'GET' });
    deferred.addCallbacks(onWaitSuccess, onWaitError);
}

function onPreviewSuccess(doc) {
    var json = JSON.parse(doc.responseText, null);
   
    var count = 0;
    var sets = ""
    for (import_set in json['sets']) {
        count++;
        if (sets.length < 1)
            sets = "<tr><td><b>Import Set</b></td><td><b>Rows To Retrieve</b></td></tr>";
        sets += "<tr><td>" + import_set + "</td><td>" + json['sets'][import_set] + "</td></tr>";
    }
    
    $('previewsolr').innerHTML = sets;
    
    if (!json['last_import_date']) {
        $('no_last_import_date').style.display = 'block';
    } else {
        $('id_last_import_date').value = json['last_import_date'];
        $('id_last_import_time').value = json['last_import_time'];    
    
        if (count < 1) {
            $('no_data_to_import').style.display = 'block';
        } else {
            $('id_last_import_datetime').innerHTML = '<b>' + json['last_import_date'] + " " + json['last_import_time'] + "</b>";
            $('yes_last_import_date').style.display = 'block';
        }
    }
}

function onPreviewError(err) {
    alert(err);
}

function previewSolr() {
    $('no_data_to_import').style.display = 'none';
    $('no_last_import_date').style.display = 'none';
    $('yes_last_import_date').style.display = 'none';
    
    var params = {};
    if ($('id_solr_loader').last_import_date && $('id_solr_loader').last_import_date.value) { 
        params[$('id_solr_loader').last_import_date.name] = escape($('id_solr_loader').last_import_date.value);
        params[$('id_solr_loader').last_import_time.name] = escape($('id_solr_loader').last_import_time.value);
    }
    params[$('id_solr_loader').application.name] = escape($('id_solr_loader').application.value)
    params[$('id_solr_loader').collection_id.name] = escape($('id_solr_loader').collection_id.value)
    params[$('id_solr_loader').import_set_type.name] = escape($('id_solr_loader').import_set_type.value)
    params[$('id_solr_loader').facet_field.name] = escape($('id_solr_loader').facet_field.value)
    params[$('id_solr_loader').import_set.name] = escape($('id_solr_loader').import_set.value)
    
    url = 'http://' + location.hostname + ':' + location.port + "/blackrock_main/previewsolr"
    deferred = doXHR(url, { method: 'POST',
                            sendContent: queryString(params),
                            headers: {"Content-Type": "application/x-www-form-urlencoded"} 
                            });
    deferred.addCallbacks(onPreviewSuccess, onPreviewError);
    return false;
}


