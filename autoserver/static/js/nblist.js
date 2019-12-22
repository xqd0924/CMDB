function init_thead(thead_dic) {
        $.each(thead_dic, function (k,v) {
            th_str = v.title;
            var th = document.createElement('th');
            th.innerText = th_str;
            $('#thead').append(th)
        })
    }
    function init_tbody(data_list, thead_dic) {
        $.each(data_list, function (k,v) {
            var tr = document.createElement('tr');
            $.each(thead_dic, function (k, config_item) {
                var td = document.createElement('td');
                td.innerText = v[config_item['field']];
                tr.append(td)
            });
            $('#tbody').append(tr)
        })
    }