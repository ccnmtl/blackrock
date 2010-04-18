var progress_indicator_id = ''

/* Generic Import Ajax */
function onImportSuccess(doc) {
    var json = JSON.parse(doc.responseText, null);
    var status = "";
    if (json.message)
        status = status + json.message + "<br />"
    if (json.deleted)
        status += json.deleted + " rows deleted. <br />"
    if (json.rowcount)
        status += json.rowcount + " rows imported <br />";
    $('import_status').innerHTML = status;
    $(progress_indicator_id).style.display = 'none';
}

function onImportError(err) {
     $('respiration_error').innerHTML = "An error occurred importing data (" + err + "). Please try again."
     $(progress_indicator_id).style.display = 'none';
}

function submitImportRequest(form, progress_id) {
    progress_indicator_id = progress_id;
    
    $('import_status').innerHTML = "";
    $('import_error').innerHTML = "";
    $(progress_indicator_id).style.display = 'none';
    
    var msg;
    var datePattern = /\d{2,4}-\d{1,2}-\d{1,2}/
    if (form.csvfile.value.length < 1) {
        msg = "<p>Please specify a csv file name.</p>";
    } 
    
    if (msg) {
        $('import_error').innerHTML = msg;
    } else {
        var params = {};
        for( var i = 0; i < form.elements.length; i++) {
            if (form.elements[i].type == "checkbox") {
                params[form.elements[i].name] = form.elements[i].checked;
            } else {
                params[form.elements[i].name] = escape(form.elements[i].value);
            }
        }
    
        deferred = doXHR(form.action, 
          { 
             method: 'POST', 
             sendContent: queryString(params),
             headers: {"Content-Type": "application/x-www-form-urlencoded"} 
          });
       deferred.addCallbacks(onImportSuccess, onImportError);  
       $(progress_indicator_id).style.display = 'block';   
    }
    return false; 
}


/* Respiration Forms -- */
function onSolrQuerySuccess(doc) {
    log('onSuccess');
    var json = JSON.parse(doc.responseText, null);
    var status = "";
    if (json.message)
        status = status + json.message + "<br />"
    if (json.deleted)
        status += json.deleted + " rows deleted. <br />"
    if (json.rowcount)
        status += json.rowcount + " rows imported <br />";
    $('respiration_status').innerHTML = status;
    $('progress_indicator').style.display = 'none';
}

function onSolrQueryError(err) {
    log('onError');
     $('respiration_error').innerHTML = "An error occurred importing data (" + err + "). Please try again."
     $('progress_indicator').style.display = 'none';
}

function submitSolrQuery(form) {     
    $('respiration_status').innerHTML = "";
    $('respiration_error').innerHTML = "";
    $('progress_indicator').style.display = 'none';
    
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
    
        deferred = doXHR(form.action, 
          { 
             method: 'POST', 
             sendContent: queryString(params),
             headers: {"Content-Type": "application/x-www-form-urlencoded"} 
          });
       deferred.addCallbacks(onSolrQuerySuccess, onSolrQueryError);  
       $('progress_indicator').style.display = 'block';   
    }
    return false; 
}
