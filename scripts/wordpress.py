"""Deploy the local design using a WordPress application password. Never prints secrets."""
import base64,json,re,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
ENV={}
for line in (ROOT/'.env').read_text().splitlines():
 if '=' in line and not line.lstrip().startswith('#'):
  k,v=line.split('=',1);ENV[k.strip()]=v.strip().strip('\"\'')
BASE=ENV.get('WP_URL',ENV.get('site','https://lynnbout.nl')).replace('https;','https:').rstrip('/')
USER=ENV.get('WP_USER','admin'); PASSWORD=ENV.get('WP_APP_PASSWORD',ENV.get('api',''))
AUTH='Basic '+base64.b64encode(f'{USER}:{PASSWORD}'.encode()).decode()
def request(path,data=None,headers=None,raw=None):
 h={'Authorization':AUTH};h.update(headers or {})
 if data is not None:raw=json.dumps(data).encode();h['Content-Type']='application/json'
 req=urllib.request.Request(BASE+'/wp-json/wp/v2/'+path,data=raw,headers=h)
 try:
  with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
 except urllib.error.HTTPError as e:raise SystemExit(f'WordPress {e.code}: '+e.read().decode()[:350])
def main():
 me=request('users/me');print('WordPress authentication successful.')
 settings=request('settings');page_id=settings.get('page_on_front')
 if not page_id:raise SystemExit('No static homepage configured; review before deployment.')
 backup=ROOT/'backups';backup.mkdir(exist_ok=True)
 original=request(f'pages/{page_id}?context=edit')
 (backup/f'page-{page_id}.json').write_text(json.dumps(original,ensure_ascii=False,indent=2))
 (backup/'settings.json').write_text(json.dumps(settings,ensure_ascii=False,indent=2))
 html=(ROOT/'index.html').read_text()
 for name in ['megacity','pavilion']:
  f=ROOT/'assets'/f'{name}.png'
  media=request('media',raw=f.read_bytes(),headers={'Content-Type':'image/png','Content-Disposition':f'attachment; filename="lynn-unbuilt-{name}.png"'})
  request('media/'+str(media['id']),{'alt_text': 'AI-gegenereerde architectuurconceptstudie: '+('verticale anime-stad' if name=='megacity' else 'houten paviljoen boven water')})
  html=html.replace('assets/'+name+'.png',media['source_url'])
 css=re.search(r'<style>(.*?)</style>',html,re.S).group(1)
 body=re.search(r'<body>(.*?)</body>',html,re.S).group(1)
 # Customizr theme: make the page canvas full width and hide surrounding theme chrome.
 override='body:has(#lynn-site) #customizr-slider-main_slider{display:none!important}body:has(#lynn-site){background:#eeeee5}body:has(#lynn-site) #tc-page-wrap{overflow:hidden}body:has(#lynn-site) .tc-header,body:has(#lynn-site) #footer,body:has(#lynn-site) .entry-header,body:has(#lynn-site) .post-navigation,body:has(#lynn-site) .breadcrumb-trail,body:has(#lynn-site) #right,body:has(#lynn-site) #left{display:none!important}body:has(#lynn-site) #main-wrapper,body:has(#lynn-site) #main-wrapper .container,body:has(#lynn-site) .article-container,body:has(#lynn-site) .entry-content,body:has(#lynn-site) article,body:has(#lynn-site) .content{width:100%!important;max-width:none!important;margin:0!important;padding:0!important}#lynn-site{width:100vw;position:relative;left:50%;margin-left:-50vw;text-align:left;font-family:"DM Sans",sans-serif;color:#161a18;background:#eeeee5}#lynn-site h1,#lynn-site h2,#lynn-site h3{text-transform:none;color:inherit}#lynn-site .dark h2{color:#eeeee5}'
 content='<!-- wp:html -->\n<style>'+css+'\n'+override+'</style><div id="lynn-site">'+body+'</div>\n<!-- /wp:html -->'
 result=request(f'pages/{page_id}',{'title':'LYNN / UNBUILT','content':content,'status':'publish','comment_status':'closed','ping_status':'closed'})
 request('settings',{'title':'LYNN / UNBUILT','description':'Anime × Bouwkunde × Verbeelding'})
 print('Published: '+result['link'])
if __name__=='__main__':main()
