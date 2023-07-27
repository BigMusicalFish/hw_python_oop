from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Informational message about training."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    results = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.results.format(*asdict(self).values())


@dataclass
class Training:
    """Basic training class."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Get the distance km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the average speed of movement."""
        km_distance = self.get_distance()
        return km_distance / self.duration

    def get_spent_calories(self) -> float:
        """Get the calories expended"""
        raise NotImplementedError('Использован метод базового класса.')

    def show_training_info(self) -> InfoMessage:
        """Return the information message about the completed training"""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    '''Training - running.'''
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        '''Return the calories spent while running.'''
        min_speed = self.duration * self.MINUTES
        mid_speed = super().get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * mid_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * min_speed)


@dataclass
class SportsWalking(Training):
    '''Training - sports walking.'''
    SETTING_WALK_1 = 0.035
    SETTING_WALK_2 = 0.029
    METERS_SECONDS = 0.278
    CENTIMETRS = 100

    height: float

    def get_spent_calories(self):
        '''Return the calories spent while walking.'''
        ms_speed = super().get_mean_speed() * self.METERS_SECONDS
        m_height = self.height / self.CENTIMETRS
        min_duration = self.duration * self.MINUTES
        return ((self.SETTING_WALK_1 * self.weight
                 + (ms_speed**2 / m_height) * self.SETTING_WALK_2
                 * self.weight) * min_duration)


@dataclass
class Swimming(Training):
    '''Training - swimming.'''
    LEN_STEP = 1.38
    SETTING_SWIMM_1 = 1.1
    SETTING_SWIMM_2 = 2

    length_pool: float
    count_pool: float

    def get_mean_speed(self):
        """Get an average speed when swimming."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        '''Return the calories spent while swimming.'''
        mid_speed = self.get_mean_speed()
        calories = ((mid_speed + self.SETTING_SWIMM_1)
                    * self.SETTING_SWIMM_2 * self.weight
                    * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    '''Read the sensor data.'''
    training_dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type not in training_dict:
        return ('Incorrect workout type.')
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    '''Print a training message.'''
    its_work = training.show_training_info()
    print(its_work.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('WLK', [9000, 1.5, 75, 180]),
        ('WLK', [3000.33, 2.512, 75.8, 180.1])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
