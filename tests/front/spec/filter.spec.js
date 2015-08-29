describe('filter.js', function() {

  describe('Search page filters', function() {

    beforeEach(function() {
      var btn1 = document.createElement('button');
      btn1.className = 'filter filter_statistic filter_active';
      btn1.setAttribute('data-list', '0');
      btn1.id = 'btn1';
      document.body.appendChild(btn1);

      var btn2 = document.createElement('button');
      btn2.className = 'filter filter_statistic';
      btn2.setAttribute('data-list', '1');
      btn2.id = 'btn2';
      document.body.appendChild(btn2);

      var ul1 = document.createElement('ul');
      ul1.className = 'list list_table list_filter list_filter_active';
      ul1.id = 'list-0';
      document.body.appendChild(ul1);

      var ul2 = document.createElement('ul');
      ul2.className = 'list list_table list_filter';
      ul2.id = 'list-1';
      document.body.appendChild(ul2);
    });

    afterEach(function() {
      document.body.innerHTML = '';
    });

    it('should update filter button classes when listFilterClick is run', function() {
      listFilterClick($('#btn2'));
      expect($('#btn1').hasClass('filter_active')).to.equal(false);
      expect($('#btn2').hasClass('filter_active')).to.equal(true);
    });

    it('active filter id should match active list id after filter select', function() {
      listFilterClick($('#btn2'));
      expect('list-'+$('#btn2').attr('data-list')).to.equal($('.list_filter_active')[0].id);
    });
  });

  describe('Question filters', function() {

    beforeEach(function() {
      var input1 = document.createElement('input');
      input1.setAttribute('name', 'q_an');
      input1.checked = true;
      input1.setAttribute('type', 'checkbox');
      input1.id = 'input1';
      document.body.appendChild(input1);
      
      var q1 = document.createElement('label');
      q1.className = 'q_unique q_an';
      document.body.appendChild(q1);
    });

    afterEach(function() {
      document.body.innerHTML = '';
    });

    it('question hides when input is checked false', function() {
      $('#input1').prop('checked', false); // mimicks user check
      serviceFilterChange($('#input1'));
      expect($('.q_an').css('display')).to.equal('none');
    });
  });

});