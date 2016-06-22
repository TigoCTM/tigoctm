'use strict';

import browserSync from 'browser-sync';
import gulp from 'gulp';
import gulpConfig from '../../gulp.config';
import gutil from 'gulp-util';

const context = gutil.env.layout ? gulpConfig.dirs.dev : gulpConfig.dirs.dest;

gulp.task('browser-sync', () => (
  browserSync(
    {
      server: {
        baseDir: context
      }
    }
  )
));
