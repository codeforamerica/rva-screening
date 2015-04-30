from flask_assets import Bundle, Environment

js = Bundle(
  'vendor/jquery/dist/jquery.js',
  'vendor/bootstrap/dist/js/bootstrap.js',
  'js/main.js',
  output='./public/js/app.js',
  depends=('js/*.js', 'js/**/*.js')
)

css = Bundle(
  Bundle(
    'vendor/bootstrap/dist/css/bootstrap.css',
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