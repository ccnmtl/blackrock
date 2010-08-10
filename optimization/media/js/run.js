var global_http_request;

function getcsv() {
  if(! global_http_request) {
    return false;
  }
  $("csvform").submit();
}

function showResults(http_request) {
  global_http_request = http_request;

  var results = evalJSON(http_request.responseText);
  var summary = [
      results['input']['num_plots'],
      results['input']['shape'],
      results['input']['size'],
      results['input']['arrangement'],
      results['sample-area'],
      results['sample-time'],
      results['avg-time'],
      results['sample-variance-density'],
      results['sample-variance-basal']
  ];
  var run_num = 0;
  if (window.SampleStorage) {
      run_num = SampleStorage.addSample(summary, results) +1;
  }

  showResultsInfo(results, 
                  addSampleSummaryRow(run_num, summary));

  setStyle('waitmessage', {'display':'none'});
  $('calculate').disabled = false; 

}

var cur_results = false;
function showResultsInfo(results, new_row) {
    if (window.console)
        console.log(results);
    if (cur_results) {
        removeElementClass(cur_results,'sample-enabled');
    }
    if (new_row) {
        addElementClass(new_row,'sample-enabled');
        cur_results = new_row;
    }
    if (!results) {return};
    ///Summary table deprecated
    //$('results-time').innerHTML = results['sample-time'];
    //$('results-avg-time').innerHTML = results['avg-time'];
    //$('results-variance-density').innerHTML = results['sample-variance-density'];
    //$('results-variance-basal').innerHTML = results['sample-variance-basal'];

  // store in form for CSV export
  $('form-results').value = serializeJSON(results);
  $('csvbutton').disabled = false;

  $('results-area').innerHTML = results['sample-area'];
  $('results-species').innerHTML = results['sample-species'];
  $('results-count').innerHTML = results['sample-count'];
  $('results-dbh').innerHTML = results['sample-dbh'];
  $('results-variance-dbh').innerHTML = results['sample-variance-dbh'];
  $('results-density').innerHTML = results['sample-density'];
  $('results-basal').innerHTML = results['sample-basal'];

  $('actual-area').innerHTML = results['actual-area'];
  $('actual-species').innerHTML = results['actual-species'];
  $('actual-count').innerHTML = results['actual-count'];
  $('actual-dbh').innerHTML = results['actual-dbh'];
  $('actual-variance-dbh').innerHTML = results['actual-variance-dbh'];
  $('actual-density').innerHTML = results['actual-density'];
  $('actual-basal').innerHTML = results['actual-basal'];
  
  $('comparison-area').innerHTML = results['comparison-area'];
  $('comparison-species').innerHTML = results['comparison-species'];
  $('comparison-count').innerHTML = results['comparison-count'];
  $('comparison-dbh').innerHTML = results['comparison-dbh'];
  $('comparison-variance-dbh').innerHTML = results['comparison-variance-dbh'];
  $('comparison-density').innerHTML = results['comparison-density'];
  $('comparison-basal').innerHTML = results['comparison-basal'];
  visualized_map = new SampleMap({id:'results-map',
				  bounds:results.sample.bounds,
                                  onSelect:function(e) {
                                      document.location = '#plot'+e.feature.plotname;
                                  },
                                  onHover:function(e) {
                                      $('map-select-plot').innerHTML = 'Plot '+e.feature.plotname;
                                      //console.log(e.feature.plotname);
                                  }
				 });
  // individual plots
  var plots = results['plots'];
  var numPlots = plots.length || dictlen(plots); //legacy
  $('plot-parent').innerHTML = '';
  for(var i=0; i<numPlots; i++) {
      var plotname = i+1;
      showPlotInfo(plotname, plots[i]);
      visualized_map.addPlot(plots[i], plotname);
  }
  showElement('results');
  setStyle('details', {'display':'block'});

}

function dictlen(d) {
    var len = 0;
    for (a in d) len++;
    return len;
}

function showError(http_request) {
    global_http_request = http_request;
    log(http_request);
    var custom = '';
    try {
	var json = evalJSON(http_request.req.responseText);
	custom = json.error || '';
    } catch(e) {/*pass*/}
    $('customerror').innerHTML = custom;

    showElement('errormessage');
    hideElement('waitmessage');
    Highlight('errormessage',{startcolor:'#ffff99'});
    $('calculate').disabled = false; 
}

