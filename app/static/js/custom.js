var success_div = '<div class="success-div"><i class="fas fa-check-circle"></i></div>';
var failed_div = '<div class="failed-div"><i class="fas fa-times-circle"></i></div>';
var progress_bar_div = '<div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"  aria-valuemin="0" aria-valuemax="100" style="width: 0%"></div></div>';

var table = $('#recordsTable').DataTable({
    "dom": 'rt<"bottom"ilp><"clear">',
    "pageLength": 15,
    "lengthMenu": [15, 30, 60],
    "order": [
        [0, "desc"]
    ],

    "ajax": {
        "url": "/records",
        "type": "GET",
        "dataSrc": function (json) {
            data = json["data"]
            for (var i = 0; i < data.length; i++) {
                if (data[i].status.toLowerCase() == "in_process") {
                    data[i].status = progress_bar_div;
                } else if (data[i].status.toLowerCase() == "success") {
                    data[i].status = success_div;
                } else if (data[i].status.toLowerCase() == "failed") {
                    data[i].status = failed_div;
                }
                if (data[i].log_path != null) {
                    data[i].log_path = '<div class="report-div"><a href="'+ data[i].log_path +'"><i class="far fa-file-alt"></i></a></div>'
                }
            }
            return data;
        }


    },
    "columns": [{
            "data": "id"
        },
        {
            "data": "name"
        },
        {
            "data": "owner"
        },
        {
            "data": "start_time"
        },
        {
            "data": "end_time"
        },
        {
            "data": "task_id"
        },
        {
            "data": "status"
        },
        {
            "data": "log_path"
        }
    ],
    "columnDefs": [{
            "targets": 5,
            "createdCell": function (td, cellData, rowData, row, col) {
                $(td).addClass('task_id')
            }
        },
        {
            "targets": 6,
            "createdCell": function (td, cellData, rowData, row, col) {
                $(td).addClass('status')
            }

        }
    ],

})
$('#recordSearch').keyup(function () {
    table.search($(this).val()).draw();
})

$.get("/runnigRecords", function (data) {
    for (var i = 0; i < data["runningRecords"].length; i++) {
        var record = data["runningRecords"][i];
        $.each(record, function () {
            var key = Object.keys(this)[0];
            var value = this[key];
        });
        //var statusElement = $("td:contains(" + record["task_id"] + ")").next();
        //var progressHtml = '<div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div></div>';
        //statusElement.empty();
        //statusElement.append(progressHtml);
        update_progress("/task_status", record["task_id"]);
    }

});

/*

$.get("{{url_for('main.runnigRecords')}}", function (data) {
    for (record in data["runningRecords"]) {
        status_url = '{{url_for("main.task_status",task_id="#")}}'.replace("#", record["task_id"])
        update_progress(status_url, record["id"]);

    }
    if (data['state'] == 'SUCCESS') {
        var progressEelem = syncElem.parent().next(".executionSection").find(".progress");
        progressEelem.remove();
        var res =
            '<span class="executionStatus"><a href="#" ><i class="far fa-file-alt"></i></a></span>'
            .replace("#", "http://127.0.0.1:9900/browse/1233")
        syncElem.parent().next(".executionSection").append(res)
    } else {
        setTimeout(function () {
            update_progress(status_url, syncElem);
        }, 2000);
    }
});
    */

$('#selectCaseModal').on('show.bs.modal', function (e) {
    $("#tree").fancytree({
        extensions: ["filter"],
        quicksearch: true,
        focusOnSelect: false,
        filter: {
            autoApply: true, // Re-apply last filter if lazy data is loaded
            autoExpand: false, // Expand all branches that contain matches while filtered
            counter: true, // Show a badge with number of matching child nodes near parent icons
            fuzzy: false, // Match single characters in order, e.g. 'fb' will match 'FooBar'
            hideExpandedCounter: true, // Hide counter badge if parent is expanded
            hideExpanders: false, // Hide expanders if all child nodes are hidden by filter
            highlight: true, // Highlight matches by wrapping inside <mark> tags
            leavesOnly: false, // Match end nodes only
            nodata: true, // Display a 'no data' status node if result is empty
            mode: "hide" // Grayout unmatched nodes (pass "hide" to remove unmatched node instead)

        },
        checkbox: true,
        selectMode: 3,
        source: {
            url: "/cases"
        },
        activate: function (event, data) {
            $("#statusLine").text(event.type + ": " + data.node);
        },
        select: function (event, data) {
            $("#statusLine").text(event.type + ": " + data.node.isSelected() +
                " " + data.node);
        }
    });
})



