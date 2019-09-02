import logging
from django.db import transaction
from tqdm import tqdm
import solr_conabio.solr_api as solr

HOST = 'http://snmb.conabio.gob.mx'
COLLECTION = 'taxonomia'

TERM_FMT = (
    'Term type: {type}\n'
    '  term: {term}\n'
    '  parents: {parents}\n'
    '  common names: {common}\n'
    '  synonyms: {synonyms}'
)
TERM_METADATA_SCHEMA = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/term_metadata_schema.json",
    "type": "object",
    "title": "Esquema de metadatos para términos taxonómicos",
    "required": [
        "id",
        "version",
        "origin"
    ],
    "properties": {
        "id": {
            "$id": "#/properties/id",
            "type": "string",
            "title": "id",
            "default": "",
            "examples": [
                "term.id"
            ],
            "pattern": "^(.*)$"
        },
        "version": {
            "$id": "#/properties/version",
            "type": "string",
            "title": "version",
            "default": "",
            "examples": [
                "term.version"
            ],
            "pattern": "^(.*)$"
        },
        "origin": {
            "$id": "#/properties/origin",
            "type": "string",
            "title": "origen",
            "default": "",
            "examples": [
                "juancarlos-catálogos"
            ],
            "pattern": "^(.*)$"
        }
    }
}
TERM_ENTAILMENT_METADATA_SCHEMA = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/term_entailment_schema.json",
    "type": "object",
    "title": "Esquema de metadatos para implicaciones taxonómicas",
    "required": [
        "target_id",
        "target_version",
        "target_origin",
        "source_id",
        "source_version",
        "source_origin"
    ],
    "properties": {
        "target_id": {
            "$id": "#/properties/target_id",
            "type": "string",
            "title": "target_id",
            "default": "",
            "examples": [
                "term.id"
            ],
            "pattern": "^(.*)$"
        },
        "target_version": {
            "$id": "#/properties/target_version",
            "type": "string",
            "title": "target_version",
            "default": "",
            "examples": [
                "term.version"
            ],
            "pattern": "^(.*)$"
        },
        "target_origin": {
            "$id": "#/properties/target_origin",
            "type": "string",
            "title": "target_origin",
            "default": "",
            "examples": [
                "juancarlos-catálogos"
            ],
            "pattern": "^(.*)$"
        },
        "source_id": {
            "$id": "#/properties/source_id",
            "type": "string",
            "title": "source_id",
            "default": "",
            "examples": [
                "term.id"
            ],
            "pattern": "^(.*)$"
        },
        "source_version": {
            "$id": "#/properties/source_version",
            "type": "string",
            "title": "source_version",
            "default": "",
            "examples": [
                "term.version"
            ],
            "pattern": "^(.*)$"
        },
        "source_origin": {
            "$id": "#/properties/source_origin",
            "type": "string",
            "title": "source_origin",
            "default": "",
            "examples": [
                "juancarlos-catálogos"
            ],
            "pattern": "^(.*)$"
        }
    }
}


@transaction.atomic
def update_database(db_models):
    data = get_all_data()
    terms = parse_data(data)
    term_pk_map = create_all_terms(terms, db_models)
    create_all_entailments(terms, term_pk_map, db_models)


def parse_data(data):
    logging.info('Parsing data...')
    terms =  {
        datum['id']: Term(datum)
        for datum in data
        if datum['nombre']
    }
    logging.info('done.')
    return terms


def get_all_data(num_rows=50000):
    total_rows = get_num_rows()

    fl = [
        'id',
        'categoria_taxonomica',
        'nombre',
        'ascendentes',
        'nombres_comunes',
        'subcategoria_taxonomica',
        'sinonimos',
        '_version_'
    ]

    logging.info('Getting data...')
    data = []
    for start in tqdm(range(0, total_rows, num_rows)):
        response = solr.query(HOST, COLLECTION, rows=num_rows, start=start, fl=fl)
        data += response['response']['docs']

    logging.info('done.')
    return data

def get_num_rows():
    response = solr.query(HOST, COLLECTION, rows=0)
    return response['response']['numFound']


