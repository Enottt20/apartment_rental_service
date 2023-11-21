import schemas


def reservation_notification_message(
        message: schemas.ReservationNotification
) -> str:
    msg = (f'Вы арендовали {message.apartment_data.title} \n'\
           f'по адрессу {message.apartment_data.address} \n'\
           f'с {message.arrival_date} '\
           f'по {message.departure_date} ')

    return msg

def review_notification_message(
        message: schemas.ReviewNotification
) -> str:
    msg = (f'Вам оставили отзыв - \n '\
           f'{message.title} \n'\
           f'{message.description} \n')

    return msg
