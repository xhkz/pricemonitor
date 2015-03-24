$(document).ready(function () {
    $('.right.menu.open').on("click", function (e) {
        e.preventDefault();
        $('.ui.vertical.menu').toggle();
    });

    $('.ui.dropdown').dropdown();

    $("#price_table").DataTable({
        paging: false,
        info: false,
        autoWidth: false,
        columns: [
            null,
            null,
            { searchable: false },
            { searchable: false },
            { searchable: false },
            { searchable: false }
        ]
    });
});