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
                #intersection_x is x coordinate of intersection
                #intersection_y is y coordinate of intersection
                #subject_guess_x is x coordinate of subject guess
                #subject_guess_y is y coordinate of subject guess
                #absolute_error_pixels is absolute error in pixels
                #absolute_error_mm is absolute error in mm
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS poggendorff_results (
                        test_subject,
                        w_param FLOAT NOT NULL,
                        h_param FLOAT NOT NULL,
                        alpha_angle FLOAT NOT NULL,
                        beta_angle FLOAT NOT NULL,
                        intersection_x FLOAT NOT NULL,
                        intersection_y FLOAT NOT NULL,
                        subject_guess_x FLOAT NOT NULL,
                        subject_guess_y FLOAT NOT NULL,
                        absolute_error_pixels FLOAT NOT NULL,
                        absolute_error_mm FLOAT NOT NULL               
                    )
                ''')

                #Müller-Lyer illusion results table
                #test_subject id of test subject
                #r_param is size of circles
                #d_param is distance between circles
                #alpha_angle is angle of illusion rotation
                #desired_point_x is x coordinate of desired point
                #desired_point_y is y coordinate of desired point
                #subject_guess_x is x coordinate of subject guess
                #subject_guess_y is y coordinate of subject guess
                #absolute_error_pixels is absolute error in pixels
                #absolute_error_mm is absolute error in mm
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS muller_lyer_results (
                        test_subject,
                        r_param FLOAT NOT NULL,
                        d_param FLOAT NOT NULL,
                        alpha_angle FLOAT NOT NULL,
                        desired_point_x FLOAT NOT NULL,
                        desired_point_y FLOAT NOT NULL,
                        subject_guess_x FLOAT NOT NULL,
                        subject_guess_y FLOAT NOT NULL,
                        absolute_error_pixels FLOAT NOT NULL,
                        absolute_error_mm FLOAT NOT NULL
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
        '''Save the test subject with the given name, age'''
        try:
            subject = self.getTestSubjectId(name, age)
            if subject is not None:
                return subject
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                INSERT INTO test_subjects (
                    name, age, gender
                ) 
                VALUES (?, ?, ?)
                ''', (name, age, gender))
                return self.getTestSubjectId(name, age)
        except sqlite3.Error as e:
            return e

    def savePoggendorffResult(self, test_subject_id: int, w_param: float, 
                            h_param: float, alpha_angle: float, 
                            beta_angle: float, intersection_x: float,
                            intersection_y: float, subject_guess_x: float,
                            subject_guess_y: float, absolute_error_pixels: float,
                            absolute_error_mm: float):
        '''
        test_subject id of test subject\n
        w_param is width of wall\n
        h_param is height at which lines aligned\n
        alpha_angle is angle of line rotation\n
        beta_angle is angle of illusion rotation\n
        intersection_x is x coordinate of intersection\n
        intersection_y is y coordinate of intersection\n
        subject_guess_x is x coordinate of subject guess\n
        subject_guess_y is y coordinate of subject guess\n
        absolute_error_pixels is absolute error in pixels\n
        absolute_error_mm is absolute error in mm\n
        '''
        try: 
            result = (
                test_subject_id,
                w_param,
                h_param,
                alpha_angle,
                beta_angle,
                intersection_x,
                intersection_y,
                subject_guess_x,
                subject_guess_y,
                absolute_error_pixels,
                absolute_error_mm
            )
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                INSERT INTO poggendorff_results (
                    test_subject, w_param, h_param,
                    alpha_angle, beta_angle, intersection_x,
                    intersection_y, subject_guess_x,
                    subject_guess_y, absolute_error_pixels,
                    absolute_error_mm
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', result)
                conn.commit()
                return True
        except sqlite3.Error as e:
            return e
        
    def saveMullerLyerResult(self, test_subject_id: int, r_param: float,
                            d_param: float, alpha_angle: float, 
                            desired_point_x: float, desired_point_y: float,
                            subject_guess_x: float, subject_guess_y: float,
                            absolute_error_pixels: float, absolute_error_mm: float):
        '''
        test_subject id of test subject\n
        r_param is size of circles\n
        d_param is distance between circles\n
        alpha_angle is angle of illusion rotation\n
        desired_point_x/y is cord of desired point\n
        subject_guess_x/y is cord at which the subject aligns the circle\n
        absolute_error_pixels is absolute error in pixels\n
        absolute_error_mm is absolute error in mm\n
        '''
        try:
            result = (
                test_subject_id,
                r_param,
                d_param,
                alpha_angle,
                desired_point_x,
                desired_point_y,
                subject_guess_x,
                subject_guess_y,
                absolute_error_pixels,
                absolute_error_mm,
            )
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                INSERT INTO muller_lyer_results (
                    test_subject, r_param, d_param,
                    alpha_angle, desired_point_x, desired_point_y,
                    subject_guess_x, subject_guess_y,
                    absolute_error_pixels, absolute_error_mm
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    
    def getTestSubjectId(self, name:str, age:int):
        '''Get the id of the test subject with the given name and age'''
        try:
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                SELECT id FROM test_subjects WHERE name = ? AND age = ?
                ''', (name, age))
                fetch_result = cur.fetchone()
                if fetch_result is not None:
                    self.lastSubjectId = fetch_result[0]
                return self.lastSubjectId
        except sqlite3.Error as e:
            return e
        
    def getTestSubject(self, test_subject_id:int):
        '''Get the test subject with the given id'''
        try:
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                SELECT * FROM test_subjects WHERE id = ?
                ''', (test_subject_id,))
                return cur.fetchone()
        except sqlite3.Error as e:
            return e
    
    def getPoggendorffResults(self, test_subject_id:int):
        '''Get the Poggendorff illusion results of the test subject with the given id'''
        try:
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                SELECT * FROM poggendorff_results WHERE test_subject = ?
                ''', (test_subject_id,))
                return cur.fetchall()
        except sqlite3.Error as e:
            return e
    
    def getMullerLyerResults(self, test_subject_id:int):
        '''Get the Müller-Lyer illusion results of the test subject with the given id'''
        try:
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                SELECT * FROM muller_lyer_results WHERE test_subject = ?
                ''', (test_subject_id,))
                return cur.fetchall()
        except sqlite3.Error as e:
            return e
    
    def getVertHorzResults(self, test_subject_id:int):
        '''Get the Vertical-horizontal illusion results of the test subject with the given id'''
        try:
            with sqlite3.connect(self.database_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                SELECT * FROM vert_horz_results WHERE test_subject = ?
                ''', (test_subject_id,))
                return cur.fetchall()
        except sqlite3.Error as e:
            return e

if __name__ == "__main__":
    manager = Manager()
    test_subject_name = 'John Doe'
    test_subject_age = 25

    print(manager.saveTestSubject(test_subject_name, test_subject_age, 'ThermoNuclearMissile'))

    test_subject_id = manager.getTestSubjectId(test_subject_name, test_subject_age)
    print(test_subject_id)
    print(manager.getTestSubject(test_subject_id))

    print(manager.savePoggendorffResult(test_subject_id, 3, 4.4, 5.4, 13, 3, 4, 5, 6, 7, 8))
    print(manager.saveMullerLyerResult(test_subject_id, 3, 4.4, 5.4, 13))
    print(manager.saveVertHorzResult(test_subject_id, 32, 42, 5, 52, 3))

    print(manager.getPoggendorffResults(test_subject_id))
    print(manager.getMullerLyerResults(test_subject_id))
    print(manager.getVertHorzResults(test_subject_id))


