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

gulp.task('fonts', function(){
  return gulp.src('./node_modules/font-awesome/fonts/*')
    .pipe(gulp.dest('./app/static/fonts/'));
});

gulp.task('img', function(){
	return gulp.src('./front/img/*')
		.pipe(gulp.dest('./app/static/img/'));
});

// Concatenate js
gulp.task('js', function() {
  return gulp.src('./front/js/**.js')
    .pipe(concat('main.js'))
    .pipe(gulp.dest('./app/static/js/'));
});

var vendorJSFiles = [
  './node_modules/jquery/dist/jquery.js',
  // './node_modules/bootstrap/dist/js/bootstrap.js',
  './front/vendor/**/**.js'
];

gulp.task('vendorJS', function(){
  return gulp.src(vendorJSFiles)
    .pipe(concat('vendor.js'))
    .pipe(gulp.dest('./app/static/js/'));
});

var vendorCSSFiles = [
  // './node_modules/bootstrap/dist/css/bootstrap.css',
  './node_modules/font-awesome/css/font-awesome.css',
  './front/vendor/**/**.css'
];

gulp.task('vendorCSS', function(){
  return gulp.src(vendorCSSFiles)
    .pipe(concat('vendor.css'))
    .pipe(gulp.dest('./app/static/css/'));
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('./front/**/*.scss', ['sass']);
    gulp.watch('./front/**/*.js', ['js']);
    gulp.watch('./front/img/**.*', ['img']);
});

gulp.task('build', ['img', 'fonts', 'sass', 'vendorJS', 'vendorCSS', 'js']);
gulp.task('default', ['build', 'watch']);
