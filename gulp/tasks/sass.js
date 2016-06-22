'use strict';

import _ from 'underscore';
import bourbon from 'bourbon';
import browserSync from 'browser-sync';
import gulp from 'gulp';
import gulpConfig from '../../gulp.config';
import gutil from 'gulp-util';
import path from 'path';
import sass from 'gulp-sass';
import sourcemaps from 'gulp-sourcemaps';
import {err} from '../common';

const paths = {
  src: path.join(gulpConfig.dirs.src, gulpConfig.tasks.css.src, `/**/*.{${gulpConfig.tasks.css.extensions}}`),
  dest: path.join(gulpConfig.dirs.dest, gulpConfig.tasks.css.dest),
  layout: path.join(gulpConfig.dirs.dev, gulpConfig.tasks.css.dest)
};

const context = gutil.env.layout ? 'sass:layout' : 'sass';

const reload = browserSync.reload;

gulpConfig.tasks.css.sass.includePaths = _.extend(gulpConfig.tasks.css.sass.includePaths, bourbon.includePaths);

const sassCommon = callback => (
  gulp.src(paths.src)
  .pipe(
    sourcemaps.init()
  )
  .pipe(
    sass(gulpConfig.tasks.css.sass)
    .on('error', err('sass', callback))
  )
  .pipe(
    sourcemaps.write()
  )
);

gulp.task('sass', callback => (
  sassCommon(callback, false)
  .pipe(
    gulp.dest(paths.dest)
  )
));

gulp.task('sass:layout', callback => (
  sassCommon(callback)
  .pipe(
    gulp.dest(paths.layout)
  )
  .pipe(
    reload({stream: true, once: true})
  )
));

gulp.task('sass:watch', () => (
  gulp.watch([paths.src], [context])
));
