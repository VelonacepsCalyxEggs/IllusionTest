import sqlite3


class Manager():
    database_path = 'database/svodb.db'
    def __init__(self) -> None:
        try:
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS test_subjects (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age FLOAT NOT NULL,
                        gender TEXT NOT NULL
                    )
                ''')

                cur.execute('''
                    CREATE TABLE IF NOT EXISTS poggendorff_results (
                        test_subject INTEGER PRIMARY KEY,
                        w_param FLOAT NOT NULL,
                        h_param FLOAT NOT NULL,
                        h_human_subject FLOAT NOT NULL,
                        alpha_angle FLOAT NOT NULL,
                        beta_angle FLOAT NOT NULL                            
                    )
                ''')

                conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def saveTestSubject(self, name:str, age:int, gender:str):
        try: 
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO test_subjects (name, age, gender) VALUES (?, ?, ?)', (name, age, gender))
                
                return True
        except sqlite3.Error as e:
            return e




manager = Manager()
