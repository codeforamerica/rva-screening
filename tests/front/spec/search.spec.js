describe('search.js', function() {

  var search, searchInput, s;

  var searchData = {list:[{dob:"1962-04-14",name:"Rick Nader",ssn:"504-38-1775",url:"/patient_details/1"},{dob:"2000-02-17",name:"Samir Nasri",ssn:"222-22-2222",url:"/patient_details/4"}],total:2};
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

  describe('Utilites', function() {
    it('Defiant.js exists', function() {
      expect(typeof Defiant).to.equal('object');
    });

    it('Defiant.render() is a function', function() {
      expect(typeof Defiant.render).to.equal('function');
    });

    it('JSON.search() is a function', function() {
      expect(typeof JSON.search).to.equal('function');
    });
  });

  describe('Results', function() {

    it('Throws error if no search data', function() {
      expect(function() {  })
    });

    it('Unsuccessful JSON.search() returns empty array', function() {
      var res = JSON.search(searchData, '//*[contains(name, "Waka")]');
      expect(res).to.deep.equal(unsuccessfulSearchResults);
    });

    it('Successful JSON.search() returns success object when searching by name', function() {
      var res = JSON.search(searchData, '//*[contains(name, "Nade")]');
      expect(res).to.deep.equal(successfulSearchResults);
    });

    it('General JSON.search() returns all matches', function() {
      var res = JSON.search(searchData, '//*[contains(name, "na")]');
      expect(res).to.deep.equal(generalSearchResults);
    });

    it('Results are translated for rendering template properly', function() {
      var res = JSON.search(searchData, '//*[contains(name, "Nade")]');
      var results = translateResults(res, "Nade"); // function from search.js
      expect(results).to.deep.equal(successfulResultsTranslation);
    });

    // TODO: write tests that search by ssn and dob
  });

  // TODO: can't test templates yet because we don't have the xsl loaded in Karma
  describe('Templates', function() {
    // unsure how to test XSL templating
    // it('Templates exist', function() {});
    // it('Single result HTML string renders properly', function() {
    //   var res = JSON.search(searchData, '//*[contains(name, "Nader")]');
    //   var results = translateResults(res, "Nade"); // function from search.js
    //   var html = Defiant.render('search_results_list', results);
    // });
    // it('HTML is blank if nothing searched', function() {});
    // it('Create new patient renders if no results', function() {});
  });

});