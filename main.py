from scholarly import scholarly, ProxyGenerator
import re
import requests
import pandas as pd
from streamlit import query_params


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

def get_semantic_citedby_details(paper_id):

    response = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields=title").json()
    cited_papers_titles = [paper['citingPaper']['title'] for paper in response.get('data', [])]
    return cited_papers_titles

def get_semantic_author_afiiliation(author_id):
    res = requests.get(f'https://api.semanticscholar.org/graph/v1/author/{author_id}?fields=affiliations').json()
    # print(res)
    return res['affiliations']

def get_semantic_author_details(author_url):
    #Example url = https://www.semanticscholar.org/author/Sihong-He/2049027478

    author_id = author_url.split("/")[-1]
    query_params = {
        "fields": "name,affiliations,papers.title,papers.authors,papers.publicationVenue,papers.publicationDate"
    }

    author_url = f'https://api.semanticscholar.org/graph/v1/author/{author_id}?fields={query_params['fields']}'

    response = requests.get(author_url).json()

    for i in range(len(response['papers'])):
        pid = response['papers'][i]['paperId']
        response['papers'][i]['citedBy'] = get_semantic_citedby_details(pid)
        # print(response['papers'][i]['publicationVenue'])
        response['papers'][i]['publicationVenue'] = response['papers'][i]['publicationVenue']['name'] if response['papers'][i]['publicationVenue'] else ''
        for j in range(len(response['papers'][i]['authors'])):
            a_id = response['papers'][i]['authors'][j]['authorId']
            response['papers'][i]['authors'][j]['affiliations'] = get_semantic_author_afiiliation(a_id)
        #     break
        # break
    # print(response)
    return response



# a = get_google_author_details('https://scholar.google.com/citations?user=-zSd9V0AAAAJ&hl=en')
# print(a)

a = get_semantic_author_details('https://www.semanticscholar.org/author/Sihong-He/2049027478')
print(a)

# a = get_semantic_paper_details('18763b34cd0d476c084498ffa180c67c76e485d1')
# print(a)