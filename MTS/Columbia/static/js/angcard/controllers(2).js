'use strict';

/* Controllers */

angular.module('angcardApp.controllers', [])

    .controller('OnlineCtrl', ['$scope', '$http', function ($scope, $http) {

        $scope.submit = function (form) {
		
		    $scope.r_google = 'Loading...';
			$scope.r_bing = 'Loading...';
			$scope.r_youdao = 'Loading...';
			$scope.r_best = 'Calculating...';
		
		    var bestparams = {};
            // 向服务请求 Google 的翻译结果
            $http.get('/google', {params: form}).success(function(result){
               // 将翻译的结果赋值给 r_google (result_google的缩写)
                $scope.r_google = result.translate_result;
				bestparams.google = result.translate_result;
            });

            // 向服务请求 Bing 的翻译结果
            $http.get('/bing', {params: form}).success(function(result){
                $scope.r_bing = result.translate_result;
				bestparams.bing = result.translate_result;
            });

            // 向服务请求 Youdao 的翻译结果
            $http.get('/youdao', {params: form}).success(function(result){
                $scope.r_youdao = result.translate_result;
				bestparams.youdao = result.translate_result
            });

			function submitBest() {
                // 需要google, bing, youdao 3个参数， 所以要定义一下需要的参数长度
                // 当达到所有参数都存在的条件时（bestparamsLength == 3），就向服务器提交数据
                
				
				var bestparamsLength = 0;

                // 计算bestparams里有多少个参数，并将结果赋给bestparamsLength
                angular.forEach(bestparams, function(value, key){
                                            bestparamsLength += 1;
                                        });

                // 达到条件，提交数据
                if (bestparamsLength == 3) {                    

                    // 发送请求:
                    // 将 form 与 best2params 合并后发给服务器
                    // 后台就可以通过i.get('sri') 获取参数
                    angular.forEach(bestparams, function(value, key){
                                            form[key] = value;
                                        });

                    $http.get('/best', {params: form}).success(function(result){
                        $scope.r_best = result.translate_result;
                    }); 

                    // 清空参数，防止无限循环地发送请求                    
                    bestparams = {};
                }
            }

            //每3秒执行一次submitBest
            window.setInterval(submitBest, 3000); 
        }

    }])


    .controller('OfflineCtrl', ['$scope', '$http', function ($scope, $http) {
        
        // 请求txtdb, 用于下拉菜单
        $http.get('/txtdb').success(function(result){
            $scope.txtdb = result.txtdb;
        });

        $scope.showEN = function(index){
            $scope.EN = $scope.txtdb[index-1]['en_row'];
        }

        $scope.submit = function (form) {
		
		    $scope.r_google = 'Loading...';
			$scope.r_bing = 'Loading...';
			$scope.r_youdao = 'Loading...';
			$scope.r_best = 'Calculating...';
		
		    var bestparams = {};
            // 向服务请求 Google 的翻译结果
            $http.get('/google', {params: form}).success(function(result){
               // 将翻译的结果赋值给 r_google (result_google的缩写)
                $scope.r_google = result.translate_result; 
				bestparams.google = result.translate_result;
            });

            // 向服务请求 Bing 的翻译结果
            $http.get('/bing', {params: form}).success(function(result){
                $scope.r_bing = result.translate_result;
				bestparams.bing = result.translate_result;
            });

            // 向服务请求 Youdao 的翻译结果
            $http.get('/youdao', {params: form}).success(function(result){
                $scope.r_youdao = result.translate_result;
				bestparams.youdao = result.translate_result;
            });

			
			function submitBest() {
                // 需要google, bing, youdao 3个参数， 所以要定义一下需要的参数长度
                // 当达到所有参数都存在的条件时（bestparamsLength == 3），就向服务器提交数据
				
				var bestparamsLength = 0;

                // 计算bestparams里有多少个参数，并将结果赋给bestparamsLength
                angular.forEach(bestparams, function(value, key){
                                            bestparamsLength += 1;
                                        });

                // 达到条件，提交数据
                if (bestparamsLength == 3) {                    

                    // 发送请求:
                    // 将 form 与 best2params 合并后发给服务器
                    // 后台就可以通过i.get('sri') 获取参数
                    angular.forEach(bestparams, function(value, key){
                                            form[key] = value;
                                        });

                    $http.get('/best', {params: form}).success(function(result){
                        $scope.r_best = result.translate_result;
                    }); 

                    // 清空参数，防止无限循环地发送请求                    
                    bestparams = {};
                }
            }

            //每3秒执行一次submitBest
            window.setInterval(submitBest, 3000); 
        }

    }])


    .controller('Offline2Ctrl', ['$scope', '$http', function ($scope, $http) {
        
        // 请求txtdb, 用于下拉菜单
        $http.get('/txtdb').success(function(result){
            $scope.txtdb = result.txtdb;
        });

        $scope.showEN = function(index){
            $scope.EN = $scope.txtdb[index-1]['en_row'];
            $scope.CN = $scope.txtdb[index-1]['row'];
        }

        $scope.submit = function (form) {
		
		    $scope.r_nrc = 'Loading...';
			$scope.r_pbt = 'Loading...';
			$scope.r_aml = 'Loading...';
			$scope.r_jx = 'Loading...';
			$scope.r_sh = 'Loading...';
			$scope.r_pbt = 'Loading...';
			$scope.r_best2 = 'Calculating...';
			
            var best2params = {};

            $scope.translation = {};

            // 向服务请求 nrc 的翻译结果
            $http.get('/nrc', {params: form}).success(function(result){
               // 将翻译的结果赋值给 r_google (result_google的缩写)
                $scope.r_nrc = result.translate_result;
                $scope.translation.NRC = $scope.r_nrc;
                best2params.nrc = result.translate_result;
            });

            // 向服务请求 pbt 的翻译结果
            $http.get('/pbt', {params: form}).success(function(result){
                $scope.r_pbt = result.translate_result;
                $scope.translation.RWTH_PBT = $scope.r_pbt;
                best2params.pbt = result.translate_result;
            });

            // 向服务请求 aml 的翻译结果
            $http.get('/aml', {params: form}).success(function(result){
                $scope.r_aml = result.translate_result;
                $scope.RWTH_PBT_AML = $scope.r_aml;
                best2params.aml = result.translate_result;
            });

            // 向服务请求 jx 的翻译结果
            $http.get('/jx', {params: form}).success(function(result){
                $scope.r_jx = result.translate_result;
                $scope.translation.RWTH_PBT_JX = $scope.r_jx;
                best2params.jx = result.translate_result;
            });

            // 向服务请求 sh 的翻译结果
            $http.get('/sh', {params: form}).success(function(result){
                $scope.r_sh = result.translate_result;
                $scope.translation.RWTH_PBT_SH = $scope.r_sh;
                best2params.sh = result.translate_result;
            });

            // 向服务请求 sri 的翻译结果
            $http.get('/sri', {params: form}).success(function(result){
                $scope.r_sri = result.translate_result;
                $scope.translation.SRI_HPBT = $scope.r_sri;
                best2params.sri = result.translate_result;
            });            

            
            function submitBest2() {
                // 需要nrc, pbt, aml, jx, sh, sri 6个参数， 所以要定义一下需要的参数长度
                // 当达到所有参数都存在的条件时（best2paramsLength == 6），就向服务器提交数据
                var best2paramsLength = 0;

                // 计算best2params里有多少个参数，并将结果赋给best2paramsLength
                angular.forEach(best2params, function(value, key){
                                            best2paramsLength += 1;
                                        });

                // 达到条件，提交数据
                if (best2paramsLength == 6) {                    

                    // 发送请求:
                    // 将 form 与 best2params 合并后发给服务器
                    // 后台就可以通过i.get('sri') 获取参数
                    angular.forEach(best2params, function(value, key){
                                            form[key] = value;
                                        });

                    $http.get('/best2', {params: form}).success(function(result){
                        $scope.r_best = result.translate_result;
                        
                        // 向服务器请求 dependency analysis 结果
                        $http.get('/dependency').success(function(result){
                            $scope.r_dependency = result;
                        });
                    }); 

                    // 清空参数，防止无限循环地发送请求                    
                    best2params = {};
                }            
            }

            //每3秒执行一次submitBest2 
            window.setInterval(submitBest2, 3000); 

        }

    }])