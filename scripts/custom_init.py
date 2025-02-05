from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator import WikibaseIntegrator, wbi_login, datatypes
from wikibaseintegrator.datatypes import extra
import pandas
import pathlib
import rdflib
import requests
import time
import tqdm
import os

# we also need to handle a .env file
import dotenv

vars = dotenv.dotenv_values()


def pull_attribute(row, pre, filt):

    ''' Pull specific attribute from graph. '''

    iri = row['iri']
    for s,p,o in data_model.triples((rdflib.URIRef(iri), pre, None)):
        if filt in str(o):
            return str(o)
        
def pull_attribute_ml(row, pre, filt):

    ''' Pull specific attribute from graph - multilingual. '''

    iri = row['iri']
    labels = {}
    for s,p,o in data_model.triples((rdflib.URIRef(iri), pre, None)):
        labels[o.language] = str(o)
    return labels

try:
    data_model = rdflib.Graph().parse(pathlib.Path.cwd() / 'wikibase_generic_model.ttl')
except FileNotFoundError:
    r = requests.get('https://gitlab.com/nfdi4culture/ta1-data-enrichment/wikibase-model/-/raw/main/wikibase_generic_model.ttl')
    data_model = rdflib.Graph().parse(data=r.content, format='ttl')

# compile entities

entities = list()
for x in [rdflib.OWL.Class, rdflib.OWL.ObjectProperty, rdflib.OWL.DatatypeProperty, rdflib.OWL.NamedIndividual]:
    entities += [{'iri':s, 'type':str(o)} for s,p,o in data_model.triples((None, rdflib.RDF.type, x))]
dataframe = pandas.DataFrame(entities)

# build a table of entities to write.

dataframe.loc[dataframe.type.str.contains('Class|Individual', na=False), 'wikibase_type'] = 'item'
dataframe.loc[dataframe.type.str.contains('Property', na=False), 'wikibase_type'] = 'property'

dataframe['wikibase_id'] = dataframe.apply(pull_attribute, pre=rdflib.SKOS.note, filt='Wikibase ID', axis=1)
dataframe['wikibase_datatype'] = dataframe.apply(pull_attribute, pre=rdflib.SKOS.note, filt='datatype', axis=1)
dataframe['label'] = dataframe.apply(pull_attribute_ml, pre=rdflib.RDFS.label, filt='', axis=1)
dataframe['description'] = dataframe.apply(pull_attribute_ml, pre=rdflib.URIRef('http://purl.org/dc/elements/1.1/description'), filt='', axis=1)

# id wrangling.

dataframe['wikibase_datatype'] = dataframe['wikibase_datatype'].str.replace('Wikibase datatype:','').str.strip()
dataframe['wikibase_id'] = dataframe['wikibase_id'].str.replace('Wikibase ID:','').str.strip() 
dataframe['wikibase_id'] = dataframe['wikibase_id'].str.replace('Q','').str.strip() 
dataframe['wikibase_id'] = dataframe['wikibase_id'].str.replace('P','')
dataframe['wikibase_id'] = dataframe['wikibase_id'].str.strip().astype('int')
dataframe = dataframe.sort_values(by='wikibase_id')

# pull subclass and subprop statements.

subclass_dataframe = pandas.DataFrame(columns=['iri', 'subclass_of'])
for s,p,o in data_model.triples((None, rdflib.RDFS.subClassOf, None)):
    subclass_dataframe.loc[len(subclass_dataframe)] = [s, o]
dataframe = pandas.merge(dataframe, subclass_dataframe, on='iri', how='left')

subprop_dataframe = pandas.DataFrame(columns=['iri', 'subproperty_of'])
for s,p,o in data_model.triples((None, rdflib.RDFS.subPropertyOf, None)):
    subprop_dataframe.loc[len(subprop_dataframe)] = [s, o]
dataframe = pandas.merge(dataframe, subprop_dataframe, on='iri', how='left')


# writing config ( all from dotenv)
domain = "http://" + os.environ.get('W4R_SERVER_NAME') + "/"
# if no trailing slash, add it.
if domain[-1] != '/':
    domain += '/'
wbi_config['MEDIAWIKI_API_URL'] = domain+'api.php'
wbi_config['USER_AGENT'] = 'generic data model'
login_instance = wbi_login.Login(user=os.environ.get('W4R_MW_ADMIN_USER'), password=os.environ.get('W4R_MW_ADMIN_PASS'))
wbi = WikibaseIntegrator(login=login_instance)

# write entities.

for x in tqdm.tqdm(dataframe.to_dict('records')):

    if x['wikibase_type'] == 'property':
        ident = f"P{x['wikibase_id']}"
        r = requests.get(f'{domain}wiki/Special:EntityData/{ident}.ttl', verify=False)
        if r.status_code == 404:
            try:
                entity = wbi.property.new(datatype=x['wikibase_datatype'])
            except ValueError:
                entity = wbi.property.new(datatype='string')
            entity.write()

        updater = wbi.property.get(ident)
        for key, value in x['label'].items():
            updater.labels.set(key, value)
        for key, value in x['description'].items():
            updater.descriptions.set(key, value)
        updater.write()

    if x['wikibase_type'] == 'item':
        ident = f"Q{x['wikibase_id']}"
        r = requests.get(f'{domain}wiki/Special:EntityData/{ident}.ttl', verify=False)
        if r.status_code == 404:
            entity = wbi.item.new()
            entity.write()

        updater = wbi.item.get(ident)
        for key, value in x['label'].items():
            updater.labels.set(key, value)
        for key, value in x['description'].items():
            updater.descriptions.set(key, value)
        updater.write()


# reserve items up to 200.

for x in tqdm.tqdm(range(200)):

    ident = f"Q{x}"
    r = requests.get(f'{domain}wiki/Special:EntityData/{ident}.ttl', verify=False)
    if r.status_code == 404:
        entity = wbi.item.new()
        entity.write()

# write subclass and subproperty claims.

for x in tqdm.tqdm(dataframe.to_dict('records')):

    if type(x['subproperty_of']) != float:
        target = dataframe.loc[dataframe.iri.isin([x['subproperty_of']])].iloc[0]['wikibase_id']
        prop = wbi.property.get('P'+str(x['wikibase_id']))
        claim = datatypes.Property(prop_nr='P3', value='P'+str(target))
        prop.claims.add(claim)
        prop.write()

    if type(x['subclass_of']) != float:
        target = dataframe.loc[dataframe.iri.isin([x['subclass_of']])].iloc[0]['wikibase_id']
        item = wbi.item.get('Q'+str(x['wikibase_id']))
        claim = datatypes.Item(prop_nr='P2', value='Q'+str(target))
        item.claims.add(claim)
        item.write()
