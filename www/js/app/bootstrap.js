require.config({
	paths: {
		jquery: '../libs/jquery/jquery.min', // 2.1.4
		underscore: '../libs/underscore/underscore.min', // 1.8.3
		backbone: '../libs/backbone/backbone.min', // 1.2.3,
		toastr: '../libs/toastr/toastr.min'
	},
	shim: {
		underscore: {
			exports: '_'
		},
		backbone: {
			deps: ['underscore', 'jquery'],
			exports: 'Backbone'
		},
	}
});

require(['app'], function(App) {
	App.init();
});