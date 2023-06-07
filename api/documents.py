from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from api.models import Complaint


@registry.register_document
class ComplaintsDocument(Document):
    id = fields.KeywordField(attr='complaint_id')
    status = fields.TextField(attr='status')
    date = fields.DateField(attr='date')
    region = fields.TextField(attr='region')
    customer_name = fields.TextField(attr='customer_name')
    customer_inn = fields.TextField(attr='customer_inn')
    complainant_name = fields.TextField(attr='complainant_name')
    complainant_inn = fields.TextField(attr='complainant_inn')
    justification = fields.TextField(attr='justification')
    numb_purchase = fields.TextField(attr='numb_purchase')
    prescription = fields.TextField(attr='prescription')
    list_docs = fields.TextField(attr='list_docs')
    json_data = fields.TextField(attr='json_data')
    docs_complaints = fields.TextField(attr='docs_complaints')

    class Index:
        name = 'complaints'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Complaint


@registry.register_document
class SolutionsDocument(Document):
    id = fields.KeywordField(attr='complaint_id')
    status = fields.TextField(attr='status')
    date = fields.DateField(attr='date')
    region = fields.TextField(attr='region')
    customer_name = fields.TextField(attr='customer_name')
    customer_inn = fields.TextField(attr='customer_inn')
    complainant_name = fields.TextField(attr='complainant_name')
    complainant_inn = fields.TextField(attr='complainant_inn')
    justification = fields.TextField(attr='justification')
    numb_purchase = fields.TextField(attr='numb_purchase')
    prescription = fields.TextField(attr='prescription')
    list_docs = fields.TextField(attr='list_docs')
    json_data = fields.TextField(attr='json_data')
    docs_solutions = fields.TextField(attr='docs_solutions')

    class Index:
        name = 'solutions'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Complaint


@registry.register_document
class PrescriptionsDocument(Document):
    id = fields.KeywordField(attr='complaint_id')
    status = fields.TextField(attr='status')
    date = fields.DateField(attr='date')
    region = fields.TextField(attr='region')
    customer_name = fields.TextField(attr='customer_name')
    customer_inn = fields.TextField(attr='customer_inn')
    complainant_name = fields.TextField(attr='complainant_name')
    complainant_inn = fields.TextField(attr='complainant_inn')
    justification = fields.TextField(attr='justification')
    numb_purchase = fields.TextField(attr='numb_purchase')
    prescription = fields.TextField(attr='prescription')
    list_docs = fields.TextField(attr='list_docs')
    json_data = fields.TextField(attr='json_data')
    docs_prescriptions = fields.TextField(attr='docs_prescriptions')

    class Index:
        name = 'prescriptions'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Complaint

