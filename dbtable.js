/*
	javascript stuff for dbtable application
*/
$(document).ready(function () {
	// refresh dbtable
	$("#ref").click(function () {
		$.ajax({url: path + "dbtable",
			data: {table: "pdata"}}).done(
			function (data) {
				$("#dbtable").html(data);
				alert("refreshed");
			});
	});
	// delete marked records
	$("#del").click(function () {
		var s = "";
		$(":input:checkbox:checked").
			each( function (ind,val) {
				s += val.name + ";";
			});
		//alert(s);
		if (s.length) {
			$.ajax({url: path + "dbdel",
				data: {table: "pdata", ids: s}}).done(
				function (data) {
					alert(data);
					$("#ref").trigger("click");
				}
                        )
		} else {
			alert("No row(s) selected")
		}
	});
	// datepicker
	$("#d1").datepicker();
	// edit form 
	function save() {
	}
	dialog = $("#dia").dialog({autoOpen: false, modal: true,
		buttons: { "Save": save,
		Cancel: function () { dialog.dialog("close");}}
	});
	$("#upd").click(function () {
		dialog.dialog("open");
	});
});
