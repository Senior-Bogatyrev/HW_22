class InfoMessage:
    '''Информационное сообщение о тренировке.'''
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
    

class Training:
    '''Базовый класс тренировки.'''

    def __init__(self, action: int, duration: float, weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight
    
    M_IN_KM = 1000
    LEN_STEP = 0.65
    HOUR_IN_MIN = 60
        
    def get_distance(self):
        return self.action * self.LEN_STEP / self.M_IN_KM
    
    def get_mean_speed(self):
        return self.get_distance() / self.duration
    
    def get_spent_calories(self):
        pass

    def show_training_info(self):
        return InfoMessage(self.__class__.__name__, self.duration, 
                           self.get_distance(), self.get_mean_speed(), 
                            self.get_spent_calories())


class Running(Training):
    '''Тренировка: бег.'''

    def get_spent_calories(self):
        CALORIES_MEAN_SPEED_MULTIPLIER = 18
        CALORIES_MEAN_SPEED_SHIFT = 1.79

        return ((CALORIES_MEAN_SPEED_MULTIPLIER * self.get_distance() + 
        CALORIES_MEAN_SPEED_SHIFT)* self.weight / self.M_IN_KM * self.duration 
        * self.HOUR_IN_MIN) 


class SportsWalking(Training):
    '''Тренировка: спортивная ходьба.'''
    def __init__(self, action: int, duration: float, weight: float, 
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    COEF_ONE = 0.035
    COEF_TWO = 0.029
    CENTIM_IN_METERS = 100
    KMH_IN_MS = 0.28

    def get_spent_calories(self):
        return ((self.COEF_ONE * self.weight + ((self.get_mean_speed() * 
            self.KMH_IN_MS)**2 / (self.height/ self.CENTIM_IN_METERS)) * 
            self.COEF_TWO * self.weight) * self.duration * self.HOUR_IN_MIN)


class Swimming(Training):
    '''Тренировка: плавание.'''
    def __init__(self, action: int, duration: float, weight: float, 
                 length_pool: int, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    LEN_STEP = 1.38
    COEF_ONE = 1.1
    COEF_TWO = 2

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM /
                (self.duration))

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.COEF_ONE) * self.COEF_TWO 
            * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    '''Прочитать данные полученные от датчиков.'''
    train_dict = {
        'SWM' : Swimming,
        'RUN' : Running,
        'WLK' : SportsWalking
    }

    return train_dict.get(workout_type)(*data)


def main(training: Training) -> None:
    '''Главная функция.'''
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
