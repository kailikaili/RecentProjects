'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('angcardApp.services', ['ngResource'])
    .factory('Form', ['$http', function ($http) {        
        return {
            submit: function(url, data, msg, method) {
                var confirm_flag = false;
                var confirm_result = true;
                if (msg != null && msg != 'undefined' && msg != '') {
                    confirm_flag = true;
                }

                if (confirm_flag) {
                    if (confirm(msg) == true) {
                        confirm_result = true;
                    }else{
                        return;
                    }
                }

                if (confirm_result) {
                    $http ({
                        method: method,
                        url: url,
                        data: jQuery.toJSON(data),                        
                    }).success(function(data){
                        alert(data.msg);
                        return data.success;                        
                    });
                }
            }    
        };
    }])
    .factory('Store',function ($resource) {
        return {
            user: $resource('/user'),
            userList: $resource('/user/list'),
            operator: $resource('/operator'),
            operatorList: $resource('/operator/list'),
            unit: $resource('/unit'),
            unitList: $resource('/unit/list'),
            shop: $resource('/shop'),
            shopList: $resource('/shop/list'),
            terminal: $resource('/terminal'),
            terminalList: $resource('/terminal/list'),
            cardList: $resource('/card/list'),
            cardTrans: $resource('/card/trans'),

            getTransDim: function(){
                return [{trans_code: '000110', trans_name: '卡启用'},
                        {trans_code: '000010', trans_name: '消费'},
                        {trans_code: '000020', trans_name: '消费撤销'},
                        {trans_code: '000030', trans_name: '充值'},
                        {trans_code: '000040', trans_name: '充值撤销'},
                        {trans_code: '000050', trans_name: '积分消费'},
                        {trans_code: '000060', trans_name: '积分消费撤销'},
                        {trans_code: '000070', trans_name: '积分充值'},
                        {trans_code: '000080', trans_name: '积分充值撤销'}];
            }
        }
    })
    .factory('Pagination', function(){
        return function(total, page, limit){

            var pagerSize = 10;  // 每页显示10个跳转
            var totalPage = total % limit == 0? total/limit: total/limit + 1;  // 共多少页
            var startPage = ((page - 1) / limit) * limit + 1;  // 开始序号
            if (startPage > pagerSize) {
                startPage -= 1;
            }
            var endPage = startPage + pagerSize;  
            if (endPage > totalPage) endPage = totalPage;            
            
            var pager = {};
            // pager.total = total;
            // pager.page = page;
            // pager.limit = limit;
            // pager.startPage = startPage;
            // pager.endPage = endPage;
            pager.pages = [];
            pager.pages.push({'page': 1, label: '首页'});
            for(var i=startPage; i<endPage; i++){
                pager.pages.push({'page': i, 'label': i});
            }               
            pager.pages.push({'page': totalPage, label: '末页'});
            return pager;
        };
    })    
;