'use strict';


// Declare app level module which depends on filters, and services
angular.module('angcardApp', [
  'ngRoute',
  'angcardApp.filters',
  'angcardApp.services',
  'angcardApp.directives',
  'angcardApp.controllers',
  'ngBootstrap'
]).
config(['$routeProvider', function($routeProvider) {
  var baseUrl = '/static/partials';
  $routeProvider.when('/online', {templateUrl: baseUrl + '/online.html', controller: 'OnlineCtrl'});
  $routeProvider.when('/offline', {templateUrl: baseUrl + '/offline.html', controller: 'OfflineCtrl'});
  $routeProvider.when('/offline_2', {templateUrl: baseUrl + '/offline_2.html', controller: 'Offline2Ctrl'});
  $routeProvider.otherwise({redirectTo: '/online'});
}]);