function showPlotInfo(plotNumber, results) {
  var parent = $('plot-parent'); 
  var plotTable = $('plot-template').innerHTML;
  var id = "plot" + plotNumber;
  var name = "PLOT " + plotNumber;

  if(plotNumber > 0) {
    var newDiv = DIV();
    addElementClass(newDiv, "plot-wrapper");
    addElementClass(newDiv, "toggle-container");
    appendChildNodes(parent, newDiv);
    newDiv.innerHTML = plotTable.replace(/plot1/g, id).replace(/PLOT 1/g, name);
    newDiv.id = id;
    forEach(getElementsByTagAndClassName("tr","calculated",newDiv), function(elem) {
      removeElement(elem);
    });
  }
  $(id+'-area').innerHTML = results['area'];
  $(id+'-time-total').innerHTML = results['time-total'];
  $(id+'-time-travel').innerHTML = results['time-travel'];
  $(id+'-time-locate').innerHTML = results['time-locate'];
  $(id+'-time-establish').innerHTML = results['time-establish'];
  $(id+'-time-measure').innerHTML = results['time-measure'];
  $(id+'-species').innerHTML = results['num-species'];
  $(id+'-count').innerHTML = results['count'];
  $(id+'-details-count').innerHTML = results['count'];
  $(id+'-dbh').innerHTML = results['dbh'];
  $(id+'-variance-dbh').innerHTML = results['variance-dbh'];
  $(id+'-density').innerHTML = results['density'];
  $(id+'-basal').innerHTML = results['basal'];
  
  var numSpecies = results['num-species'];
  var speciesList = results['species-totals'];
  var totalsRow = getFirstElementByTagAndClassName("TR", null, id+'-species-table');
  for(var i=0; i<numSpecies; i++) {
    var child = TR({'class':'calculated'}, TD(null, speciesList[i]['name']),
                         TD({'class':'right'}, speciesList[i]['count']),
                         TD({'class':'right'}, speciesList[i]['dbh']),
                         TD({'class':'right'}, speciesList[i]['variance-dbh']),
                         TD({'class':'right'}, speciesList[i]['density']),
                         TD({'class':'right'}, speciesList[i]['basal'])
                   );
    insertSiblingNodesBefore(totalsRow, child);
  }
  if(plotNumber > 0) {
    var togglectrl = getFirstElementByTagAndClassName("*", "toggle-control", id);
    connect(togglectrl, "onclick", toggle);
  }
}

function reset() {
  setStyle('errormessage', {'display':'none'});
  setStyle('waitmessage', {'display':'none'});
  setStyle('results', {'display':'none'});
  setStyle('details', {'display':'none'});
  updateShapeLabel($("plotArrangement"));
  $('csvbutton').disabled = true;
  $('form-results').value = "";
  if(global_http_request) {
    global_http_request.cancel();
  }
  
  forEach(getElementsByTagAndClassName("div","plot-wrapper"), function(elem) {
    if(elem.id != "plot-template")
      removeElement(elem);
  });

  /* collapse plot1 if it's un-collapsed */
  var rightarrow = getFirstElementByTagAndClassName("span", "rightarrow", "plot-template");
  var downarrow = getFirstElementByTagAndClassName("span", "downarrow", "plot-template");
  var parent = $("plot-template");
  var inner = getFirstElementByTagAndClassName("div", "toggle-nest", parent);

  var visible = (getStyle(downarrow, "display") != "none");

  if(visible) {
    setStyle(downarrow, {'display':'none'});
    setStyle(rightarrow, {'display':'inline'});
    setStyle(inner, {'display':'none'});
  }

}

