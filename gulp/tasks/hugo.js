'use strict';

import exec from 'child_process';
import gulp from 'gulp';
import gutil from 'gulp-util';

gulp.task('hugo', ['jade:layout'], () => {
  const result = exec.execSync(
    'hugo --config=config.toml',
    {
      encoding: 'utf-8'
    }
  );
  gutil.log('[hugo]', result.toString({
    colors: true
  }));
});
