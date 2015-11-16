describe('search.js', function() {

  var search, searchInput, s;

  var searchData = {list:[{dob:"1962-04-14",fname:"Rick",lname:"Nader",ssn:"504-38-1775",url:"/patient_details/1"},{dob:"2000-02-17",fname:"Samir",lname:"Nasri",ssn:"222-22-2222",url:"/patient_details/4"}],total:2};
  var badSearchData = {lists:[{name:'WakaFlaka'},{name:'FlakaBadaka'}],total:3}
  var successfulSearchResults = [{dob:"1962-04-14",name:"Rick Nader",ssn:"504-38-1775",url:"/patient_details/1"}];
  var generalSearchResults = [{dob:"1962-04-14",name:"Rick Nader",ssn:"504-38-1775",url:"/patient_details/1"},{dob:"2000-02-17",name:"Samir Nasri",ssn:"222-22-2222",url:"/patient_details/4"}];
  var unsuccessfulSearchResults = [];
  var successfulResultsTranslation = {patients:successfulSearchResults,none:[{name:"Nade"}]};

  var opts = { foo: 'bar', elementClass: '.field_input_search', searchData: searchData };
  var optsNoSearchData = { foo: 'bar', elementClass: '.field_input_search' };
  var optsNoElementClass = { foo: 'bar', searchData: searchData };

  var htmlSuccessfulSingleResponse = '<ul xmlns:d="defiant-namespace" class="list list_table"><li class="list_row"><a href="/patient_details/1"><span class="list_row_item list_row_name"> Rick Nader </span><span class="list_row_item list_row_dob">1962-04-14</span><span class="list_row_item list_row_edits">Richmond Resource Center</span></a></li><li class="list_row"><a href="/patient_details/52"><span class="list_row_item list_row_name"> Samuel Matthews </span><span class="list_row_item list_row_dob">1989-02-09</span><span class="list_row_item list_row_edits">Richmond Resource Center</span></a></li><li class="list_row list_row_addnew"><a href="/new_patient"><i class="fa fa-plus"></i> Not the right <strong>Nader</strong>? Add them as a new patient.</a></li></ul>';

  beforeEach(function() {
    searchInput = document.createElement('input');
    searchInput.className = 'field_input_search';
    document.body.appendChild(searchInput);
    search = new Search(opts);
    s = Search; // locally scoped version of search for usage within it()
  });

  afterEach(function() {
    document.body.innerHTML = '';
    search = null;
  });

  describe('Initialization', function() {

    it('Throws error if no options are passed', function() {
      expect(function() { s(); }).to.throw(Error);
    });

    it('Throws error if .elementClass does not exist', function() {
      expect(function(){ s(optsNoElementClass); }).to.throw(Error);
    });

    it('Throws error if no search data', function() {
      expect(function() { s(optsNoSearchData); }).to.throw(Error);
    });

    it('Search is initialized with options', function() {
      expect(search.options).to.equal(opts);
    });

    it('Search elementClass exists', function() {
      expect(search.options.elementClass).to.equal(opts.elementClass);
    });
  });

  describe('Results', function() {

    var searchOptions = {
      keys: ['fname', 'lname', 'dob', 'ssn'],   // keys to search in
      includeScore: true,
      threshold: 0.5      // we should play around with this
    };
    var f = new Fuse(searchData.list, searchOptions);

    it('Unsuccessful Fuse.search() returns empty array', function() {
      var res = f.search('x');
      expect(res.length).to.equal(0);
    });

    it('Vague Fuse.search() returns fuzzy response', function() {
      var res = f.search('a');
      expect(res.length).to.equal(2);
    });

    it('Explicit Fuse.search() returns specific response', function() {
      var res = f.search('Rick');
      expect(res.length).to.equal(1);
    });

  });

  describe('Templates', function() {

    var searchOptions = {
      keys: ['fname', 'lname', 'dob', 'ssn'],   // keys to search in
      includeScore: true,
      threshold: 0.5      // we should play around with this
    };
    var f = new Fuse(searchData.list, searchOptions);
    
    // it('Renders a proper list on successful response', function() {
    //   window.newPatientUrl = '/url'; // this is suuuuuper hacky
    //   var resultsContainer = document.createElement('div');
    //   resultsContainer.id = 'results_container';
    //   document.body.appendChild(resultsContainer);
    //   var results = translateResults(f.search('a'));
    //   var html = templates.render('list', results);
    //   $('#results_container').html(html);
    //   expect(document.getElementsByTagName('li').length).to.equal(3); // three includes "add new" button
    // });

    it('Renders an empty list on empty response, but has "add new" button', function() {
      window.newPatientUrl = '/url'; // this is suuuuuper hacky
      var resultsContainer = document.createElement('div');
      resultsContainer.id = 'results_container';
      document.body.appendChild(resultsContainer);
      var results = translateResults(f.search('x'));
      var html = templates.render('list', results);
      $('#results_container').html(html);
      expect(document.getElementsByTagName('li').length).to.equal(1); // three includes "add new" button
    });

  });

});