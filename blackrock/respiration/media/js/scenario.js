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
       newDiv.innerHTML = html.replace(/scenario1/g, "scenario" + numScenarios);
       newDiv.id = "scenario" + numScenarios;
       var namediv = getFirstElementByTagAndClassName("input", "scenario-name", newDiv);
       namediv.value = "Scenario " + numScenarios;
       forEach(getElementsByTagAndClassName("div", "species", newDiv), function(elem) {
          incNumSpecies();
          var n = getNumSpecies();
          elem.id = "species" + n;
          elem.innerHTML = elem.innerHTML.replace(/species\d/g, elem.id);
          elem.innerHTML = elem.innerHTML.replace(/Your Tree \#\d/g, "Your Tree #" + n);
          global.EquationHighlighter.initSpecies(elem);
       });
       
       // add handlers for the collapsing sections
       forEach(getElementsByTagAndClassName("div", "toggler", newDiv), function(elem) {
           connect(elem, "onclick", toggle);
    });
    initYearHelper();
    updateColors();
   }
   
   function delScenario(id) {
       removeElement(id);
       if(id == "scenario1") {
         setSpeciesList([]);
       }
   }
   
   function initScenarioModule() {
       initScenarioCloner();
   }
   
   function getNumScenarios() {
       return numScenarios;
   }
   
   global.addScenario = addScenario;
   global.delScenario = delScenario;
   global.initScenarioModule = initScenarioModule;
   global.getNumScenarios = getNumScenarios;
})();