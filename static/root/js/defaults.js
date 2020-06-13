if (window.productionMode) {
  console.debug = function() {};
  console.error = function() {};
  console.log = function() {};
  console.warn = function() {};
}
