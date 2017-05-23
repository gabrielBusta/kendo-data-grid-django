/* global $ kendo*/
$(function() {
    var employeeDataSource = new kendo.data.DataSource({
        transport: {
            read: {
                url: "https://mwmtest-gabrielbusta.c9users.io/employees/",
                dataType: "json",
            },
        },
        schema: {
            data: function(response) {
                /* Convert the string representation of birth dates into JavaScript Date objects. */
                for (var i = 0; i < response.data.length; i++) {
                    response.data[i].birth_date = new Date(response.data[i].birth_date);
                }
                return response.data;
            },
            total: function(response) {
                return response.total;
            },
        },
        pageSize: 100,
        serverPaging: true,
        serverFiltering: true,
        model: {
            fields: {
                first_name: { type: 'string' },
                last_name: { type: 'string' },
                city: { type: 'string' },
                job_title: { type: 'string' },
                birth_date: { type: 'date'},
            },
        },
    });

    $("#grid").kendoGrid({
        dataSource: employeeDataSource,
        scrollable: true,
        filterable: {
            extra: false,
            operators: {
                string: {
                    eq: "Is equal to",
                    neq: "Is not equal to",
                },
            },
        },
        pageable: true,
        columns:
        [
            {
                /* TODO: Make this column filterable */
                title: "Name",
                width: 160,
                template: "#=first_name# #=last_name#",
            },
            {
                field: "city",
                title: "City",
                width: 130,
                filterable: {
                    ui: cityFilter,
                },
            },
            {
                field: "job_title",
                title: "Title",
                filterable: {
                    ui: titleFilter,
                },
            },
            {
                field: "birth_date",
                title: "Birth Date",
                format: "{0:MM/dd/yyyy}",
                filterable: {
                    ui: "datepicker",
                },
            },
        ],
    });
});

function titleFilter(element) {
    element.kendoAutoComplete({
        dataSource: new kendo.data.DataSource({
            transport: {
                read: {
                    url: "https://mwmtest-gabrielbusta.c9users.io/titles/",
                    dataType: "json",
                },
            },
            schema: {
                data: function(response) {
                    return response.data;
                },
                total: function(response) {
                    return response.total;
                },
            },
        }),
    });
}

function cityFilter(element) {
    element.kendoDropDownList({
        dataSource: new kendo.data.DataSource({
            transport: {
                read: {
                    url: "https://mwmtest-gabrielbusta.c9users.io/cities/",
                    dataType: "json",
                },
            },
            schema: {
                data: function(response) {
                    return response.data;
                },
                total: function(response) {
                    return response.total;
                },
            },
        }),
        optionLabel: "--Select Value--",
    });
}