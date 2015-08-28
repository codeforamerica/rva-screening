describe('menu.js', function() {

  var opts = {
    id: 'nav'
  };

  var menuHTML = '<nav class="nav cf" id="nav"><div class="nav_logo"><img src=""></div><div class="nav_menu"><ul class="nav_menu_list"><li class="menu_list_item "><a href="/new_prescreening"><i class="fa fa-pencil"></i> Pre-Screener</a></li><li class="menu_list_item "><a href="/"><i class="fa fa-search"></i> Search Patients</a></li></ul></div><div class="nav_user"><a href="#" class="nav_user_profile">daily_planet_user@test.com</a> / <a href="/logout">Logout</a></div></nav>';

  beforeEach(function() {
    // var nav = document.createElement('div');
    // nav.id = 'nav';
    // document.body.appendChild(nav);

    document.body.innerHTML = menuHTML;

    var btn = document.createElement('button');
    btn.className = 'button_nav';
    btn.id = 'nav_button';
    btn.type = 'button';
    btn.onclick = function() {
      document.body.className = 'waka';
    }
    b = btn;

    document.body.appendChild(btn);

    m = Menu; // locally scoped menu function
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  describe('Initialization', function() {

    it('fails if no menu id is specified or found', function() {
      expect(function(){ m(); }).to.throw(Error);
    });

    it('sets options properly', function() {
      var menu = new m(opts);
      expect(menu.options).to.equal(opts);
    });

  });

  describe('DOM Elements', function() {

    it('.nav_menu class exists', function() {
      var navMenu = document.getElementsByClassName('nav_menu').length;
      expect(navMenu).to.not.equal(0);
    });

    it('.button_nav class exists', function() {
      var navMenu = document.getElementsByClassName('button_nav').length;
      expect(navMenu).to.not.equal(0);
    });

  });

  describe('User interaction', function() {

    it('toggles open', function() {
      var menu = new m(opts);
      menuToggle(menu);
      expect(document.body.className).to.equal('menu_open');
    });

    it('toggles closed', function() {
      var menu = new m(opts);
      menuToggle(menu); // toggle open
      menuToggle(menu); // toggle close
      expect(document.body.className).to.equal('');
    });

    it('menu opens on touchstart functions to the right', function() {
      var menu = new m(opts);
      var fakeEventObject = {touches:[{clientX:0,clientY:0,}]};
      var fakeEventObject2 = {touches:[{clientX:10,clientY:0,}]};

      handleTouchStart(fakeEventObject, menu); // initiate touch event
      handleTouchMove(fakeEventObject2, menu); // enact touch event

      expect(document.body.className).to.equal('menu_open');
    });

    it('menu closes on touchstart functions to the left', function() {
      var menu = new m(opts);
      var fakeEventObject = {touches:[{clientX:10,clientY:0,}]};
      var fakeEventObject2 = {touches:[{clientX:0,clientY:0,}]};
      
      menuToggle(menu);
      expect(document.body.className).to.equal('menu_open');

      handleTouchStart(fakeEventObject, menu); // initiate touch event
      handleTouchMove(fakeEventObject2, menu); // enact touch event

      expect(document.body.className).to.equal('');
    });

  });

});