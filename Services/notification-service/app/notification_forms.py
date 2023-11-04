from .schemas import ReservationNotification


def reservation_notification_message(
        message: ReservationNotification
) -> str:
    msg = (f'Вы арендовали {message.apartment_data.title} \n'\
           f'по адрессу {message.apartment_data.address} \n'\
           f'с {message.arrival_date} '\
           f'по {message.departure_date} ')

    return msg