$(function () {
    var $wrapper = $('#div-table-container');
    var $table = $('#product_list_table');
    var brand_id = $('#hidden_brand_id').val()

    var _table = $table.dataTable($.extend(true, {}, CONSTANT.DATA_TABLES.DEFAULT_OPTION, {
        ajax: function (data, callback, settings) {//ajax配置为function,手动调用异步查询
            //手动控制遮罩

            //封装请求参数
            var param = productManage.getQueryCondition(data);
            $.ajax({
                type: "GET",
                url: "/api/sparrow_crawl/site/o/product/list/",
                cache: false,  //禁用缓存
                data: param,    //传入已封装的参数
                dataType: "json",
                success: function (result) {
                    //setTimeout仅为测试延迟效果
                    setTimeout(function () {
                        //异常判断与处理
                        if (result.errorCode) {
                            $.dialog.alert("查询失败。错误码：" + result.errorCode);
                            return;
                        }

                        //封装返回数据，这里仅演示了修改属性名
                        var returnData = {};
                        //returnData.draw = 1;//data.draw;//这里直接自行返回了draw计数器,应该由后台返回
                        returnData.recordsTotal = result.count;
                        returnData.recordsFiltered = result.count;//后台不实现过滤功能，每次查询均视作全部结果
                        returnData.data = result.results;
                        //关闭遮罩

                        //调用DataTables提供的callback方法，代表数据已封装完成并传回DataTables进行渲染
                        //此时的数据需确保正确无误，异常判断应在执行此回调前自行处理完毕
                        callback(returnData);
                    }, 200);
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    $.dialog.alert("查询失败");

                }
            });
        },
        columns: [
            CONSTANT.DATA_TABLES.COLUMN.CHECKBOX,
            {
                className: "ellipsis", //文字过长时用省略号显示，CSS实现
                data: "sku",
                width: "45px"
                //render: CONSTANT.DATA_TABLES.RENDER.ELLIPSIS,//会显示省略号的列，需要用title属性实现划过时显示全部文本的效果
            },

            {
                className: "ellipsis",
                data: "title",
                render: CONSTANT.DATA_TABLES.RENDER.ELLIPSIS,
                //固定列宽，但至少留下一个活动列不要固定宽度，让表格自行调整。不要将所有列都指定列宽，否则页面伸缩时所有列都会随之按比例伸缩。
                //切记设置table样式为table-layout:fixed; 否则列宽不会强制为指定宽度，也不会出现省略号。
                width: "80px"
            },
            {
                data: "colors",
                width: "80px"
            },
            {
                data: "url",
                width: "30px",
                render: function (data, type, row, meta) {
                    return '<a href="{{ data }}" target="_blank"><i class="fa fa-paperclip"></i></a>';
                }
            },
            {
                className: "td-operation",
                data: null,
                defaultContent: "",
                orderable: false,
                width: "120px"
            }
        ],
        "createdRow": function (row, data, index) {
            //行渲染回调,在这里可以对该行dom元素进行任何操作
            //给当前行加样式

            //不使用render，改用jquery文档操作呈现单元格
            var $btnView = $('<button type="button" class="btn btn-small btn-primary btn-edit">详情</button>');
            var $btnDel = $('<button type="button" class="btn btn-small btn-danger btn-del">删除</button>');
            $('td', row).eq(5).append($btnView).append($btnDel);
        },
        "drawCallback": function (settings) {
            //渲染完毕后的回调
            //清空全选状态
            $(":checkbox[name='cb-check-all']", $wrapper).prop('checked', false);
            //默认选中第一行
            $("tbody tr", $table).eq(0).click();
        }
    })).api();//此处需调用api()方法,否则返回的是JQuery对象而不是DataTables的API对象

    $("#import_file_input1").fileinput({
        showUpload: true,
        //showCaption: false,
        theme: "explorer-fa",
        showPreview: false,
        dropZoneEnabled: true,
        removeClass: "btn btn-primary",
        uploadClass: "btn btn-primary",
        browseClass: "btn btn-primary",
        allowedFileExtensions: ['xls', 'xlsx'],
        previewFileIcon: "<i class='glyphicon glyphicon-king'></i>",
        showRemove: true,
        uploadUrl: '/api/sparrow_crawl/site/o/import/productlist/',
        initialPreviewConfig: [],
        fileActionSettings: {                               // 在预览窗口中为新选择的文件缩略图设置文件操作的对象配置
            showRemove: true,                                   // 显示删除按钮
            showUpload: true,                                   // 显示上传按钮
            showDownload: false,                            // 显示下载按钮
            showZoom: false,                                    // 显示预览按钮
            showDrag: false,                                        // 显示拖拽
            removeIcon: '<i class="fa fa-trash"></i>',   // 删除图标
            uploadIcon: '<i class="fa fa-upload"></i>',     // 上传图标
            uploadRetryIcon: '<i class="fa fa-repeat"></i>'  // 重试图标
        },
        uploadExtraData:
            function () {  // uploadExtraData携带附加参数，上传时携带brand_id
                return {
                    brand_id: $('#brand_id_input').val()
                }
            }
    });


//     $("#btn-add").click(function(){
//         userManage.addItemInit();
//     });
//
//     $("#btn-del").click(function(){
//         var arrItemId = [];
//         $("tbody :checkbox:checked",$table).each(function(i) {
//             var item = _table.row($(this).closest('tr')).data();
//             arrItemId.push(item);
//         });
//         userManage.deleteItem(arrItemId);
//     });
//
    $("#btn-simple-search").click(function () {
        //reload效果与draw(true)或者draw()类似,draw(false)则可在获取新数据的同时停留在当前页码,可自行试验
//      _table.ajax.reload();
//      _table.draw(false);
        _table.draw();
    });
//
//     $("#btn-advanced-search").click(function(){
//         userManage.fuzzySearch = false;
//         _table.draw();
//     });
//
//     $("#btn-save-add").click(function(){
//         userManage.addItemSubmit();
//     });
//
//     $("#btn-save-edit").click(function(){
//         userManage.editItemSubmit();
//     });
//
//     //行点击事件
//     $("tbody",$table).on("click","tr",function(event) {
//         $(this).addClass("active").siblings().removeClass("active");
//         //获取该行对应的数据
//         var item = _table.row($(this).closest('tr')).data();
//         userManage.currentItem = item;
//         userManage.showItemDetail(item);
//     });
//
//     $table.on("change",":checkbox",function() {
//         if ($(this).is("[name='cb-check-all']")) {
//             //全选
//             $(":checkbox",$table).prop("checked",$(this).prop("checked"));
//         }else{
//             //一般复选
//             var checkbox = $("tbody :checkbox",$table);
//             $(":checkbox[name='cb-check-all']",$table).prop('checked', checkbox.length == checkbox.filter(':checked').length);
//         }
//     }).on("click",".td-checkbox",function(event) {
//         //点击单元格即点击复选框
//         !$(event.target).is(":checkbox") && $(":checkbox",this).trigger("click");
//     }).on("click",".btn-edit",function() {
//         //点击编辑按钮
//         var item = _table.row($(this).closest('tr')).data();
//         $(this).closest('tr').addClass("active").siblings().removeClass("active");
//         userManage.currentItem = item;
//         userManage.editItemInit(item);
//     }).on("click",".btn-del",function() {
//         //点击删除按钮
//         var item = _table.row($(this).closest('tr')).data();
//         $(this).closest('tr').addClass("active").siblings().removeClass("active");
//         userManage.deleteItem([item]);
//     });
//
    $("#toggle-advanced-search").click(function () {
        $("i", this).toggleClass("fa-angle-double-down fa-angle-double-up");
        $("#div-advanced-search").slideToggle("fast");
    });

    $.ajax({
            url: 'https://backend5.hanguangbaihuo.com/api/sparrow_admin/brands_for_filter/?page_size=10000',
            type: "GET",
            success: function (resp) {
                let array = new Array();
                if (resp.results) {
                    for (var i = 0; i < resp.results.length; i++) {
                        var brand = resp.results[i];
                        one = {id: brand.id, text: brand.name};
                        array.push(one);
                    }
                }
                let _brand_select = $('.select2').select2({
                    data: array
                });
                _brand_select.val(brand_id).trigger("change")
            }
        }
    );

    $('#select-brand').on('select2:select', function (e) {
        var data = e.params.data;
        console.log(data);
        brand_id = data.id;
        $('#hidden_brand_id').val(data.id)
        _table.draw()
    });
    // $('.select2').select2({
    //         ajax: {
    //             url: 'https://backend5.hanguangbaihuo.com/api/sparrow_admin/brands_for_filter/?page_size=10000',
    //             dataType: 'json',
    //             processResults: function (resp) {
    //                 var array = new Array();
    //                 if (resp.results) {
    //                     for (var i = 0; i < resp.results.length; i++) {
    //                         var brand = resp.results[i];
    //                         one = {id: brand.id, text: brand.name};
    //                         if (brand.id == brand_id) {
    //                             one['selected'] = "selected";
    //                             console.log(one)
    //                         } else one['selected'] = false;
    //                         array.push(one);
    //                     }
    //                 }
    //                 var ret = new Object();
    //                 ret.results = array;
    //                 return ret;
    //             },
    //             cache: true
    //         }
    //     }
    // );
//
//     $("#btn-info-content-collapse").click(function(){
//         $("i",this).toggleClass("fa-minus fa-plus");
//         $("span",this).toggle();
//         $("#user-view .info-content").slideToggle("fast");
//     });
//
//     $("#btn-view-edit").click(function(){
//         userManage.editItemInit(userManage.currentItem);
//     });
//
//     $(".btn-cancel").click(function(){
//         userManage.showItemDetail(userManage.currentItem);
//     });
});

