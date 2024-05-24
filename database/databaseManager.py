import sqlite3

class Manager():
    database_path = ''
    lastSubjectId = None

    def __init__(self, database_path = 'database/svodb.db') -> None:
        try:
            self.database_path = database_path
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                #Subjects table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS test_subjects (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age FLOAT NOT NULL,
                        gender TEXT NOT NULL
                    )
                ''')

                #Poggendorff illusion results table
                #test_subject id of test subject
                #w_param is width of wall
                #h_param is height at which lines aligned
                #h_subject_guess is height at which subject aligned line
                #alpha_angle is angle of line rotation
                #beta_angle is angle of illusion rotation
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS poggendorff_results (
                        test_subject,
                        w_param FLOAT NOT NULL,
                        h_param FLOAT NOT NULL,
                        h_subject_guess FLOAT NOT NULL,
                        alpha_angle FLOAT NOT NULL,
                        beta_angle FLOAT NOT NULL                            
                    )
                ''')

                #Müller-Lyer illusion results table
                #test_subject id of test subject
                #s_param is size of circles
                #d_param is distance between circles
                #d_subject_guess is length at which the subject aligns the circle
                #alpha_angle is angle of illusion rotation
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS muller_lyer_results (
                        test_subject,
                        s_param FLOAT NOT NULL,
                        d_param FLOAT NOT NULL,
                        d_subject_guess FLOAT NOT NULL,
                        alpha_angle FLOAT NOT NULL
                    )
                ''')

                #Vertical–horizontal illusion results table
                #test_subject id of test subject
                #h_param is length of vertical line
                #h_subject_guess is length at which the subject aligns the vertical line
                #d_param is horizontal offset of vertical
                #beta_angle is angle of vertical line
                #alpha_angle is angle of illusion rotation
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS vert_horz_results (
                        test_subject INTEGER,
                        h_param FLOAT NOT NULL,
                        h_subject_guess FLOAT NOT NULL,
                        d_param FLOAT NOT NULL,
                        beta_angle FLOAT NOT NULL,
                        alpha_angle FLOAT NOT NULL
                    )
                '''
                )

                conn.commit()
        except sqlite3.Error as e:
            return e

    def saveTestSubject(self, name:str, age:int, gender:str):
        try: 
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                INSERT INTO test_subjects (
                    name, age, gender
                ) 
                VALUES (?, ?, ?)
                ''', (name, age, gender))
                return True
        except sqlite3.Error as e:
            return e

    def savePoggendorffResult(self, test_subject_id: int, w_param: float, 
                            h_param: float, h_subject_guess: float, 
                            alpha_angle: float, beta_angle: float):
        '''
        test_subject id of test subject\n
        w_param is width of wall\n
        h_param is height at which lines aligned\n
        h_subject_guess is height at which subject aligned line\n
        alpha_angle is angle of line rotation\n
        beta_angle is angle of illusion rotation\n
        '''
        try: 
            result = (
                test_subject_id,
                w_param,
                h_param,
                h_subject_guess,
                alpha_angle,
                beta_angle
            )
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                INSERT INTO poggendorff_results (
                    test_subject, w_param, h_param,
                    h_subject_guess, alpha_angle, beta_angle
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ''', result)
                conn.commit()
                return True
        except sqlite3.Error as e:
            return e
        
    def saveMullerLyerResult(self, test_subject_id: int, s_param: float, 
                            d_param: float, d_subject_guess: float, 
                            alpha_angle: float):
        '''
        test_subject id of test subject\n
        s_param is size of circles\n
        d_param is distance between circles\n
        d_subject_guess is length at which the subject aligns the circle\n
        alpha_angle is angle of illusion rotation\n
        '''
        try:
            result = (
                test_subject_id,
                s_param,
                d_param,
                d_subject_guess,
                alpha_angle
            )
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                INSERT INTO muller_lyer_results (
                    test_subject, s_param, d_param,
                    d_subject_guess, alpha_angle
                )
                VALUES (?, ?, ?, ?, ?)
                ''', result)
                conn.commit()
                return True
        except sqlite3.Error as e:
            return e
            
    def saveVertHorzResult(self, test_subject_id: int, h_param: float, 
                            h_subject_guess: float, d_param: float, 
                            beta_angle: float, alpha_angle: float):
        '''
        test_subject id of test subject\n
        h_param is length of vertical line\n
        h_subject_guess is length at which the subject aligns the vertical line\n
        d_param is horizontal offset of vertical\n
        beta_angle is angle of vertical line\n
        alpha_angle is angle of illusion rotation\n
        '''
        try:
            result = (
                test_subject_id,
                h_param,
                h_subject_guess,
                d_param,
                beta_angle,
                alpha_angle
            )
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                INSERT INTO vert_horz_results (
                    test_subject, h_param, h_subject_guess,
                    d_param, beta_angle, alpha_angle
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ''', result)
                conn.commit()
                return True
        except sqlite3.Error as e:
            return e

if __name__ == "__main__":
    manager = Manager()
    manager.saveTestSubject('ADdsada', 12, 'ThermoNuclearMissile')
    print(manager.savePoggendorffResult(1, 12.0, 3, 4, 12, 4))
    print(manager.saveMullerLyerResult(2, 3, 4.4, 5.4, 13))
    print(manager.saveVertHorzResult(1, 32, 42, 5, 52, 3))
