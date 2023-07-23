class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        km_distance = self.get_distance()
        return km_distance / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        min_speed = self.duration * self.MINUTES
        mid_speed = super().get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * mid_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * min_speed)


class SportsWalking(Training):
    WALK_CONST_1 = 0.035
    WALK_CONST_2 = 0.029
    WALK_CONST_3 = 0.278
    WALK_CONST_4 = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        ms_speed = super().get_mean_speed() * self.WALK_CONST_3
        m_height = self.height / self.WALK_CONST_4
        min_duration = self.duration * self.MINUTES
        return ((self.WALK_CONST_1 * self.weight
                 + (ms_speed**2 / m_height) * self.WALK_CONST_2
                 * self.weight) * min_duration)


class Swimming(Training):
    LEN_STEP = 1.38
    SWIMM_CONST_1 = 1.1
    SWIMM_CONST_2 = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        mid_speed = self.get_mean_speed()
        calories = ((mid_speed + self.SWIMM_CONST_1)
                    * self.SWIMM_CONST_2 * self.weight
                    * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    training_dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    its_work = training.show_training_info()
    print(its_work.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
