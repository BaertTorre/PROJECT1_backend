from .Database import Database

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def __make_time_event(error_id):
        sql = f"INSERT INTO `time` (`error codes_id error code`) VALUES ({error_id});"
        return Database.execute_sql(sql)

    @staticmethod
    def add_ultrasone_waarde(ultrasone_data, ultrasone_positie):
        id_time = DataRepository.__make_time_event(200)
        sql = f"INSERT INTO `ultrasonic data` (`ultrasonic data`,`ultrasonic positie rechts midden links`,`time_id time`) VALUES ({ultrasone_data},{ultrasone_positie},{id_time});"
        return Database.execute_sql(sql)