var gulp        =  require('gulp'),
    gutil       =  require('gulp-util'),
    concat      =  require('gulp-concat'),
    connect     =  require('gulp-connect'),
    sass        =  require('gulp-sass'),
    jshint      =  require('gulp-jshint'),
    stylish     =  require('jshint-stylish'),
    cssmin      =  require('gulp-minify-css'),
    htmlmin     =  require('gulp-minify-html'),
    uglify      =  require('gulp-uglify'),
    streamify   =  require('gulp-streamify'),
    browserify  =  require('browserify'),
    source      =  require('vinyl-source-stream'),
    rename      =  require('gulp-rename');



/** PATHS
  *
  *
  */
var app = './app/';
var dest = app + 'static/';
var src = './src/';



/** SASS
  *
  *
  */
gulp.task('sass', function(){
  return gulp.src(src + 'sass/main.scss')
    .pipe(sass())
    .pipe(gulp.dest(dest + 'css'));
    // .pipe(connect.reload());
});


// gulp.task('copy', function(){
//   return gulp.src([
//     appstatic + 'favicon.ico',
//     ])
//     .pipe(gulp.dest(diststatic));
// });

// gulp.task('fonts', function(){
//   return gulp.src(appstatic + 'fonts/*')
//     .pipe(gulp.dest(diststatic + 'fonts/'));
// });

// // JS error checking
// gulp.task('lint', function() {
// return gulp.src(['./gulpfile.js', 
//   './app/js/**/*.js'])
//       .pipe(jshint())
//       .pipe(jshint.reporter());
// });

// // Concatenate & Minify JS
// gulp.task('js', ['lint'], function() {
//   return browserify('./app/js/main.js')
//     .bundle({ debug: true })
//     .pipe(source('bundle.js'))
//     .pipe(gulp.dest(appstatic + 'js'))
//     .pipe(gulp.dest(diststatic + 'js'))
//     .pipe(connect.reload());
// });

// var vendorEntryFiles = [
//         './node_modules/jquery/dist/jquery.js',
//         './node_modules/bootstrap/dist/js/bootstrap.js',
//         ];

// gulp.task('vendor', function(){
//   gulp.src(vendorEntryFiles)
//     .pipe(concat('vendor.js'))
//     .pipe(gulp.dest(appstatic + 'js/'))
//     .pipe(gulp.dest(diststatic + 'js/'));
// });

// gulp.task('glyphicons', function(){
//   return gulp.src('./node_modules/bootstrap/fonts/*')
//     .pipe(gulp.dest('./app/static/fonts/'))
//     .pipe(gulp.dest('./dist/static/fonts/'));
// });


// gulp.task('html', function() {
//   gulp.src(appdir + '*.html')
//     .pipe(htmlmin({
//       comments: true,
//       conditionals: true
//     })).pipe(cssmin())
//     .pipe(gulp.dest(distdir))
//     .pipe(connect.reload());
// });

// // Watch Files For Changes
// gulp.task('watch', function() {
//     gulp.watch(appdir + '*.html', ['html', 'copy']);
//     gulp.watch([appdir + 'js/**/*.js', appdir + 'js/**/*.hbs'], ['js']);
//     gulp.watch(appdir + 'less/**/*.less', ['less']);
// });


// gulp.task('connect', function(){
//   connect.server({
//     port: '3000',
//     root: 'app',
//     livereload: true
//   });
// });


// gulp.task('build', ['copy', 'html', 'less', 'vendor', 'glyphicons', 'js']);
// gulp.task('default', ['build', 'connect', 'watch']);