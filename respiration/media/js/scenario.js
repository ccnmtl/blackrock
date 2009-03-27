/* module wrapper pattern*/
(function() {
   var global = this;
   var numScenarios = 1;
   var html = "";

   function initScenarioCloner() {
      html = $('scenario1').innerHTML;
      updateColors();
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
      // add handlers for the collapsing sections
      forEach(getElementsByTagAndClassName("div", "toggler", newDiv), function(elem) {
	        connect(elem, "onclick", toggle);
	});
	initYearHelper();
	//connect(newDiv.id + "-fieldstation", "onchange", updateYears);
	updateColors();
   }
   
   function delScenario(id) {
	   removeElement(id);
	   if(id == "scenario1") {
	     setSpeciesList([]);
	   }
   }
   
   function loadSpeciesData() {
      // load data from leaf mode
      
      // adjust percentages
   }
   
   addLoadEvent(initScenarioCloner);
   global.addScenario = addScenario;
   global.delScenario = delScenario;
})();