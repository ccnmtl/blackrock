/* global initSpeciesModule: true, setup: true */
/* global getSpeciesList: true */

function formSubmit() {
    $('specieslist').value = getSpeciesList().join();
    $('leaf-form').submit();
}

function initNav() {
    connect('tab-canopy', 'onclick', formSubmit);
}
addLoadEvent(initNav);

addLoadEvent(function() {
    initNav();
    initSpeciesModule();
    setup();
});