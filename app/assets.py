from flask_assets import Bundle, Environment

js = Bundle(
  'vendor/jquery/dist/jquery.js',
  'vendor/bootstrap/dist/js/bootstrap.js',
  'js/main.js',
  output='./public/js/app.js',
  depends=('js/*.js', 'js/**/*.js')
)

sass = Bundle(
  'sass/main.scss',
  filters='sass',
  output='./public/css/app.css',
  depends=('sass/*.scss', 'sass/**/*.scss')
)

css_bootstrap = Bundle(
  'vendor/bootstrap/dist/css/bootstrap.css',
  output='./public/css/bootstrap.css'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_bootstrap', css_bootstrap)
assets.register('css_app', sass)