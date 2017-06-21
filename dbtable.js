/*
	javascript stuff for dbtable application
*/
$(document).ready(function () {
	// refresh dbtable
	$("#ref").click(function () {
		$.ajax({
			url: path + "dbtable",
			data: { 
				table: "pdata",
				idFilt: idF,
				eastingFilt: eastingF,
				northingFilt: northingF,
				elevFilt: elevF,
				d1Filt: d1F,
				d2Filt: d2F 
			}
		}).done(
			function (data) {
				// Parse the JSON data returned.
				var refrData = JSON.parse(data);

				$("#dbtable").html(refrData.html);
				if (dialog.mode == "filt") {
					alert("Database filtered. " + refrData.rowcount + " row(s) returned.")
					dialog.mode = "";
				} else {
					alert("Database refreshed!");					
				};
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

	//datepicker
	$(function () {
		$("#d1").datepicker({ dateFormat: 'yy-mm-dd',
							  constrainInput: false });
	});

	var selectedId;
	var selectedDate;
	var selectedTime;

	// Initialize filter dialog box variables.
	var idF = "";
	var eastingF = "";
	var northingF = "";
	var elevF = "";
	var d1F = "";
	var d2F = "";

	function dialogFill() {
		// Reset the dialog box text.
		$("#filtMessage").html("");

		// Reset the dialog box fields except if filter is selected.
		if (dialog.mode != "filt") {
			$("#diaFields")[0].reset();
		};


		// Selected checkboxes.
		s = $(":input:checkbox:checked");

		// Filter mode for dialog box.
		if (dialog.mode == "filt") {
			// Getting the previous filter entries.
			$("#id").val(idF);
			$("#easting").val(eastingF);
			$("#northing").val(northingF);
			$("#elev").val(elevF);
			$("#d1").val(d1F);
			$("#d2").val(d2F);

			// Show filtering options to the user.
			$("#filtMessage").html("<p style='margin-bottom:8px'>RegEx can be used to filter the point ID's.</p>" +
								   "<p style='margin-top:0;margin-bottom:8px'>Valid operators for the easting, northing, elevation, date and hour filtering: " +
								   "<, >, =, <=, >=, and, or, between x and y.</p>" +
								   "<p style='margin-top:0'>Example: < 2017-02-02 and >= 2017-01-03</p>")
		};

		if (dialog.mode == "upd") {
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
						$("#northing").val(res[2] == 'None' ? '' : res[2]);
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
		};

		return[selectedDate, selectedId, selectedTime];
	
	};

	// edit form 
	function save() {
		// Filter option for the dialog box.
		if (dialog.mode == "filt") {
			// Get the values from the filter dialog box.
			idF = $("#id").val();
			eastingF = $("#easting").val();
			northingF = $("#northing").val();
			elevF = $("#elev").val();
			d1F = $("#d1").val();
			d2F = $("#d2").val();

			// Validate the field values.
			// Easting, Northing and Elevation validation:
			if (coordValid(eastingF) == 0) {
				alert("Easting filter invalid!");
				return;
			};

			if (coordValid(northingF) == 0) {
				alert("Northing filter invalid!");
				return;
			};

			if (coordValid(elevF) == 0) {
				alert("Elevation filter invalid!");
				return;
			};

			// D1 validation (year-month-day):
			if (dateValid(d1F) == 0) {
				alert("Date filter invalid!")
				return;
			};

			//D2 validation (hour-minute-second):
			if (hmsValid(d2F) == 0) {
				alert("Hour:Minute:Second filter invalid!");
				return;
			};

			// Trigger the refresh button with the filter settings.
			$("#ref").trigger("click");
		};

		// check fields
		var loc = { table: "pdata" };
		var fields = ["id", "easting", "northing"];
		var opts = ["elev", "d1", "d2"];
		if (dialog.mode == "ins" || dialog.mode == "upd") {
			for (i = 0; i < fields.length; i++) {
				loc[fields[i]] = $("#" + fields[i]).val().trim();
				if (loc[fields[i]].length == 0) {
					alert(fields[i] + " is empty");
					return loc;
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
				$.ajax({
					url: path + "dbupd",
					data: loc
				}).done(
					function (data) {
						alert(data);
						$("#ref").trigger("click");
					});
			};

		};

		dialog.dialog("close");
	};

	// Validity checker for the coordinate fields.
	function coordValid(coord) {
		matches = /^(<|>|>=|<=|=)\ ?(\-?\d+\.?\d*|\.\d+)$/.test(coord) +
				  /^(<|>|>=|<=|=)\ ?(\-?\d+\.?\d*|\.\d+)\ (and|or)\ (<|>|>=|<=|=)\ ?(\-?\d+\.?\d*|\.\d+)$/.test(coord) +
				  /^between\ (\-?\d+\.?\d*|\.\d+)\ and\ (\-?\d+\.?\d*|\.\d+)$/.test(coord) +
				  /^$/.test(coord);

		if (matches == 0) {
			return(0);
		} else {
			return(1);
		};
	};

	// Validity checker for the date field.
	function dateValid(d1) {
		matches = /^(<|>|=|<=|>=){1}\ ?\d{4}\-\d{2}\-\d{2}$/.test(d1) +
				  /^(<|>|=|<=|>=){1}\ ?\d{4}\-\d{2}\-\d{2}\ (and|or)\ (<|>|=|<=|>=){1}\ ?\d{4}\-\d{2}\-\d{2}$/.test(d1) +
				  /^between\ \d{4}\-\d{2}\-\d{2}\ and\ \d{4}\-\d{2}\-\d{2}$/.test(d1) +
				  /^$/.test(d1);
	
		if (matches == 0) {
			return(0);
		} else {
			return(1);
		};
	};

	// Validity checker for the hour-minute-second field.
	function hmsValid(d2) {
		matches = /^(<|>|=|<=|>=){1}\ ?\d{2}\:\d{2}\:\d{2}$/.test(d2) +
				  /^(<|>|=|<=|>=){1}\ ?\d{2}\:\d{2}\:\d{2}\ (and|or)\ (<|>|=|<=|>=){1}\ ?\d{2}\:\d{2}\:\d{2}$/.test(d2) +
				  /^between\ \d{2}\:\d{2}\:\d{2}\ and\ \d{2}\:\d{2}\:\d{2}$/.test(d2) +
				  /^$/.test(d2);

		if (matches == 0) {
			return(0);
		} else {
			return(1);
		};
	};

	dialog = $("#dia").dialog({
		autoOpen: false, modal: true,
		buttons: {
			Save: save,
			Cancel: function () { dialog.mode = ""; dialog.dialog("close"); }
		}
	});

	$("#dia").dialog({ open: dialogFill });

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
		dialog.mode = "filt";
		dialog.dialog("open");
	});

});
