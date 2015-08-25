var validations = validations || {};

validations.bindings = [
  { origin: "first_name", recipient:".hh_member.patient .hh_member_full_name", type: "text" },
  { origin: "dob", recipient:".hh_member.patient .hh_member_dob", type: "text" },
  { origin: "ssn", recipient:".hh_member.patient .hh_member_ssn", type: "text" },
];

var bindingsProcessors = {
  "text": function(origin, recipient){
    recipient.text(origin.val());
  }
};

function registerOneWayDataBinding(b){
  var origin = $("[name='"+b.origin+"']");
  var recipient = $(b.recipient);
  var processor = bindingsProcessors[b.type];
  origin.on("change", function(e){
      console.log("changed a sensitive field");
      processor(origin, recipient);
  });
}