$("input[name=caseSearch]").keyup(function (e) {
    var n,
        tree = $.ui.fancytree.getTree(),
        args = "autoApply autoExpand fuzzy hideExpanders highlight leavesOnly nodata".split(
            " "),
        opts = {},
        filterFunc = tree.filterNodes,
        match = $(this).val();

    $.each(args, function (i, o) {
        opts[o] = $("#" + o).is(":checked");
    });
    opts.mode = "hide";
    filterFunc.call(tree, match, opts);
}).focus();



// Select a node on click
$("#execute").click(function () {
    var tree = $("#tree").fancytree("getTree");
    var nodes = tree.getSelectedNodes();
    var url = "/async_execute";
    var executingCases = new Array();
    var count = 0;
    for (var i = 0; i < nodes.length; i++) {
        if (!nodes[i].folder) {
            executingCases.push(nodes[i].key);
            count++;
        }
    }
    if ((count > 0 && count < 6)) {
        $.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify({
                "caseList": executingCases
            }),
            contentType: "application/json; charset=utf-8",
            success: function (data) {}
        })
        //$.post(url, {"caseList": executingCases}, function (data, status, request) {});
        $('#selectCaseModal').modal('hide');
        window.location.reload();
    } else if (count > 5) {
        $('.alert .modal-header').prepend('<div style="font-size:1.5em; color:red" id="Title"><i class="fas fa-exclamation-triangle "></i></div>');
        $('.alert .modal-body').prepend('<p>Do not choose more than 5 cases each time!</p>');
        $('.alert').modal("show");
    }

});

function update_progress(status_url, task_id) {
    $.ajax({
        url: status_url,
        type: "GET",
        data: {
            "task_id": task_id
        },
        success: function (data) {
            if (data['state'] == 'PROGRESS') {
                var progressBar = $("td:contains(" + task_id + ")").next().find('.progress-bar');
                percent = parseInt(data['current'] * 100 / data['total']);
                progressBar.width(percent + "%");
                setTimeout(function () {
                    update_progress(status_url, task_id);
                }, 2000);
            } else if (data['state'] == 'SUCCESS') {
                $.post("/update_task", data = {
                    "status": data['state'],
                    "task_id": task_id,
                    "end_time": data['end_time'],
                    "log_path": data['log_path']
                });
                //window.location.reload();
                $("td:contains(" + task_id + ")").prev().text(data['end_time']);
                var statusElement = $("td:contains(" + task_id + ")").next();
                statusElement.empty();
                statusElement.append(success_div);
                var logElement = statusElement.next();
                logElement.append('<div class="report-div"><a href="'+ data['log_path']+'"><i class="far fa-file-alt"></i></a></div>');


            } else {
                setTimeout(function () {
                    update_progress(status_url, task_id);
                }, 2000);
            }
        }


    })
    /*
    $.get(status_url, function(data){
        if (data['state'] == 'SUCCESS'){
            var progressEelem = syncElem.parent().next(".executionSection").find(".progress");
            progressEelem.remove();
            var res = '<span class="executionStatus"><a href="#" ><i class="far fa-file-alt"></i></a></span>'.replace("#","http://127.0.0.1:9900/browse/1233")
            syncElem.parent().next(".executionSection").append(res)
            }
        else {
            setTimeout(function(){
                update_progress(status_url, syncElem);
            },2000);
        }
    });
    */
}