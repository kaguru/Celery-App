from sqlalchemy import or_, func, any_, and_
from ..db import get_db_session
from ..helpers.log_handler import exception_handler


db_session = get_db_session()


class CommonModel:
    @classmethod
    def create(cls, **kwargs):
        theme = cls(**kwargs)
        db_session.add(theme)
        db_session.commit()
        return theme

    @classmethod
    def bulk_insert_items(cls, item_list):
        try:
            rs = db_session \
                .execute(cls.__table__.insert(),
                         item_list)
            db_session.commit()
            return rs
        except Exception as e:
            print(f"************* Exception Models \n {e}")
            return None

    @classmethod
    @exception_handler()
    def create_if_not_exist(cls, original_dict, check_dict):
        object_rs = cls.get_by_dict(check_dict)
        if object_rs:
            return object_rs
        else:
            return cls.create(**original_dict)

    @classmethod
    @exception_handler()
    def get_all(cls):
        out = cls.query.order_by(cls.created_at.desc()).all()
        print("out All:: ", out)
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    @exception_handler()
    def get_by_id(cls, object_id):
        return cls.query.filter(cls.id == object_id).first()

    @classmethod
    @exception_handler()
    def get_by_email(cls, email_address):
        return cls.query.filter(cls.email == email_address).first()

    @classmethod
    @exception_handler()
    def get_by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    @exception_handler()
    def get_by_names(cls, name):
        return cls.query.filter(cls.name.ilike(name)).all()

    @classmethod
    @exception_handler()
    def get_by_national_id(cls, national_id):
        return cls.query.filter(cls.national_id == national_id).first()

    @classmethod
    @exception_handler()
    def get_by_identifier(cls, item_identifier):
        return cls.query.filter(cls.identifier == item_identifier).first()

    @classmethod
    @exception_handler()
    def get_by_dict(cls, input_dict):
        object_rs = db_session \
            .query(cls).filter_by(**input_dict) \
            .order_by(cls.created_at.desc()) \
            .first()
        return object_rs

    @classmethod
    @exception_handler()
    def get_all_by_dict(cls, check_dict):
        object_rs = db_session \
            .query(cls).filter_by(**check_dict) \
            .order_by(cls.created_at.desc()) \
            .all()
        return object_rs

    @classmethod
    @exception_handler()
    def search_by_name(cls, name_params):
        name_params = f"%{name_params}%".replace(" ", "%")
        return cls.query.filter(cls.name.ilike(name_params))\
                  .order_by(cls.created_at.desc()).all()

    @classmethod
    @exception_handler()
    def search_by_description(cls, description_params):
        description_params_formatted = f"%{description_params}%".replace(" ", "%")
        return cls.query.filter(cls.description.ilike(description_params_formatted)) \
            .order_by(cls.created_at.desc()).all()

    @classmethod
    @exception_handler()
    def search_patient(cls, search_params):
        search_params_list = ' '.join(search_params.split()).lower().split()
        search_params_formatted = [f"%{i}%" for i in search_params_list]
        search_args = [col.ilike(any_(search_params_formatted)) for col in [cls.first_name,
                                                                       cls.middle_name,
                                                                       cls.last_name,
                                                                       cls.patient_number,
                                                                       cls.patient_numbers_reference,
                                                                       cls.old_patient_number,
                                                                       cls.national_id
                                                                       ]]
        return cls.query.filter(or_(*search_args)) \
            .order_by(cls.created_at.desc()) \
            .limit(100)\
            .all()

    @exception_handler()
    def search_by_description(cls, description_params):
        description_params_formatted = f"%{description_params}%".replace(" ", "%")
        return cls.query.filter(cls.description.ilike(description_params_formatted)) \
            .order_by(cls.created_at.desc()).all()

    @classmethod
    @exception_handler()
    def search_service(cls, search_params, exclude_pharmacy=True):
        search_params_list = ' '.join(search_params.split()).lower().split()
        search_params_formatted = [f"%{i}%" for i in search_params_list]
        search_args = [col.ilike(any_(search_params_formatted)) for col in [cls.name,
                                                                            cls.abbreviation,
                                                                            cls.description,
                                                                            cls.tags
                                                                            ]]
        if exclude_pharmacy:
            return cls.query.filter(and_(cls.department != "pharmacy"), or_(*search_args)) \
                .order_by(cls.created_at.desc()) \
                .limit(100) \
                .all()
        return cls.query.filter(or_(*search_args)) \
            .order_by(cls.created_at.desc()) \
            .limit(100) \
            .all()

    @classmethod
    @exception_handler()
    def update_by_id(cls, object_id, object_values):
        if object_id:
            db_session.query(cls).filter(cls.id == object_id).update(object_values)
            db_session.commit()
            return cls.query.filter(cls.id == object_id).first()

    @classmethod
    @exception_handler()
    def update_by_identifier(cls, object_identifier, object_values):
        if object_identifier:
            db_session.query(cls).filter(cls.identifier == object_identifier).update(object_values)
            db_session.commit()
            return cls.query.filter(cls.identifier == object_identifier).first()

    @classmethod
    @exception_handler()
    def delete_by_id(cls, item_id):
        if item_id:
            model_objects = db_session.query(cls).filter(cls.id == item_id).first()
            return cls.delete_objects(model_objects)

    @classmethod
    @exception_handler()
    def delete_by_identifier(cls, item_identifier):
        if item_identifier:
            model_objects = db_session.query(cls).filter(cls.identifier == item_identifier).first()
            return cls.delete_objects(model_objects)

    @staticmethod
    def delete_objects(model_objects):
        if model_objects:
            db_session.delete(model_objects)
            db_session.commit()
        return model_objects
