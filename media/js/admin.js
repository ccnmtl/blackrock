var original_request = null;
var poll_url = null;

function onQueryError(err) {
    log('onError');
     $('respiration_error').innerHTML = "An error occurred importing data (" + err + "). Please try again."
     $('solr_progress').style.display = 'none';
}

function submitSolrQuery(form) {     
    $('respiration_status').innerHTML = "";
    $('respiration_error').innerHTML = "";
    $('solr_progress').style.display = 'none';
    
    var msg;
    var datePattern = /\d{2,4}-\d{1,2}-\d{1,2}/
    if (form.base_query.value.length < 1) {
        msg = "<p>Please enter a base Solr query.</p>";
    } else if (form.import_set.value.length > 0 && form.delete_data.checked && form.station.value == 'All') {
        // don't let anyone do anything stupid.
        if (!confirm("You're only importing one set of data. Are you sure you want to delete All data?"))
            return false;
    } else if (form.delete_data.checked) {
        if ((datePattern.test(form.start_date.value) && !datePattern.test(form.end_date.value)) ||
            (!datePattern.test(form.start_date.value) && datePattern.test(form.end_date.value)))    
        msg = "<p>When specifying dates, both must be valid. Format: yyyy-mm-dd</p>";
    } 
    
    if (msg) {
        $('respiration_error').innerHTML = msg;
    } else {
        var params = {};
        for( var i = 0; i < form.elements.length; i++) {
            if (form.elements[i].type == "checkbox") {
                params[form.elements[i].name] = form.elements[i].checked;
            } else {
                params[form.elements[i].name] = escape(form.elements[i].value);
            }
        }
        
        original_request = doXHR(form.action, 
          { 
             method: 'POST', 
             sendContent: queryString(params),
             headers: {"Content-Type": "application/x-www-form-urlencoded"} 
          });
       original_request.addErrback(onQueryError);
       poll_url = form.action + 'poll' 
       
       waitForResults();
       $('solr_progress').style.display = 'block';   
    }
    return false; 
}

function onWaitSuccess(doc) {
    log('onWaitSuccess')
    var json = JSON.parse(doc.responseText, null);
    if (json['solr_complete']) {
        var status = "";
        if (json.solr_error)
            status = status + json.solr_error + "<br />"
        if (json.solr_deleted)
            status += json.solr_deleted + " rows deleted. <br />"
        if (json.solr_rowcount)
            status += json.solr_rowcount + " rows imported <br />";
        $('respiration_status').innerHTML = status;
        $('solr_progress').style.display = 'none';
        
        try {
           original_request.cancel();
        } catch (e) {
           log('Cancelling original request error: ' + e);
        }
    } else {
        setTimeout(waitForResults, 30000 /* ..after 30 seconds */);
    }
}

function waitForResults() {
    log('waitForResults')
    deferred = doXHR(poll_url, { method: 'GET' });
    deferred.addCallbacks(onWaitSuccess, onQueryError);
}

