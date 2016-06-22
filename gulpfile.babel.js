'use strict';

import gulp from 'gulp';
import requireDir from 'require-dir';
import runSequence from 'run-sequence';

requireDir('./gulp', {
  recurse: true
});

gulp.task('default', () => {
  runSequence('build');
});

gulp.task('layout', () => {
  runSequence('sass:layout', 'hugo');
});

gulp.task('server', () => {
  runSequence('layout', 'browser-sync', 'jade:watch', 'sass:watch');
});

gulp.task('build', () => {
  runSequence('sass', 'hugo');
});
