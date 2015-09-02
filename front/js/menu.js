Function.prototype.bind = Function.prototype.bind || function (thisp) {
  var fn = this;
  return function () {
    return fn.apply(thisp, arguments);
  };
};

window.Menu = window.Menu || {};

var Menu = function ( options ) {
  this.options = options || {};
  this.yDown = null;
  this.xDown = null;
  if (!options.id) {
    var err = new Error('Please specify an ID for the menu');
    throw err;
  }
  this.id = options.id;
  this.swipeMenuState = false;
  this.elem = document.getElementById(options.id);
  this.button = document.getElementById('nav_button');
  that = this;

  window.ontouchstart = function(e) {
    handleTouchStart(e, that);
  };

  window.ontouchmove = function(e) {
    handleTouchMove(e, that);
  };

  that.button.addEventListener('click', function(e) {
    menuToggle(that);
  });

};

function menuOpen(that) {
  that.elem.className += ' open';
  document.body.className = 'menu_open';
  that.button.className += ' open';
  that.swipeMenuState = !that.swipeMenuState;
}

function menuClose(that) {
  that.elem.className = 'nav';
  document.body.className = '';
  that.button.className = 'button_nav';
  that.swipeMenuState = !that.swipeMenuState;
}

function menuToggle(that) {
  if (that.swipeMenuState) {
    menuClose(that);
  } else {
    menuOpen(that);
  }
}

function handleTouchStart(event, that) {
  that.xDown = event.touches[0].clientX;                                      
  that.yDown = event.touches[0].clientY;
}

function handleTouchMove(event, that) {
  if ( isNaN(that.xDown) || isNaN(that.yDown) ) {
    return;
  }
  var xUp = event.touches[0].clientX,                                    
      yUp = event.touches[0].clientY,
      xDiff = that.xDown - xUp,
      yDiff = that.yDown - yUp;

  if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {
    document.body.className = 'menu_open'; // prevent vertical scroll during open
    if ( xDiff > 0 ) {
      if (that.swipeMenuState) menuClose(that); 
    } else {
      if (!that.swipeMenuState) menuOpen(that);
    }                       
  } else {
    if ( yDiff > 0 ) {
      return;
    } else { 
      return;
    }                                                                 
  }
  /* reset values */
  that.xDown = null;
  that.yDown = null;
}