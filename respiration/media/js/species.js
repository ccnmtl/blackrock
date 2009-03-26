/* module wrapper pattern*/
(function() {
    var global = this;
    
    var numSpecies = 1;
    var scenario1Species = ["species1"];
    var html = "";
    function initSpeciesCloner() {
    	html = $('species1').innerHTML;
    }
    
    function addSpecies(elem) {
      numSpecies++;
      if($("numspecies")) {
        $("numspecies").value = numSpecies;
      }
      //$("numspecies").value = numSpecies;
      if(! elem) {
        var scenario = document;
      }
      else {
        // get scenario, if there is one
        var scenario = getFirstParentByTagAndClassName(elem, "div", "scenario");
        if(! scenario) {
          scenario = document;
        }
        else if(scenario.id == "scenario1") {
          scenario1Species.push("species" + numSpecies);
        }
      }
      var parent = getFirstElementByTagAndClassName("div", "speciescontainer", scenario);
      var newDiv = DIV();
      addElementClass(newDiv, "species");
      appendChildNodes(parent, newDiv);
      newDiv.innerHTML = html.replace(/species1/g, "species" + numSpecies);
      newDiv.id = "species" + numSpecies;
      var namediv = getFirstElementByTagAndClassName("input", "species-name", newDiv);
      namediv.value = "Your Tree #" + numSpecies;
      global.EquationHighlighter.initSpecies(newDiv);
      updateColors();
    }
    
    
    function initSpecies() {
      if($("scenario1-base-temp")) {
        $("scenario1-base-temp").value = $("leaf-base-temp").value;
      }
      else {
        $("base-temp").value = $("leaf-base-temp").value;
      }
      var leafSpecies = $("leaf-numspecies").value;
      scenario1Species = ["species1"];
      for(var i=1; i<=leafSpecies; i++) {
        if(i > 1) {
          addSpecies();
          scenario1Species.push("species"+i);
        }
        $('species'+i+'-name').value = $('leaf-species'+i+'-name').value;
        $('species'+i+'-R0').value = $('leaf-species'+i+'-R0').value;
        $('species'+i+'-E0').value = $('leaf-species'+i+'-E0').value;
      }
      if(leafSpecies == 0) {setDefaults(); }
    }

    function setDefaults() {
      $('species1-name').value = "Your Tree #1";
      $('species1-R0').value = 0; /*0.84*/
      $('species1-E0').value = 0; /*27210*/

      addSpecies();
      $('species2-name').value = "Your Tree #2";
      $('species2-R0').value = 0;/*0.86*/
      $('species2-E0').value = 0;/*40073*/

      if($('species1-percent')) {
        $('species1-percent').value = 0;/*50*/
      }
      if($('species2-percent')) {
        $('species2-percent').value = 0;/*50*/
      }
    }
    
    function delSpecies(id) {
      //numSpecies--;  // do not reuse species IDs
      removeElement(id);
      // remove from scenario1 array if it exists
      if(scenario1Species.indexOf(id) != -1) { 
        scenario1Species.splice(scenario1Species.indexOf(id), 1);
      }
    }

    function EquationHighlighter() {
	connect(window,'onload',this,'onLoad');
	this.vars = {"e-zero":[],
		     "r-g":[],
		     "t-zero":[],
		     "t-a":[],
		     "r-zero":[],
		     "r-result":[]
		    };
	this.current = [];
    }
    EquationHighlighter.prototype.onLoad = function() {
	var self = this;
	this.arrhenius_vars = getElementsByTagAndClassName(null,'arr-variable','equation');
	for (a in self.vars) {
	    connect('arr-'+a,'onmouseenter',bind(self.hiliteFields,self,a));
	    connect('arr-'+a,'onmouseleave',bind(self.unHiliteFields,self,a));
	    forEach(getElementsByTagAndClassName(null,a),function(elt) {
		connect(elt,'onfocus',bind(self.hiliteVar,self,a,addElementClass));
		connect(elt,'onblur',bind(self.hiliteVar,self,a,removeElementClass));
		if($("plotGraph") != null) {
		  connect(elt,'onchange',self.needsUpdate);
		}
	    });
	}
    }
    EquationHighlighter.prototype.needsUpdate = function() {
	//addElementClass('plotGraph','needsupdate');
	leafGraph();
	global.TemperatureSliders.updateCursorVals();
    }
    EquationHighlighter.prototype.initSpecies = function(elt) {
	var self = this;
	e_zero = getFirstElementByTagAndClassName(null,"e-zero",elt);
	r_zero = getFirstElementByTagAndClassName(null,"r-zero",elt);
	connect(e_zero,'onfocus',function(){self.hiliteVar("e-zero");});
	connect(r_zero,'onfocus',function(){self.hiliteVar("r-zero");});
	if($("plotGraph") != null) {
	  connect(e_zero,'onchange',self.needsUpdate);
	  connect(r_zero,'onchange',self.needsUpdate);
	}
    }
    EquationHighlighter.prototype.hiliteVar = function(arr_var,select_func) {
	var self = this;
	forEach(self.arrhenius_vars,function(elt) {
	    removeElementClass(elt,'selected');
	});
	select_func = (select_func)?select_func:addElementClass;
	select_func('arr-'+arr_var,'selected');
    }
    EquationHighlighter.prototype.hiliteFields = function(arr_var) {
	var self = this;
	self.curr = getElementsByTagAndClassName(null,arr_var);
	forEach(self.curr,function(elt) {
	    addElementClass(elt,'selected');
	});
	self.hiliteVar(arr_var);
    }
    EquationHighlighter.prototype.unHiliteFields = function(arr_var) {
	var self = this;
	forEach(self.curr,function(elt) {
	    removeElementClass(elt,'selected');
	});
    }

    function TemperatureSliders() {
	connect(window,'onload',this,'onLoad');
	this.low=null;
	this.high=null;
	this.MAX_TEMP = 45;
	this.MIN_TEMP_WIDTH = 10;
	this.length=null;
	this.margin = 25;
	this.graph_left_margin = 40;
	this.graph_right_margin = 2;
	this.freeze = false;
    }
    TemperatureSliders.prototype.onLoad = function() {
	var self = this;
	if(!$('temp-slider')) { return; }
	try {
  	  var sliders = getElementsByTagAndClassName(null,'slider','temp-slider');
  	}
  	catch(err) {
  	  return;  // no sliders; don't initialize this part
  	}
	this.input_low = $('temp_low');
	this.input_high = $('temp_high');
	this.low = Number(this.input_low.value);
	this.high = Number(this.input_high.value);

	this.length = getElementDimensions(sliders[0].parentNode).w - this.margin;
	//length2temp:divide ; temp2length:multiply
	this.conv = this.length/this.MAX_TEMP;
	this.MIN_WIDTH = this.MIN_TEMP_WIDTH * this.conv;

	this.canvas = getElement('graph');
	this.graph_cursor = getElement('graph-cursor');
	this.canvas_length = getElementDimensions(this.canvas).w-this.graph_left_margin-this.graph_right_margin;

	/// Temperature Sliders
	connect(this.input_low,'onchange',function(){self.low = self.input_low.value;
						     self.update('input_low')});
	connect(this.input_high,'onchange',function(){self.high = self.input_high.value;
						      self.update('input_high')});
	this.drag_low = Draggable(sliders[0],{snap:bind(this.lowSnap,this),
					      onchange:bind(this.update,this,'drag_low'),
					      revert:global.EquationHighlighter.needsUpdate
					     });
	this.drag_high = Draggable(sliders[1],{snap:bind(this.highSnap,this),
					       onchange:bind(this.update,this,'drag_high'),
					       revert:global.EquationHighlighter.needsUpdate
					      });

	this.drag_range = Draggable(sliders[2],{snap:bind(this.rangeSnap,this),
						onchange:bind(this.update,this,'drag_range'),
						revert:global.EquationHighlighter.needsUpdate
					       });

	/// Graph Mouse Cursor
	connect(this.canvas,'onmousemove',this,'graphCursor');
	connect(this.canvas,'onclick',this,'setCursorFreeze');
	connect('unfreeze','onclick',this,'setCursorFreeze');


	this.update('do all of them');
	global.EquationHighlighter.needsUpdate();
    }
    TemperatureSliders.prototype.lowSnap = function(x,y) {
	x = Math.min(x,this.length-this.MIN_WIDTH);
	x = Math.max(x,0);
	this.low = x/this.conv; //math
	this.high = Math.max(this.high,(x+this.MIN_WIDTH)/this.conv); //math
	return [x,0];
    }
    TemperatureSliders.prototype.highSnap = function(x,y) {
	x = Math.min(x,this.length);
	x = Math.max(x,this.MIN_WIDTH);
	this.low = Math.min(this.low,(x-this.MIN_WIDTH)/this.conv); //math
	this.high = x/this.conv; //math
	return [x,0];
    }
    TemperatureSliders.prototype.rangeSnap = function(x,y) {
	var range = this.high - this.low;
	x = Math.min(x,this.length - range*this.conv);
	var low_coords = this.lowSnap(x,y);
	this.high = this.low + range;
	low_coords[1] = 8; //match #temp-slider .range in CSS
	return low_coords;
    }

    TemperatureSliders.prototype.update = function(not_me) {
	var self = this;
	var plans = {
	    'input_low':function(){self.input_low.value = String(self.low).substr(0,4);},//2 decimals
	    'input_high':function(){self.input_high.value = String(self.high).substr(0,4);},
	    'drag_low':function(){
		self.drag_low.element.style.left = self.low*self.conv +'px'; //math
	    },
	    'drag_high':function(){
		self.drag_high.element.style.left = self.high*self.conv +'px'; //math
	    },
	    'drag_range':function(){
		self.drag_range.element.style.left = self.low*self.conv +'px'; //math
		self.drag_range.element.style.width = (self.high-self.low)*self.conv +'px'; //math
	    }
	};
	delete plans[not_me];
	for (a in plans) {plans[a]();}
	//EquationHighlighter.needsUpdate();
    }

    TemperatureSliders.prototype.graphCursor = function(evt,do_anyway) {
	if (this.freeze && !do_anyway) return;

	var mouse = evt.mouse();
	var coords = getElementPosition(this.canvas);
	var pos_x = mouse.page.x - coords.x;
	this.temp = pos_x - this.graph_left_margin;
	//log(this.temp);
	if (this.temp < 0) { this.temp = 0; }
	if (this.temp > this.canvas_length - this.graph_right_margin) { this.temp = this.canvas_length - this.graph_right_margin; }
	if (this.temp > 0) {
	    this.graph_cursor.style.left = (pos_x)+'px';
	    var self = this;
	    setTimeout(function(){self.updateCursorVals();},10);
	    setTimeout(function(){showElement(self.graph_cursor);},10);
	}
    }
    TemperatureSliders.prototype.setCursorFreeze = function(evt) {
	var src = evt.src();
	if (src.id == 'unfreeze') {
	    this.freeze = false;
	    hideElement(src);
	}
	else {
	    this.graphCursor(evt,true);
	    this.freeze = true;
	    showElement('unfreeze');
	}
    }
    TemperatureSliders.prototype.updateCursorVals = function(evt) {
	var lf = global.LeafData;
	var real_temp = lf.t_a_min + (lf.t_a_max-lf.t_a_min)*this.temp/(this.canvas_length - this.graph_right_margin);
	if (!isNaN(real_temp)) {
	    $('temp_mouse').value = Math.round(real_temp * 10) / 10;
	    for (a in lf.species) {
		$(a+'-R').value = lf.arrhenius(a,real_temp);
	    }
	}
    }
    
    function getNumSpecies() {
      return numSpecies;
    }
    function incNumSpecies() {
      numSpecies++;
    }
    function getScenario1Species() {
      return scenario1Species;
    }
    
    addLoadEvent(initSpeciesCloner);
    addLoadEvent(initSpecies);
    global.addSpecies = addSpecies;
    global.delSpecies = delSpecies;
    global.getNumSpecies = getNumSpecies;
    global.incNumSpecies = incNumSpecies;
    global.getScenario1Species = getScenario1Species;
    global.EquationHighlighter = new EquationHighlighter();
    global.TemperatureSliders = new TemperatureSliders();

})();