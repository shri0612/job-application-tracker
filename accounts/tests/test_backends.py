from accounts.backends import EmailBackend

def test_email_backend_authenticate_no_user():
    backend = EmailBackend()
    user = backend.authenticate(None, username="nouser@example.com", password="wrongpass")
    assert user is None
