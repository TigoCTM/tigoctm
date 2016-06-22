import gutil from 'gulp-util';

export const err = (name, callback) => (
  (err, stats) => {
    if (err) {
      throw new gutil.PluginError(name, err);
    }
    gutil.log(`[${name}]`, stats.toString({
      colors: true
    }));
    callback();
  }
);
