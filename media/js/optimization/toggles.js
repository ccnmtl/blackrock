function toggle(e) {
    var rightarrow =
        getFirstElementByTagAndClassName('span', 'rightarrow', e.src());
    var downarrow =
        getFirstElementByTagAndClassName('span', 'downarrow', e.src());
    var parent =
        getFirstParentByTagAndClassName(e.src(), 'div', 'toggle-container');
    var inner =
        getFirstElementByTagAndClassName('div', 'toggle-nest', parent);

    var visible = (getStyle(downarrow, 'display') != 'none');

    if (visible) {
        setStyle(downarrow, {'display': 'none'});
        setStyle(rightarrow, {'display': 'inline'});
        setStyle(inner, {'display': 'none'});
    } else {
        setStyle(downarrow, {'display': 'inline'});
        setStyle(rightarrow, {'display': 'none'});
        setStyle(inner, {'display': 'block'});
    }
}

function initToggles() {
    var elts = getElementsByTagAndClassName('*', 'toggle-control');
    forEach(elts, function(elem) {
        connect(elem, 'onclick', toggle);
    });
}

addLoadEvent(initToggles);