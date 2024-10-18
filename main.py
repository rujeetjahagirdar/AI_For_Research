from scholarly import scholarly, ProxyGenerator
import re
import pandas as pd

# pg = ProxyGenerator()
# # success = pg.FreeProxies()
# # success = pg.SingleProxy(http = "34.81.160.132", https = "203.154.162.230")
# success = pg.Tor_Internal(tor_cmd = "tor")
# scholarly.use_proxy(pg)

def get_google_author_details(authr_url):
    #authr_url=https://scholar.google.com/citations?user=-zSd9V0AAAAJ&hl=en
    # pg = ProxyGenerator()
    # success = pg.FreeProxies()
    # scholarly.use_proxy(pg)
    match = re.search(r"user=([^&]+)", authr_url)
    if match:
        authr_id = match.group(1)
        print("Author ID= ", authr_id)
        authr_name = scholarly.search_author_id(authr_id)['name']
        print("Author Name= ", authr_name)
    else:
        authr_name = ''
    result= []
    search_query = scholarly.search_author(authr_name)
    for authrs in search_query:
        if(authrs['scholar_id']==authr_id):
            t = {}
            rslt = scholarly.fill(authrs, sections=['basics', 'counts', 'publications'])
            t['name'] = rslt['name']
            t['affiliation'] = rslt['affiliation']
            t['citation_counts'] = rslt['citedby']
            t['publications'] = []
            for i in rslt['publications']:
                temp = {}
                citedbylist = [c['bib']['title'] for c in scholarly.citedby(i)]
                temp['title'] = i['bib']['title']
                temp['pub_year'] = i['bib']['pub_year']
                temp['conference'] = i['bib']['conference']
                temp['authors'] = [a.rstrip().lstrip() for a in i['bib']['author'].split('and')]
                temp['citedbyList'] = citedbylist
                # t['publications'].append((temp['title'], temp['pub_year'], temp['citation'].split(',')[0], \
                #                           temp['conference'], [a.rstrip().lstrip() for a in temp['author'].split('and')], citedbylist))
                t['publications'].append(temp)
                # break
            result.append(t)

    return result

a = get_google_author_details('https://scholar.google.com/citations?user=-zSd9V0AAAAJ&hl=en')
print(a)

# df = pd.DataFrame()
#next(scholarly.search_pubs("Uncertainty quantification of collaborative Detection for self-driving"))
