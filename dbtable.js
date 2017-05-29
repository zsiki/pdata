/*
	javascript stuff for dbtable application
*/
$(document).ready(function () {
	// refresh dbtable
	$("#ref").click(function () {
		$.ajax({
			url: path + "dbtable",
			data: { table: "pdata" }
		}).done(
			function (data) {
				$("#dbtable").html(data);
				alert("refreshed");
			});
	});
	// delete marked records
	$("#del").click(function () {
		var s = "";
		$(":input:checkbox:checked").
			each(function (ind, val) {
				s += val.name + ";";
			});
		//alert(s);
		if (s.length) {
			$.ajax({
				url: path + "dbdel",
				data: { table: "pdata", ids: s }
			}).done(
				function (data) {
					alert(data);
					$("#ref").trigger("click");
				});
		} else {
			alert("No row(s) selected")
		}
	});

	// datepicker
	$(function () {
		$("#d1").datepicker({ dateFormat: 'yy-mm-dd' });
	});

	var selectedId;

	function updateDialogFill() {
		var s = [];
		$(":input:checkbox:checked").
			each(function (ind, val) {
				s.push(val.name);
			});

		if (s.length == 1) {
			selectedId = s[0].split('|')[0];

			var eredmeny;
			$.post({url: path + "test", data:{ id: selectedId }},
				function (data, status) {
					eredmeny = JSON.parse(data);
					//alert(eredmeny[0][1])
					$("#id").val(eredmeny[0][0]);
					$("#easting").val(eredmeny[0][1]);
					$("#northing").val(eredmeny[0][2]);
					$("#elev").val(eredmeny[0][3]);
					$("#d1").val("");
					$("#d2").val("");

				});
		} else if (s.length > 1) {
			alert("Too many rows selects")
			dialog.dialog("close");
		} else {
			alert("No row selected")
			dialog.dialog("close");
		}
	}

	// edit form 
	function save() {
		// check fields
		var loc = { table: "pdata" };
		var fields = ["id", "easting", "northing"];
		var opts = ["elev", "d1", "d2"];
		if (dialog.mode == "ins" || dialog.mode == "upd") {
			for (i = 0; i < fields.length; i++) {
				loc[fields[i]] = $("#" + fields[i]).val().trim();
				if (loc[fields[i]].length == 0) {
					alert(fields[i] + " is empty");
					return;
				}
			}
			for (i = 0; i < opts.length; i++) {
				var w = $("#" + opts[i]).val().trim();
				if (w.length == 0) {
					if (dialog.mode == "upd") {
						alert(opts[i] + " is empty");
						return;
					} else {
						w = 'NULL'
					}
				} else {
					loc[opts[i]] = w;
				}
			}
			// check timformat
			if (dialog.mode == "ins") {
				var value = w
				var matches = value.match(/([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]/)
				if (matches == null) {
					alert("Not good time-format!");
					return;
				}
			}


			loc["d"] = loc["d1"] + " " + loc["d2"]
			//del loc["d1"]
			if (dialog.mode == "ins") {
				$.ajax({
					url: path + "dbins",
					data: loc
				}).done(
					function (data) {
						alert(data);
						$("#ref").trigger("click");
					});
			}

			if (dialog.mode == "upd") {
				loc["id"] = selectedId;
				$.ajax({
					url: path + "dbupd",
					data: loc
				}).done(
					function (data) {
						alert(data);
						$("#ref").trigger("click");
					});
			}
		}
		dialog.dialog("close");
	}

	dialog = $("#dia").dialog({
		autoOpen: false, modal: true,
		buttons: {
			Save: save,
			Cancel: function () { dialog.dialog("close"); }
		}
	});

	$("#dia").dialog({ open: updateDialogFill });

	$("#ins").click(function () {
		dialog.mode = "ins";
		dialog.dialog("open");
	});

	$("#upd").click(function () {
		dialog.mode = "upd";
		dialog.dialog("open");
	});

	$("#sel").click(function () {
		dialog.mode = "sel";
		dialog.dialog("open");
	});
});