function validate() {
  // validate number of plots
  var numPlots = $('numPlots').value;
  if(numPlots == "" || isNaN(numPlots)) {
    alert("Error: Number of Plots must be a number.  Please check your input and try again.");
    return false;
  }
  if(numPlots < 1 || numPlots > 100) {
    alert("Error: Number of Plots must be between 1 and 100.  Please check your input and try again.");
    return false;
  }
  if(numPlots.indexOf(".") != -1) {
    alert("Error: Number of Plots must be a whole number.  Please check your input and try again.");
    return false;
  }
  
  // validate plot dimensions
  var size = $('plotSize').value;
  var label = $('shapeLabel').innerHTML;
  if(size == "" || isNaN(size)) {
    alert("Error: Plot " + label + " must be a number.  Please check your input and try again.");
    return false;
  }
  if(size < 1 || size > 100) {
    alert("Error: Plot " + label + " must be between 1 and 100.  Please check your input and try again.");
    return false;
  }
  if(size.indexOf(".") != -1) {
    alert("Error: Plot " + label + " must be a whole number.  Please check your input and try again.");
    return false;
  }  
  
  return true;
}

function calculate() {
  if(! validate()) { return false; }
  $('csvbutton').disabled = true;
  $('form-results').value = "";

  $('calculate').disabled = true;
  setStyle('waitmessage', {'display':'block'});
  setStyle('errormessage', {'display':'none'});

  forEach(getElementsByTagAndClassName("div","plot-wrapper"), function(elem) {
    if(elem.id != "plot-template")
      removeElement(elem);
  });
  
  /* collapse plot-template if it's un-collapsed */
  var rightarrow = getFirstElementByTagAndClassName("span", "rightarrow", "plot-template");
  var downarrow = getFirstElementByTagAndClassName("span", "downarrow", "plot-template");
  var parent = $("plot-template");
  var inner = getFirstElementByTagAndClassName("div", "toggle-nest", parent);

  var visible = (getStyle(downarrow, "display") != "none");

  if(visible) {
    setStyle(downarrow, {'display':'none'});
    setStyle(rightarrow, {'display':'inline'});
    setStyle(inner, {'display':'none'});
  }

  forEach(getElementsByTagAndClassName("tr","calculated"), function(elem){
    removeElement(elem);
  });

  
  global_http_request = doXHR("calculate", {
          'method':'POST', 
          'sendContent':queryString(document.forms['runform']),
          'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
      });
  global_http_request.addCallback(showResults);
  global_http_request.addErrback(showError);
}

function updateShapeLabel(e) {
  var shape = "square";
  if(e.src)
    shape = e.src().value;
  else
    shape = e.value;

  if(shape == "square") {
    $('shapeLabel').innerHTML = "Edge";
  }
  else {
    $('shapeLabel').innerHTML = "Radius";
  }
}

function deleteSample(run_num) {
    SampleStorage.deleteSample(run_num-1);
    removeElement('samplerun-'+run_num);
}

function addSampleSummaryRow(run_num, summary_ary) {
    var tr = document.createElement('tr');
    tr.id = 'samplerun-'+run_num;
    var html = '<td>'+run_num+' <a href="#top" '
        +'onclick="deleteSample('+run_num+');return false;">x</a></td>';
    for (var i=0;i<summary_ary.length;i++) {
        html += '<td>'+summary_ary[i]+'</td>';
    }
    dom_prepend($('sample-list'),tr);
    tr.innerHTML = html;
    connect(tr, 'onclick', function(evt) {
        showResultsInfo(SampleStorage.getSample(run_num-1), tr);
    });
    return tr;
}

function dom_prepend(parent, newchild) {
    if (parent.firstChild)
        parent.insertBefore(newchild, parent.firstChild)
    else
        parent.appendChild(newchild);
}

function loadSampleHistory() {
    if (SampleStorage) {
        var ss = SampleStorage.samples;
        for (var i=0;i<ss.length;i++) 
            if (ss[i])
                addSampleSummaryRow(i+1, ss[i]);
    }
}

function initRun() {
  connect("calculate", "onclick", calculate);
  connect("reset", "onclick", reset);
  connect("plotShape", "onchange", updateShapeLabel);
  $('csvbutton').disabled = true;
  $('calculate').disabled = false; 
  loadSampleHistory();
}

addLoadEvent(initRun);

TableSortCasts["human_time"] = function(cell) {
    var time=0;
    var str = String(cell.innerHTML);
    var min = str.match(/([.\d]+) min/);
    var hr = str.match(/([.\d]+) hr/);
    if (min) time += parseFloat(min[1]);
    if (hr) time += 60*parseFloat(hr[1]);
    return time;
}