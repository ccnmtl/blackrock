/*
  LOCAL SESSION at window.Stor
*/
(function() {
    var global = this;
    function hasAttr(obj,key) {
	try {
	    return (typeof(obj[key]) != 'undefined');
	} catch(e) {return false;}
    }

    function NOT(bool) {
	return !bool;
    }

    function StorageWrapper(stor) {

	this.KEYS_KEY = 'KEYS';
	this.hasKey = function(key) {
	    return (stor.getItem(key) != null);
	};
	this.get = function(key,default_val) {
	    return (this.hasKey(key) ? stor.getItem(key) : default_val);
	};
	var key_dict = JSON.parse(this.get(this.KEYS_KEY,'{}'));
	this.set = function(key,value) {
	    stor.setItem(key,value);
	    key_dict[key]=1;
	    stor.setItem(this.KEYS_KEY,JSON.stringify(key_dict));
	};

	///actually returns a dict in the form {key1:1,key2:1,...}
	this.keyDict = function() {
	    return key_dict;
	};
	this.del = function(key) {
	    delete stor[key];
	    delete key_dict[key];
	    stor.setItem(this.KEYS_KEY,JSON.stringify(key_dict));
	};
	this.deleteEveryFuckingThing = function() {
	    for (a in key_dict)  {
		      this.del(a);
      }
	};
    }


    if (window.localStorage) {
	global.Stor = new StorageWrapper(hasAttr(global,'localStorage')?global.localStorage:global.globalStorage[location.hostname]);
	//global.e = global.Stor;
    } else {
	throw "No localStorage support in browser (yet)!";
    }

})();