var productManage = {
    currentItem: null,
    fuzzySearch: true,
    getQueryCondition: function (data) {
        var param = {};
        //组装排序参数
        if (data.order && data.order.length && data.order[0]) {
            switch (data.order[0].column) {
                case 1:
                    param.orderColumn = "sku";
                    break;
                default:
                    param.orderColumn = "title";
                    break;
            }
            param.orderDir = data.order[0].dir;
        }
        //组装分页参数
        param.start = data.start;
        param.length = data.length;

        //组装brand_id
        let brand_id = $('#hidden_brand_id').val()
        //console.log(brand_id)
        if (brand_id && brand_id!='None') {
            brand_id = brand_id.trim()
            if (brand_id.length > 0) {
                param.brand_id = brand_id;
            }
        }
        //组装简单模糊查询
        let fuzzy = $("#fuzzy-search").val()
        if (fuzzy) {
            console.log(fuzzy)
            fuzzy = fuzzy.trim()
            if (fuzzy.length > 0)
                param.query = fuzzy;
        }
        return param;
    }
};
// var userManage = {
//     currentItem : null,
//     fuzzySearch : true,
//     getQueryCondition : function(data) {
//         var param = {};
//         //组装排序参数
//         if (data.order&&data.order.length&&data.order[0]) {
//             switch (data.order[0].column) {
//             case 1:
//                 param.orderColumn = "name";
//                 break;
//             case 2:
//                 param.orderColumn = "position";
//                 break;
//             case 3:
//                 param.orderColumn = "status";
//                 break;
//             case 4:
//                 param.orderColumn = "start_date";
//                 break;
//             default:
//                 param.orderColumn = "name";
//                 break;
//             }
//             param.orderDir = data.order[0].dir;
//         }
//         //组装查询参数
//         param.fuzzySearch = userManage.fuzzySearch;
//         if (userManage.fuzzySearch) {
//             param.fuzzy = $("#fuzzy-search").val();
//         }else{
//             param.name = $("#name-search").val();
//             param.position = $("#position-search").val();
//             param.office = $("#office-search").val();
//             param.extn = $("#extn-search").val();
//             param.status = $("#status-search").val();
//             param.role = $("#role-search").val();
//         }
//         //组装分页参数
//         param.startIndex = data.start;
//         param.pageSize = data.length;
//
//         return param;
//     },
//     showItemDetail : function(item) {
//         $("#user-view").show().siblings(".info-block").hide();
//         if (!item) {
//             $("#user-view .prop-value").text("");
//             return;
//         }
//         $("#name-view").text(item.name);
//         $("#position-view").text(item.position);
//         $("#salary-view").text(item.salary);
//         $("#start-date-view").text(item.start_date);
//         $("#office-view").text(item.office);
//         $("#extn-view").text(item.extn);
//         $("#role-view").text(item.role?"管理员":"操作员");
//         $("#status-view").text(item.status?"在线":"离线");
//     },
//     addItemInit : function() {
//         $("#form-add")[0].reset();
//
//         $("#user-add").show().siblings(".info-block").hide();
//     },
//     editItemInit : function(item) {
//         if (!item) {
//             return;
//         }
//         $("#form-edit")[0].reset();
//         $("#title-edit").text(item.name);
//         $("#name-edit").val(item.name);
//         $("#position-edit").val(item.position);
//         $("#salary-edit").val(item.salary);
//         $("#start-date-edit").val(item.start_date);
//         $("#office-edit").val(item.office);
//         $("#extn-edit").val(item.extn);
//         $("#role-edit").val(item.role);
//         $("#user-edit").show().siblings(".info-block").hide();
//     },
//     addItemSubmit : function() {
//         $.dialog.tips('保存当前添加用户');
//     },
//     editItemSubmit : function() {
//         $.dialog.tips('保存当前编辑用户');
//     },
//     deleteItem : function(selectedItems) {
//         var message;
//         if (selectedItems&&selectedItems.length) {
//             if (selectedItems.length == 1) {
//                 message = "确定要删除 '"+selectedItems[0].name+"' 吗?";
//
//             }else{
//                 message = "确定要删除选中的"+selectedItems.length+"项记录吗?";
//             }
//             $.dialog.confirmDanger(message, function(){
//                 $.dialog.tips('执行删除操作');
//             });
//         }else{
//             $.dialog.tips('请先选中要操作的行');
//         }
//     }
// };