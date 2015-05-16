var gulp        =  require('gulp'),
	  rename      = require('gulp-rename'),
	  concat      = require('gulp-concat'),
    sass        = require('gulp-sass');

from = './app/front/'
to = './app/static/'

gulp.task('sass', function(){
	return gulp.src('./front/sass/main.scss')
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest('./app/static/css'));
});

gulp.task('glyphicons', function(){
	return gulp.src('./node_modules/bootstrap/fonts/*')
		.pipe(gulp.dest('./app/static/fonts/'));
});

gulp.task('img', function(){
	return gulp.src('./front/img/*')
		.pipe(gulp.dest('./app/static/img/'));
});


var vendorCSSFiles = [
				'./node_modules/jquery/dist/css/bootstrap.min.css',
				];
gulp.task('vendorCSS', function(){
	return gulp.src('./node_modules/bootstrap/dist/css/bootstrap.min.css')
    .pipe(rename('vendor.css'))
		.pipe(gulp.dest('./app/static/css/'));
});

var jsFiles = [
  './front/js/main.js'
];
// Concatenate js
gulp.task('js', function() {
	return gulp.src(jsFiles)
		.pipe(concat('main.js'))
		.pipe(gulp.dest('./app/static/js/'));
});

var vendorJSFiles = [
				'./node_modules/jquery/dist/jquery.js',
				'./node_modules/bootstrap/dist/js/bootstrap.js',
        './front/js/lib/*.js'
				];

gulp.task('vendorJS', function(){
	return gulp.src(vendorJSFiles)
		.pipe(concat('vendor.js'))
		.pipe(gulp.dest('./app/static/js/'));
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('./front/**/*.scss', ['sass']);
    gulp.watch('./front/**/*.js', ['js']);
});

gulp.task('build', ['img', 'glyphicons', 'vendorCSS', 'sass', 'vendorJS', 'js']);
gulp.task('default', ['build', 'watch']);

