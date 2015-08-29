describe('filter.js', function() {

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

  describe('Search page filters', function() {
    it('should update filter button classes when listFilterClick is run', function() {
      listFilterClick($('#btn2'));
      expect($('#btn1').hasClass('filter_active')).to.equal(false);
    });

    it('active filter id should match active list id after filter select', function() {
      listFilterClick($('#btn2'));
      expect('list-'+$('#btn2').attr('data-list')).to.equal($('.list_filter_active')[0].id);
    });
  });

});