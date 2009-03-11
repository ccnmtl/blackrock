/* module wrapper pattern*/
(function() {
   var global = this;
   var numScenarios = 1;
   var html = "";

   function initScenarioCloner() {
      html = $('scenario1').innerHTML;
   }

   function addScenario() {
      var newDiv = DIV();
      addElementClass(newDiv, "scenario");
	   appendChildNodes("scenariobox", newDiv);
	   numScenarios++;
	   incNumSpecies();
	   newDiv.innerHTML = html.replace(/scenario1/g, "scenario" + numScenarios);
	   newDiv.innerHTML = newDiv.innerHTML.replace(/species1/g, "species" + getNumSpecies());
	   newDiv.innerHTML = newDiv.innerHTML.replace(/Your Tree \#1/g, "Your Tree #" + getNumSpecies());
	   newDiv.id = "scenario" + numScenarios;
	   var namediv = getFirstElementByTagAndClassName("input", "scenario-name", newDiv);
	   namediv.value = "Scenario " + numScenarios;
	   forEach(getElementsByTagAndClassName("div", "species", newDiv), function(elem) {
	      global.EquationHighlighter.initSpecies(elem);
	   });
      forEach(getElementsByTagAndClassName("div", "toggler", newDiv), function(elem) {
	        connect(elem, "onclick", toggle);
	});
   }
   
   function delScenario(id) {
	   removeElement(id);
	   numScenarios--;
   }
   
   function loadSpeciesData() {
      // load data from leaf mode
      
      // adjust percentages
   }
   
   addLoadEvent(initScenarioCloner);
   //addLoadEvent(setDefaults);
   global.addScenario = addScenario;
   global.delScenario = delScenario;

    function setDefaults() {
      return;
	$('species1-name').value = "Your Tree #1";
	$('species1-R0').value = 0.84;
	$('species1-E0').value = 27210;
	
	addSpecies();
	$('species2-name').value = "Your Tree #2";
	$('species2-R0').value = 0.86;
	$('species2-E0').value = 40073;
    }

  // overrides original from species.js
  function addSpecies(elem) {
    alert("called");
    if(! elem) {
      var scenario = document;
      newID = "scenario1-species" + numSpecies;
    }
    else {
      // get scenario, if there is one
      var scenario = getFirstParentByTagAndClassName(elem, "div", "scenario");
      if(! scenario) {
        scenario = document;
	    newID = "species" + numSpecies;
	  }
      else {
	  newID = scenario.id + "-species" + numSpecies;
      }
    }
    var parent = getFirstElementByTagAndClassName("div", "speciescontainer", scenario);
    var newDiv = DIV();
    addElementClass(newDiv, "species");
    appendChildNodes(parent, newDiv);
    numSpecies++;
    newDiv.innerHTML = html.replace(/species1/g, "species" + numSpecies);
    newDiv.id = newID;
    var namediv = getFirstElementByTagAndClassName("input", "species-name", newDiv);
    namediv.value = "Your Tree #" + numSpecies;
    global.EquationHighlighter.initSpecies(newDiv);
  }
  //global.addSpecies = addSpecies;
  //global.setDefaults = setDefaults;
  //addLoadEvent(setDefaults);

})();