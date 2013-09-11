

/**********************************************************/
function add_markers (map) {

    trap_marker (2, 	[41.39247,	-74.02119], map);
    trap_marker (3, 	[41.39285,	-74.02100], map);
    trap_marker (4, 	[41.39319,	-74.02077], map);
    trap_marker (5, 	[41.39259,	-74.02066], map);
    trap_marker (6, 	[41.39266,	-74.02044], map);
    trap_marker (7, 	[41.39273,	-74.02042], map);
    trap_marker (8, 	[41.39238,	-74.02095], map);
    trap_marker (9, 	[41.39258,	-74.02052], map);
    trap_marker (10,	[41.39265,	-74.02042], map);
    trap_marker (11,	[41.39193,	-74.02129], map);
    trap_marker (12,	[41.39156,	-74.02103], map);
    trap_marker (13,	[41.39141,	-74.02089], map);
    trap_marker (14,	[41.39146,	-74.02159], map);
    trap_marker (15,	[41.39122,	-74.02145], map);
    trap_marker (16,	[41.39107,	-74.02136], map);
    trap_marker (17,	[41.39151,	-74.02153], map);
    trap_marker (18,	[41.39144,	-74.02162], map);
    trap_marker (19,	[41.39088,	-74.02164], map);
    trap_marker (20,	[41.39128,	-74.02201], map);
    trap_marker (21,	[41.39098,	-74.02213], map);
    trap_marker (22,	[41.39082,	-74.02225], map);
    trap_marker (23,	[41.39194,	-74.02209], map);
    trap_marker (24,	[41.39170,	-74.02278], map);
    trap_marker (25,	[41.39177,	-74.02285], map);
    trap_marker (26,	[41.39219,	-74.02177], map);
    trap_marker (27,	[41.39220,	-74.02213], map);
    trap_marker (28,	[41.39215,	-74.02251], map);
    trap_marker (29,	[41.39223,	-74.02245], map);
    trap_marker (30,	[41.39239,	-74.02319], map);
    trap_marker (31,	[41.39246,	-74.02354], map);
    trap_marker (32,	[41.39207,	-74.02181], map);
    trap_marker (33,	[41.39208,	-74.02178], map);
    trap_marker (34,	[41.39221,	-74.02191], map);
    trap_marker (35,	[41.39257,	-74.02187], map);
    trap_marker (36,	[41.39259,	-74.02211], map);
    trap_marker (37,	[41.39088,	-74.02164], map);
    trap_marker (38,	[41.40628,	-74.00873], map);
    trap_marker (39,	[41.40585,	-74.00920], map);
    trap_marker (40,	[41.40580,	-74.00917], map);
    trap_marker (41,	[41.40615,	-74.00885], map);
    trap_marker (42,	[41.40615,	-74.00933], map);
    trap_marker (43,	[41.40620,	-74.00930], map);
    trap_marker (45,	[41.40762,	-74.00892], map);
    trap_marker (46,	[41.40757,	-74.00922], map);
    trap_marker (47,	[41.40652,	-74.00900], map);
    trap_marker (48,	[41.40640,	-74.00907], map);
    trap_marker (49,	[41.40645,	-74.00932], map);
    trap_marker (50,	[41.40670,	-74.00892], map);
  //trap_marker (51,	[41.40683,	-74.01233], map);
    trap_marker (52,	[41.40407,	-75.00063], map);
  //trap_marker (53,	[41.40408,	-74.00552], map);
    trap_marker (54,	[41.40747,	-74.00877], map);
  //trap_marker (55,	[41.40900,	-74.00900], map);
  //trap_marker (56,	[41.40797,	-74.00088], map);
    trap_marker (57,	[41.40688,	-74.00985], map);
    trap_marker (58,	[41.40727,	-74.00847], map);
    trap_marker (59,	[41.40727,	-74.00847], map);
    trap_marker (60,	[41.40707,	-74.00912], map);
    trap_marker (61,	[41.40773,	-74.00957], map);
    trap_marker (62,	[41.40765,	-74.00995], map);
  //trap_marker (63,	[41.40517,	-74.00770], map);
    trap_marker (64,	[41.40648,	-74.00765], map);
    trap_marker (65,	[41.40643,	-74.00755], map);
    trap_marker (66,	[41.40783,	-74.00823], map);
    trap_marker (67,	[41.40783,	-74.00847], map);
  //trap_marker (68,	[41.40020,	-74.00840], map);
    trap_marker (69,	[41.40685,	-74.01020], map);
  //trap_marker (70,	[41.40000,	-74.00085], map);
    trap_marker (71,	[41.40645,	-74.00805], map);  // likely correct coordinates but wrong center point
    trap_marker (72,	[41.40620,	-74.00795], map);
    trap_marker (73,	[41.40595,	-74.00790], map);
    
}e

function trap_marker (name, where, map) {
    ppp = new google.maps.LatLng( where[0], where [1]);
    //console.log (ppp);

    result = new google.maps.Marker ({
	'position' : ppp
	, 'map' : map
	, 'title': name
    });
    return result
}

