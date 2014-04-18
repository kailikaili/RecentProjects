'use strict';

/* Filters */

angular.module('angcardApp.filters', [])
	.filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    }
  }])
  .filter('statusToHanZi', function() {
  	var statusFilter = function(status) {
  		var hanZi = '';
  		switch (status){
  			case '0':
  				hanZi = '正常';
  				break;
  			case '1':
  			  hanZi = '已禁用';
  			  break;
  		}
  		return hanZi;
  	}
  	return statusFilter;
  })
  .filter('cardStatusToHanZi', function() {
  	var statusFilter = function(status) {
  		var hanZi = '';
  		switch (status){
  			case '0':
  				hanZi = '正常';
  				break;
  			case '1':
  			  hanZi = '新卡未启用';
  			  break;
  			case '3':
  			  hanZi = '冻结';
  			  break;
  			default:
  				handZi = status;
  		}
  		return hanZi;
  	}
  	return statusFilter;
  })
  .filter('orgLevel', function(){
    var levelFilter = function(level) {
      var levelName = '';
      switch (level) {
        case 'unit':
          levelName = '集团级用户';
          break;
        case 'shop':
          levelName = '商户级用户';
          break;
        case 'terminal':
          levelName = '终端操作员'
          break;
      }
      return levelName;
    }
    return levelFilter;
  });
