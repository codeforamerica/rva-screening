function createField(type, attributes, parentId) {
  var elem = document.createElement(type);
  for (a in attributes) {
    elem.setAttribute(a, attributes[a]);
  }
  document.getElementById(parentId).appendChild(elem);
};

function createForm(className, id) {
  var form = document.createElement('form');
  form.className = className;
  form.id = id;
  document.body.appendChild(form);
}