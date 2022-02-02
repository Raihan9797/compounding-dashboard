import dash
import dash_html_components as html

app = dash.Dash(__name__)
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
app.scripts.append_script({ 'external_url' : mathjax })

app.layout = html.Div(id='main',children=[
  html.Div(id='static',children='$$ x=1 $$'),
  html.Div(id='dynamic',children=''),
  html.Button('Add Math',id='button'),
])

@app.callback(
  dash.dependencies.Output('dynamic','children'),
 [dash.dependencies.Input('button','n_clicks')]
)
def addmath(n_clicks):
  if n_clicks:
    return '$$ x=1 $$'
  else:
    return None

if __name__ == '__main__':
  app.run_server(debug=True, port = 4000)