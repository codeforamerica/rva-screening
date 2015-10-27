var gulp     = require('gulp'),
	  rename   = require('gulp-rename'),
	  concat   = require('gulp-concat'),
    sass     = require('gulp-sass'),
    karma    = require('gulp-karma');

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
  return gulp.src('./front/js/**/*.js')
    .pipe(concat('main.js'))
    .pipe(gulp.dest('./app/static/js/'));
});

var vendorJSFiles = [
  './node_modules/jquery/dist/jquery.js',
  './node_modules/fuse.js/src/fuse.js',
  './front/vendor/**/**.js'
];

gulp.task('vendorJS', function(){
  return gulp.src(vendorJSFiles)
    .pipe(concat('vendor.js'))
    .pipe(gulp.dest('./app/static/js/'));
});

var vendorCSSFiles = [
  './node_modules/font-awesome/css/font-awesome.css',
  './front/vendor/**/**.css'
];

gulp.task('vendorCSS', function(){
  return gulp.src(vendorCSSFiles)
    .pipe(concat('vendor.css'))
    .pipe(gulp.dest('./app/static/css/'));
});

var vendorIMG = [
  './front/vendor/mapbox/images/**/**.*' // specifically to get mapbox icons into the proper folders
];

gulp.task('vendorIMG', function(){
  return gulp.src(vendorIMG)
    .pipe(gulp.dest(to + '/css/images'));
});

var testFiles = [
  './tests/front/es5-shim.js',
  './tests/front/helpers.js',
  './app/static/js/vendor.js',
  './front/js/**/*.js',
  './tests/front/spec/**/*.spec.js'
];

gulp.task('test', function() {
  return gulp.src(testFiles)
    .pipe(karma({
      configFile: './tests/front/karma.conf.js',
      action: 'run'
    }))
    .on('error', function(err) {
      throw err;
    });
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('./front/**/*.scss', ['sass']);
    gulp.watch('./front/**/*.js', ['js']);
    gulp.watch('./front/img/**.*', ['img']);
});

gulp.task('build', ['img', 'fonts', 'sass', 'vendorIMG', 'vendorJS', 'vendorCSS', 'js']);
gulp.task('default', ['build', 'watch']);
