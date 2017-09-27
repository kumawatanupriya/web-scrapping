from django.core.management.base import BaseCommand
import requests
import json
import concurrent.futures

def save_documents(result,ind):
    for index,link in enumerate(result["links"]):
        if link["rel"] == 'download':
            #print("hello")
            content = requests.get(link["href"],verify = False)
            content.encoding = 'ISO-8859-1'
            with open("native"+str(ind)+"result"+str(index)+"doc.pdf","wb") as pdf:
                for chunk in content.iter_content(chunk_size=1024):
 
         
                    if chunk:
                        pdf.write(chunk)
    return 
        
class Command(BaseCommand):
    
    def add_arguments(self, parser):
        #parser.add_argument('--url', dest='url', required=True,
        #   help='the url to process',)
        parser.add_argument('filingDatetimeFrom',)
        parser.add_argument('filingDatetimeTo',)

    def handle(self, *args, **options):
        #url = options['url']
        url =  'https://ptabdata.uspto.gov/ptab-api/documents/'
        filingDateFrom = options['filingDatetimeFrom']
        filingDateTo = options['filingDatetimeTo']
        new_url = url+'?filingDatetimeFrom='+filingDateFrom+'&filingDatetimeTo='+filingDateTo
        r = requests.get(new_url,verify = False)
        new_data = json.loads(r.text)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(save_documents, result,ind): result for ind,result in enumerate(new_data["results"])}
        
        
        # process the url
