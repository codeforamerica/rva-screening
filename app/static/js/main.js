window.App = window.App || {};

var AppController = function ( options ) {
  this.options = options || {};
  this.waka = 'flaka';
  this.hiphip = 'hooray!';
  console.info('APP INITIALIZED :)');
  console.log(this);
};