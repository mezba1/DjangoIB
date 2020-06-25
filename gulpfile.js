'use strict';

const { src, dest, watch } = require('gulp');
const browserify = require('browserify');
const uglify = require('gulp-uglify');
const rename = require('gulp-rename');
const sass = require('gulp-sass');
const cleanCss = require('gulp-clean-css');
const source = require('vinyl-source-stream');
const buffer = require('vinyl-buffer');

sass.compiler = require('node-sass');

const paths = {
  js: ['./assets/js/app.js'],
  scss: ['assets/scss/app.scss'],
};

function js() {
  return browserify(paths.js)
    .transform('babelify', { presets: ['@babel/preset-env'] })
    .bundle()
    .pipe(source('app.js'))
    .pipe(buffer())
    .pipe(uglify({
      compress: true,
      mangle: { toplevel: true },
    }))
    .pipe(rename({ extname: '.min.js' }))
    .pipe(dest('src/static/js'));
}

function scss() {
  return src(paths.scss)
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCss())
    .pipe(rename({ extname: '.min.css' }))
    .pipe(dest('src/static/css'));
}

exports.default = () => {
  watch(paths.scss, scss);
  watch(paths.js, js);
}
