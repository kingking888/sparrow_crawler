$(function () {
    var $wrapper = $('#div-table-container');
    var $table = $('#brand_list_table');

    var _table = $table.dataTable($.extend(true, {}, CONSTANT.DATA_TABLES.DEFAULT_OPTION, {
        ajax: function (data, callback, settings) {//ajax配置为function,手动调用异步查询
            //手动控制遮罩

            //封装请求参数
            var param = productManage.getQueryCondition(data);
            $.ajax({
                type: "GET",
                url: "https://backend5.hanguangbaihuo.com/api/sparrow_admin/simple_brands/",
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
            {
                className: "ellipsis", //文字过长时用省略号显示，CSS实现
                data: "id",
                width: "45px"
                //render: CONSTANT.DATA_TABLES.RENDER.ELLIPSIS,//会显示省略号的列，需要用title属性实现划过时显示全部文本的效果
            },

            {
                data: "name"
            },
            {
                data: "name_en"
            },
            {
                data: "name_pinyin"
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

            _new='<a href="/api/sparrow_crawl/t/product/list/?brand_id='+data['id']+'">商品</a>';
            console.log(_new)
            var $btnView = $(_new);
            $('td', row).eq(4).append($btnView);

        }
    })).api();//此处需调用api()方法,否则返回的是JQuery对象而不是DataTables的API对象

    _table.on("click", ".btn-products", function () {
        var item = _table.row($(this).closest('tr')).data();
        $(this).closest('tr').addClass("active").siblings().removeClass("active");
        userManage.deleteItem([item]);
    });
    $("#btn-simple-search").click(function () {

        //reload效果与draw(true)或者draw()类似,draw(false)则可在获取新数据的同时停留在当前页码,可自行试验
//      _table.ajax.reload();
//      _table.draw(false);
        _table.draw();
    });

    $("#btn-simple-clear").click(function () {
        $("#name-search").val('')
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
//     $("#toggle-advanced-search").click(function(){
//         $("i",this).toggleClass("fa-angle-double-down fa-angle-double-up");
//         $("#div-advanced-search").slideToggle("fast");
//     });
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
                    param.orderColumn = "id";
                    break;
                default:
                    param.orderColumn = "name";
                    break;
            }
            param.orderDir = data.order[0].dir;
        }
        param.name = $("#name-search").val();
        //组装分页参数
        param.page = data.start / data.length + 1;
        param.page_size = data.length;

        return param;
    }
};
