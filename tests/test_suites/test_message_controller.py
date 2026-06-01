from tests.rest.models.model import MessageRequestDto

def test_delete_message(create_messages, message_repository, message_api):
    response = message_api.delete(message_repository.get_by_id(create_messages.id).get("id"))
    user_message = message_repository.get_by_id(create_messages.id)
    assert user_message is None
    assert response.status_code == 200


def test_create_message(temp_user, delete_messages, faker_instance, message_api):
    dto = MessageRequestDto(
        senderId=temp_user.id,
        receiverId=temp_user.id,
        content=faker_instance.text(),
    )
    delete_messages.append(temp_user.id)
    response = message_api.create(dto)
    assert response.content == dto.content
    assert response.sender.id == temp_user.id
    assert response.sender.username == temp_user.username
    assert response.receiver.id == temp_user.id


def test_get_dialog(create_messages, delete_messages, message_api):
    response = message_api.get_dialog(sender_id=create_messages.id, receiver_id=create_messages.id)
    delete_messages.append(create_messages.id)
    data = [(msg.sender.id, msg.sender.username) for msg in response if msg.sender.id == create_messages.id]
    for mid, username in data:
        assert mid == create_messages.id
        assert username == create_messages.username
