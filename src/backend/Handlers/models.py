from flask import jsonify

from ..DAO.modelsDAO import ModelsDAO


class ModelsHandler:
    def get_all_models(self):
        dao = ModelsDAO()
        results = dao.get_models_id_and_desc()
        return jsonify(fieldOfWorkOptions=results)
