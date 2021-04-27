import sqlite3

class DBHandler():
    # Инициализация Handler'a
    def __init__(self, db_name = 'database.db', addNoneOutput=True):
        self.dbName = db_name
        self.isConnected = False
        self.conn = None
        self.cursor = None
        self.lastOutput = []

        self.historyOutput = []
        self.errorsLogging = []

        self.addNoneOutput = addNoneOutput

    # Устанавливаем базу данных
    def setDBPath(self, db_path):
        self.dbName = db_path

    # =======================================================================

    # Подключачемся к БД
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.dbName)
            self.cursor = self.conn.cursor()
            self.isConnected = True

        except sqlite3.Error as e:
            self.appendError(100, f'[WARNING] Произошла ошибка при подключении к БД: {str(e)}')
            self.disconnect()

        except Exception as e:
            self.appendError(100, f'[WARNING] Произошла ошибка при подключении к БД: {str(e)}')
            self.disconnect()

    # Закрываем соединение
    def disconnect(self):
        self.conn.close()
        self.isConnected = False

    # =======================================================================
    
    # Быстрое выполнение запроса
    def quickExecute(self, query, args=()):
        self.connect()
        self.execute(query, args)
        self.disconnect()
        return self.lastOutput

    # Выполняем запрос 
    def execute(self, query, args=()):
        try:
            data = self.cursor.execute(query, args).fetchall()
            self.conn.commit()
            self.appendOutput(data)

        except sqlite3.Error as e:
            self.appendError(200, f'[WARNING] Произошла ошибка в БД во время исполнения запроса: {str(e)}', query, args)
            self.disconnect()
            self.appendOutput([])

        except Exception as e:
            self.appendError(200, f'[WARNING] Произошла ошибка во время исполнения запроса: {str(e)}', query, args)
            self.disconnect()
            self.appendOutput([])

        return self.lastOutput

    # =======================================================================
    
    # Добавляем результат для общего пользования 
    def appendOutput(self, data):
        self.lastOutput = data

        if self.addNoneOutput:
            self.historyOutput.append(data)
        else:
            if len(data) > 0:
                self.historyOutput.append(data)

    # Получить всю историю выводов
    def getAllHistory(self):
        return self.historyOutput

    # Очистка истории выводов
    def clearOutputHistory(self):
        self.historyOutput = []

    # =======================================================================

    # Добавляем ошибку в общий журнал ошибок
    def appendError(self, errorCode, errorBody='', query='', args=''):
        self.errorsLogging.append({ "code": errorCode, "message": errorBody, "query": query, "args": args})

    # Получить список всех ошибок
    def getAllErrors(self):
        return self.errorsLogging

    # Очистить все ошибки
    def clearErrors(self):
        self.errorsLogging = []
        
    # =======================================================================
    
# Запусти файл для проверки
if __name__ == '__main__':
    # Можно так
    handler = DBHandler('database.py');
    handler.connect()
    handler.execute("CREATE TABLE table_name (row INTEGER);")
    handler.disconnect()

    # А можно так
    handler.quickExecute("INSERT INTO table_name (row) VALUES (?);", (73, ))