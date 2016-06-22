'use strict';

import browserSync from 'browser-sync';
import gulp from 'gulp';
import gulpConfig from '../../gulp.config';
import jade from 'gulp-jade';
import path from 'path';
import sourcemaps from 'gulp-sourcemaps';
import {err} from '../common';

const paths = {
  src: [
    path.join(gulpConfig.dirs.src, gulpConfig.tasks.html.src, `/**/*.{${gulpConfig.tasks.html.extensions}}`),
    `!${path.join(
      gulpConfig.dirs.src, gulpConfig.tasks.html.src,
      `/**/includes/*.{${gulpConfig.tasks.html.extensions}}`
    )}`
  ],
  dest: path.join(gulpConfig.dirs.dest, gulpConfig.tasks.html.dest),
  layout: path.join(gulpConfig.dirs.src, 'hugo/layouts')
};

const reload = browserSync.reload;

const jadeCommon = callback => (
  gulp.src(paths.src)
  .pipe(
    sourcemaps.init()
  )
  .pipe(
    jade(gulpConfig.tasks.html.jade)
    .on('error', err('jade', callback))
  )
  .pipe(
    sourcemaps.write()
  )
);

gulp.task('jade:layout', callback => (
  jadeCommon(callback)
  .pipe(
    gulp.dest(paths.layout)
  )
  .pipe(
    reload({stream: true, once: true})
  )
));

gulp.task('jade:watch', () => (
  gulp.watch([paths.src], ['jade:layout', 'hugo'])
));
