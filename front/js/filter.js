/*
**  FILTERS
**  
**
*/

// var Filter = function(options) {
//   this.options = options || {};
//   this.filter_element = document.getElementById(options.id);
//   this.filters = options.filters;
//   this.buttons = [];
//   this.filterClass = '.' + options.filterClass;

//   this._build(this.filters);
// }

// Filter.prototype._build = function(filters) {
//   // build the 'all' filter first
//   this.filter_element.innerHTML = '<span class="sidebar_title"><i class="fa fa-sliders"></i> Filter Patients</span>';
//   this.filter_element.appendChild(this._createFilter('All', 'all', true));
//   var _this = this;
//   for (var i = 0; i < filters.length; ++i) {
//     var filter = _this._createFilter(filters[i].name, filters[i].id);
//     _this.buttons.push(filter);
//     _this.filter_element.appendChild(filter);
//   }
// }

// Filter.prototype._createFilter = function(name, id, activeState) {
//   var _this = this;
//   var btn = document.createElement('button');
//   btn.className = 'button filter_button';
//   if (activeState) btn.className += ' filter_button_active';
//   btn.setAttribute('data-filter', id);
//   btn.innerHTML = name;
//   btn.onclick = function() {
//     $('.filter_button').removeClass('filter_button_active');
//     $(this).addClass('filter_button_active');
//     _this.filterElements(id);
//   }
//   return btn;
// }

// Filter.prototype.filterElements = function(id) {
//   console.log(id);
//   if (id != 'all') {
//     $(this.filterClass).addClass('filter_hide');
//     $('.'+id).removeClass('filter_hide');
//   } else {
//     $(this.filterClass).removeClass('filter_hide');
//   }
// }