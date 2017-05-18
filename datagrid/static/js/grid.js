/* global $ kendo*/
$(function() {
    var dataSource = new kendo.data.DataSource({
        transport: {
            read: {
                url: "https://mwmtest-gabrielbusta.c9users.io/employees/",
                dataType: "json"
            }
        },
        schema: {
            parse: function(response) {
                var employees = [];
                for (var i = 0; i < response.length; i++) {
                    var employee = {
                        FirstName: response[i].first_name,
                        LastName: response[i].last_name,
                        City: response[i].city,
                        Title: response[i].job_title,
                        BirthDate: new Date(response[i].birth_date),
                    };
                    employees.push(employee);
                }
                return employees;
            }
        },
        pageSize: 100,
        model: {
            fields: {
                FirstName: { type: 'string' },
                LastName: { type: 'string' },
                City: { type: 'string' },
                Title: { type: 'string' },
                BirthDate: { type: 'date'},
            }
        },
    });
    $("#grid").kendoGrid({
        dataSource: dataSource,
        scrollable: true,
        height: window.innerHeight,
        filterable: {
            extra: false,
            operators: {
                string: {
                    startswith: "Starts with",
                    eq: "Is equal to",
                    neq: "Is not equal to"
                }
            }
        },
        pageable: true,
        columns: [{
            title: "Name",
            width: 160,
            filterable: false,
            template: "#=FirstName# #=LastName#"
        }, {
            field: "City",
            width: 130,
            filterable: {
                ui: cityFilter
            }
        }, {
            field: "Title",
            filterable: {
                ui: titleFilter
            }
        }, {
            field: "BirthDate",
            title: "Birth Date",
            format: "{0:MM/dd/yyyy}",
            filterable: {
                ui: "datetimepicker"
            }
        }]
    });
});

function titleFilter(element) {
    element.kendoAutoComplete({
        dataSource: new kendo.data.DataSource({
            transport: {
                read: {
                    url: "https://mwmtest-gabrielbusta.c9users.io/titles/",
                    dataType: "json"
                }
            }
        })
    });
}

function cityFilter(element) {
    element.kendoDropDownList({
        dataSource: new kendo.data.DataSource({
            transport: {
                read: {
                    url: "https://mwmtest-gabrielbusta.c9users.io/cities/",
                    dataType: "json"
                }
            }
        }),
        optionLabel: "--Select Value--"
    });
}