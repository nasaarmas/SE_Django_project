def add_current_group_id(request):
    # Możesz ustawić logikę, jak pobierasz current_group_id, np. z URL lub sesji
    current_group_id = request.session.get('current_group_id', None)
    return {'current_group_id': current_group_id}

