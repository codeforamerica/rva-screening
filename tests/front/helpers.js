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

// lol at this
function createMultiform() {
  document.write("<div class=\"form_multiform_wrapper\">");
  document.write("  <div class=\"form_multiform form_multiform_read\" id=\"test_multiform\">");
  document.write("    <div class=\"multiform_content\">");
  document.write("      <div class=\"multiform_content_fields\">");
  document.write("        <label>");
  document.write("          Enter something");
  document.write("          <input class=\"field_input\" name=\"something-0\" type=\"text\" id=\"something-0\" value=\"this is my content\">");
  document.write("        <\/label>");
  document.write("      <\/div>");
  document.write("      <div class=\"multiform_content_readonly\">");
  document.write("        <span class=\"multiform_item\">this is my content<\/span><br>");
  document.write("      <\/div>");
  document.write("    <\/div>");
  document.write("    <div class=\"multiform_controls\">");
  document.write("      <button type=\"button\" id=\"test_edit_button\" class=\"multiform_control_edit\" value=\"Edit\"><\/button>");
  document.write("      <button type=\"button\" id=\"test_remove_button\" class=\"multiform_control_remove\" value=\"Remove\"><\/button>");
  document.write("    <\/div>");
  document.write("  <\/div>");
  document.write("  <div class=\"form_multiform form_multiform_new\" id=\"data_clone_test\">");
  document.write("    <div class=\"multiform_content\">");
  document.write("      <div class=\"multiform_content_fields\">");
  document.write("        <label>");
  document.write("          Enter something");
  document.write("          <input name=\"something-1\" id=\"something-1\" type=\"text\" value=\"\">");
  document.write("        <\/label>");
  document.write("      <\/div>");
  document.write("    <\/div>");
  document.write("  <\/div>");
  document.write("  <button data-clone-id=\"data_clone_test\" class=\"multiform_control_add\" id=\"data_clone_test_add\">add new<\/button>");
  document.write("<\/div>");
}