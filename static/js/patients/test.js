
    $('#dataTable').DataTable({
        columnDefs: [{
            orderable: false,
            className: 'select-checkbox',
            targets: 0
        }],
        select: {
            style: 'os',
            selector: 'td:first-child'
        },
        order: [[1, 'asc']]
    });
    $('#select_patient').click(function () {
        var patient = $('#dataTable').rows('.selected').data();
        alert("Name: " + patient[1])
    });