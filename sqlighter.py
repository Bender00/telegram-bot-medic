import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ? ', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, first_name, last_name, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `status`) VALUES(?,?,?,?)", (user_id, first_name, last_name, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `status` = ? WHERE `user_id` = ?", (status, user_id,))

    def view(self, id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `Endokrynka` WHERE `id` = ?", (id,)).fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
        