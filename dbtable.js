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
	var selectedDate;
	var selectedTime;

	function updateDialogFill() {
		var s = $(":input:checkbox:checked");
		if (s.length == 1) {
			var w = s[0].name;	// point id and date time
			var w1 = w.split('|');
			var selectedId = w1[0];
			var w2 = w1[1].split(' ');
			selectedDate = w2[0];
			selectedTime = w2[1];

			$.ajax({
				url: path + "test",
				data: { table: "pdata", id: selectedId,
					d: w1[1]}
			}).done(
				function (data) {
					var res = JSON.parse(data);
					$("#id").val(res[0]);
					$("#easting").val(res[1] == 'None' ? '' : res[1]);
					$("#Elev").val(res[2] == 'None' ? '' : res[2]);
					$("#elev").val(res[3] == 'None' ? '' : res[3]);
					w = res[4].split(' ');
					$("#d1").val(w[0]);
					$("#d2").val(w[1]);
				});
		} else if (s.length > 1) {
			alert("Too many rows selected")
			dialog.dialog("close");
		} else {
			alert("Select a row!")
			dialog.dialog("close");
		}
	}

	// edit form 
	function save() {
		// check fields
		var loc = { table: "pdata" };
		var fields = ["id", "easting", "Elev"];
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
			// check timeformat
			if (dialog.mode == "ins") {
				var value = w
				var matches = value.match(/([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]/)
				if (matches == null) {
					alert("Invalid time format!");
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

	// Data filter dialog save function.
	function filtSave () {
		// Match the given date against the accepted format (empty or full date).
		var minD = $("#filtMinD").val();
		var maxD = $("#filtMaxD").val();
		var dateMatch = minD.match(/^[0-9]{4}\-[0-9]{2}\-[0-9]{2}\ [0-9]{2}\:[0-9]{2}\:[0-9]{2}$|^$/) &&
						maxD.match(/^[0-9]{4}\-[0-9]{2}\-[0-9]{2}\ [0-9]{2}\:[0-9]{2}\:[0-9]{2}$|^$/);
						
		// Match the coordinates and the elevations against the accepted format.
		var minEasting = $("#filtMinEasting").val();
		var maxEasting = $("#filtMaxEasting").val();
		var eastingMatch = minEasting.match(/^[0-9]+\.?[0-9]*$|^$/) &&
						   maxEasting.match(/^[0-9]+\.?[0-9]*$|^$/);

		var minNorthing = $("#filtMinNorthing").val();
		var maxNorthing = $("#filtMaxNorthing").val();
		var northingMatch = minNorthing.match(/^[0-9]+\.?[0-9]*$|^$/) &&
						    maxNorthing.match(/^[0-9]+\.?[0-9]*$|^$/);

		var minElev = $("#filtMinElev").val();
		var maxElev = $("#filtMaxElev").val();
		var elevMatch = minElev.match(/^[0-9]+\.?[0-9]*$|^$/) &&
						maxElev.match(/^[0-9]+\.?[0-9]*$|^$/);
		
		// Check the matches.
		if (dateMatch == null) {
			alert("Invalid date format!");
		} else if (eastingMatch == null) {
			alert("Invalid Easting format!");
		} else if (northingMatch == null) {
			alert("Invalid Northing format!");
		} else if (elevMatch == null) {
			alert("Invalid Elevation format!");
		} else {
			$.ajax({
				url: path + "dbfilt",
				data: {
					table: "pdata",
					id: $("#filtId").val(),
					minEasting: $("#filtMinEasting").val(),
					maxEasting: $("#filtMaxEasting").val(),
					minNorthing: $("#filtMinNorthing").val(),
					maxNorthing: $("#filtMaxNorthing").val(),
					minElev: $("#filtMinElev").val(),
					maxElev: $("#filtMaxElev").val(),
					minD: $("#filtMinD").val(),
					maxD: $("#filtMaxD").val()
				}
			}).done(
				function (data) {
					// Parse the returned JSON.
					var res = JSON.parse(data)
					// filtHTML contains the HTML code of the filtered rows.
					$("#dbtable").html(res.filtHTML)
					// The number of returned rows is alerted to the user.
					alert(res.rcount);
				});
			
				// Close the dialog box.
				filtDialog.dialog("close");
		};
	};

	dialog = $("#dia").dialog({
		autoOpen: false, modal: true,
		buttons: {
			Save: save,
			Cancel: function () { dialog.dialog("close"); }
		}
	});

	// Create data filter dialog.
	filtDialog = $("#filtDia").dialog({
		autoOpen: false, modal: true, width: "auto",
		buttons: {
			Valami: filtSave,
			Cancel: function () { filtDialog.dialog("close"); }
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

	// Open the data filter dialog if the "filter" button is pressed.
	$("#filt").click(function () {
		filtDialog.dialog("open");
	});
});
