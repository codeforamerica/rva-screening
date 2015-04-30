window.App = window.App || {};

var AppController = function ( options ) {
  console.info('APP INITIALIZED :)');
  this.options = options || {};
  this.waka = 'flaka';
  this.hiphip = 'hooray!';
  console.log(this);
};