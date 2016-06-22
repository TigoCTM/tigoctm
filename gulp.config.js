const dirs = {
  src: './src',
  dest: './public',
  dev: './dist',
  env: {
    src: './gulp/env',
    dest: './src/js'
  }
};

export default {
  dirs: dirs,
  context: {},
  tasks: {
    html: {
      src: 'html',
      dest: '',
      extensions: ['html', 'jade'],
      jade: {
        pretty: true
      }
    },
    css: {
      src: 'css',
      dest: 'css',
      extensions: ['css', 'scss', 'sass'],
      sass: {
        indentedSyntax: true,
        includePaths: ['sass']
      }
    }
  }
};
