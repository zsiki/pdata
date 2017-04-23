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
				});
		} else {
			alert("No row(s) selected")
		}
	});
	// datepicker
	$("#d1").datepicker();
	// edit form 
	function save() {
		// check fields
		var loc = {table: "pdata"};
		var fields = ["id", "easting", "northing"];
		var opts = ["elev", "d1"];
		for (i = 0; i < fields.length; i++) {
			loc[fields[i]] = $("#"+fields[i]).val().trim();
			if (loc[fields[i]].length == 0) {
				alert(fields[i] + " is empty");
				return;
			}
		}
		for (i = 0; i < opts.length; i++) {
			var w = $("#"+fields[i]).val().trim();
			if (w.length == 0 && dialog.mode == "upd") {
				alert(opts[i] + " is empty");
				return;
			}
			loc[opts[i]] = w;
		}
		if (dialog.mode == "ins") {
			$.ajax({url: path + "dbins",
				data: loc}).done(
				function (data) {
					alert(data);
					$("#ref").trigger("click");
				});
		}	
		dialog.dialog("close");
	}
	dialog = $("#dia").dialog({autoOpen: false, modal: true,
		buttons: { Save: save,
			Cancel: function () { dialog.dialog("close");}
		}
	});
	$("#ins").click(function () {
		dialog.mode = "ins";
		dialog.dialog("open");
	});
	$("#upd").click(function () {
		dialog.mode = "upd";
		dialog.dialog("open");
	});
});
