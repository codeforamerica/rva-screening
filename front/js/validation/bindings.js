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
    processor(origin, recipient);
  });
}