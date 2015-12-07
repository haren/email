require.config({
	paths: {
		jquery: '../libs/jquery/jquery', // 2.1.4
		underscore: '../libs/underscore/underscore', // 1.8.3
		backbone: '../libs/backbone/backbone', // 1.2.3,
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