def create_all_terms(all_terms, db_models):
    pk_map = {}

    logging.info('Creating terms...')
    for term in tqdm(all_terms.values()):
        db_term = process_term(term, db_models)
        pk_map[term.id] = db_term
    logging.info('done')

    return pk_map


def process_term(term, db_models):
    term_type, _ = get_term_type(term.term_type, db_models)
    db_term, _ = create_term(term_type, term.term, term.metadata, db_models)

    if term.synonyms:
        create_synonyms(term, db_term, db_models)

    if term.common_names:
        create_common_names(term, db_term, db_models)

    return db_term


def create_term(term_type, value, metadata, db_models):
    return db_models.Term.objects.get_or_create(
        term_type=term_type,
        value=value,
        defaults={
            'metadata': metadata
        }
    )


def create_common_names(term, db_term, db_models):
    common_name_type, _ = get_term_type('nombre común', db_models)
    for common_name in term.common_names:
        common_name_term, _ = create_term(
            common_name_type,
            common_name,
            term.metadata,
            db_models)
        create_entailment(common_name_term, db_term, db_models)


def get_term_type(term_type, db_models):
    return db_models.TermType.objects.get_or_create(
        name=term_type,
        defaults={
            'description': 'Nivel taxonómico: {}'.format(term_type),
            'is_categorical': True,
            'metadata_schema': TERM_METADATA_SCHEMA,
            'synonym_metadata_schema': TERM_METADATA_SCHEMA
        }
    )


def create_synonyms(term, db_term, db_models):
    term_type = db_term.term_type

    for synonym in term.synonyms:
        synonym_term, _ = create_term(term_type, synonym, term.metadata, db_models)
        create_synonym(synonym_term, db_term, term.metadata, db_models)


def create_synonym(source, target, metadata, db_models):
    return db_models.Synonym.objects.get_or_create(
        source=source,
        target=target,
        defaults={
            'metadata': metadata
        }
    )


def create_all_entailments(terms, mapping, db_models):
    logging.info('Creating entailments...')
    for term in tqdm(terms.values()):
        create_term_entailments(term, mapping, db_models)
    logging.info('done.')


def create_term_entailments(term, mapping, db_models):
    db_term = mapping[term.id]

    for parent_id in term.parents:
        try:
            parent_term = mapping[parent_id]
            create_entailment(db_term, parent_term, db_models)
        except KeyError:
            pass


def create_entailment(source, target, db_models):
    check_entailment_type(source, target, db_models)

    metadata = {
        "target_id": target.metadata['id'],
        "target_version": target.metadata['version'],
        "target_origin": target.metadata['origin'],
        "source_id": source.metadata['id'],
        "source_version": source.metadata['version'],
        "source_origin": source.metadata['origin']
    }

    return db_models.Entailment.objects.get_or_create(
        source=source,
        target=target,
        defaults={
            'metadata': metadata
        }
    )


def check_entailment_type(source, target, db_models):
    return db_models.EntailmentType.objects.get_or_create(
        source_type=source.term_type,
        target_type=target.term_type,
        defaults={
            'metadata_schema': TERM_ENTAILMENT_METADATA_SCHEMA
        }
    )


class Term(object):
    def __init__(self, data):
        self.id = str(data['id'])

        try:
            self.term_type = data['subcategoria_taxonomica']
        except KeyError:
            try:
                self.term_type = data['categoria_taxonomica']
            except KeyError:
                self.term_type = None
                print(data)

        self.term = data['nombre']
        self.version = data['_version_']

        self.common_names = data.get('nombres_comunes', [])
        self.synonyms = data.get('sinonimos', [])


        self.parents = [
            str(sid) for sid in data['ascendentes'].split(',')
            if str(sid) != str(self.id)
        ]

    @property
    def metadata(self):
        return   {
            'id': str(self.id),
            'version': str(self.version),
            'origin': 'juancarlos-catálogos'
        }

    def __str__(self):
        return TERM_FMT.format(
            type=self.term_type,
            term=self.term,
            parents=str(self.parents),
            common=str(self.common_names),
            synonyms=str(self.synonyms))

    def __repr__(self):
        return str(self)
