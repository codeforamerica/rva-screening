from flask_assets import Bundle, Environment
import shutil

# used to copy font files from Bootstrap
def copy(src, dest):
  try:
    shutil.copytree(src, dest)
  except OSError as e:
    print(' * Files in %s are copied!' % src)

bootstrap = 'node_modules/bootstrap/dist/'

# Copy Bootstrap Fonts
copy('app/static/{}fonts'.format(bootstrap), 'app/static/public/fonts/')

js = Bundle(
  'node_modules/jquery/dist/jquery.js',
  '{}js/bootstrap.js'.format(bootstrap),
  'js/main.js',
  output='./public/js/app.js',
  depends=('js/*.js', 'js/**/*.js')
)

css = Bundle(
  Bundle(
    '{}css/bootstrap.css'.format(bootstrap),
    filters='cssmin',
    output='./public/css/bootstrap.css'
  ),
  Bundle(
    'sass/main.scss',
    filters='sass,cssmin',
    output='./public/css/app.css',
    depends=('sass/*.scss', 'sass/**/*.scss')
  )
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
