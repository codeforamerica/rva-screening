window.Menu = window.Menu || {};

var Menu = function ( options ) {
  this.options = options || {};

  this.yDown = null;
  this.xDown = null;
  this.swipeMenuState = false;
  this.elem = document.getElementById('nav');
  this.button = document.getElementById('nav_button');
  var _this = this;
  events();

  function events() {
    document.addEventListener('touchstart', _this.handleTouchStart.bind(_this), false);
    _this.button.addEventListener('click', _this.toggle.bind(_this), false);        
    document.addEventListener('touchmove', _this.handleTouchMove.bind(_this), false);
  }

  console.info('Menu initialized :)');
};

Menu.prototype.open = function() {
  var m = this;
  m.elem.className += ' open';
  document.body.className = 'menu_open';
  m.button.className += ' open';
  m.swipeMenuState = !m.swipeMenuState;
};

Menu.prototype.close = function() {
  var m = this;
  m.elem.className = 'nav';
  document.body.className = '';
  m.button.className = 'button button_nav';
  m.swipeMenuState = !m.swipeMenuState;
};

Menu.prototype.toggle = function() {
  var m = this;
  if (m.swipeMenuState) {
    m.close();
  } else {
    m.open();
  }
};

Menu.prototype.handleTouchStart = function(event) {
  var m = this;
  m.xDown = event.touches[0].clientX;                                      
  m.yDown = event.touches[0].clientY;
};

Menu.prototype.handleTouchMove = function(event) {
  var m = this;
  if ( ! this.xDown || ! this.yDown ) {
    return;
  }
  var xUp = event.touches[0].clientX,                                    
      yUp = event.touches[0].clientY,
      xDiff = this.xDown - xUp,
      yDiff = this.yDown - yUp;
  if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {
    document.body.className = 'menu_open'; // prevent vertical scroll during open
    if ( xDiff > 0 ) {
      if (this.swipeMenuState) this.close(); 
    } else {
      if (!this.swipeMenuState) this.open();
    }                       
  } else {
    if ( yDiff > 0 ) {
      /* up swipe, do nothing */ 
    } else { 
      /* down swipe, do nothing */
    }                                                                 
  }
  /* reset values */
  this.xDown = null;
  this.yDown = null; 
};